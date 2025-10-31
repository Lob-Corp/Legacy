import unittest
from types import SimpleNamespace
from unittest.mock import patch
from flask import Flask

from wserver.routes.gwd import gwd_bp


class QueryStub:
    def __init__(self, key, results_map):
        self.key = key
        self.results_map = results_map

    def join(self, *args, **kwargs):
        return self

    def filter(self, *args, **kwargs):
        return self

    def order_by(self, *args, **kwargs):
        return self

    def group_by(self, *args, **kwargs):
        return self

    def all(self):
        return self.results_map.get(self.key, [])


class FakeSession:
    def __init__(self, results_map):
        self.results_map = results_map

    def query(self, model=None, *args, **kwargs):
        # Normalize a few common names used in titles.py
        name = getattr(model, '__name__', None)
        if name:
            key = name
        else:
            s = str(model)
            if 'title' in s.lower():
                key = 'Titles'
            elif 'person' in s.lower():
                key = 'Person'
            else:
                key = 'Misc'
        return QueryStub(key, self.results_map)


class TestGwdTitles(unittest.TestCase):
    def setUp(self):
        import os
        test_dir = os.path.dirname(os.path.abspath(__file__))
        template_folder = os.path.join(
            test_dir, '..', 'src', 'wserver', 'templates')
        self.app = Flask(__name__, template_folder=template_folder)
        self.app.config['TESTING'] = True
        self.app.register_blueprint(gwd_bp)
        self.client = self.app.test_client()

    @patch('wserver.routes.titles.render_template')
    @patch('wserver.routes.titles.get_db_service')
    def test_titles_single_result_renders_detail(self, mock_get_db_service, mock_render):
        mock_render.return_value = '<html>title detail</html>'
        the_title = SimpleNamespace(id=1, name='Lord', place='Castle')
        person = SimpleNamespace(first_name='John', surname='Doe')
        results_map = {
            'Titles': [the_title],
            'Person': [person]
        }

        fake_db = SimpleNamespace()
        fake_db.get_session = lambda: FakeSession(results_map)
        mock_get_db_service.return_value = fake_db

        resp = self.client.get('/gwd/testbase/titles?title=Lord&fief=Castle')
        self.assertEqual(resp.status_code, 200)
        mock_render.assert_called_once()
        args, kwargs = mock_render.call_args
        self.assertEqual(args[0], 'gwd/title_detail.html')
        self.assertEqual(kwargs['title_name'], 'Lord')
        self.assertEqual(kwargs['estate_name'], 'Castle')

    @patch('wserver.routes.titles.render_template')
    @patch('wserver.routes.titles.get_db_service')
    def test_titles_listing_groups_and_counts(self, mock_get_db_service, mock_render):
        mock_render.return_value = '<html>titles list</html>'
        # Several titles with varied initials
        t1 = SimpleNamespace(name='Alpha')
        t2 = SimpleNamespace(name='Alpha II')
        t3 = SimpleNamespace(name='Beta')
        results_map = {'Titles': [t1, t2, t3]}

        fake_db = SimpleNamespace()
        fake_db.get_session = lambda: FakeSession(results_map)
        mock_get_db_service.return_value = fake_db

        resp = self.client.get('/gwd/testbase/titles')
        self.assertEqual(resp.status_code, 200)
        mock_render.assert_called_once()
        args, kwargs = mock_render.call_args
        self.assertEqual(args[0], 'gwd/titles_all.html')
        self.assertEqual(kwargs['total_titles'], 3)
