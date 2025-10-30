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
        # Titles.name query will come in as an expression; normalize to 'Titles'
        return QueryStub('Titles', self.results_map)


class TestGwdFiefs(unittest.TestCase):
    def setUp(self):
        import os
        test_dir = os.path.dirname(os.path.abspath(__file__))
        template_folder = os.path.join(
            test_dir, '..', 'src', 'wserver', 'templates')
        self.app = Flask(__name__, template_folder=template_folder)
        self.app.config['TESTING'] = True
        self.app.register_blueprint(gwd_bp)
        self.client = self.app.test_client()

    @patch('wserver.routes.fiefs.render_template')
    @patch('wserver.routes.fiefs.get_db_service')
    def test_fiefs_renders_list_with_counts(self, mock_get_db_service, mock_render):
        mock_render.return_value = '<html>fiefs</html>'
        # The route expects a list of (name, count) tuples
        results_map = {'Titles': [('Castle', 3), ('Manor', 1)]}
        fake_db = SimpleNamespace()
        fake_db.get_session = lambda: FakeSession(results_map)
        mock_get_db_service.return_value = fake_db

        resp = self.client.get('/gwd/testbase/fiefs')
        self.assertEqual(resp.status_code, 200)
        mock_render.assert_called_once()
        args, kwargs = mock_render.call_args
        self.assertEqual(args[0], 'gwd/fiefs_all.html')
        self.assertEqual(kwargs['total_titles'], 2)
