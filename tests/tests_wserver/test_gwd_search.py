import unittest
from types import SimpleNamespace
from unittest.mock import patch
from flask import Flask

from wserver.routes.gwd import gwd_bp


class TestGwdSearch(unittest.TestCase):
    def setUp(self):
        import os
        test_dir = os.path.dirname(os.path.abspath(__file__))
        template_folder = os.path.join(
            test_dir, '..', 'src', 'wserver', 'templates')
        self.app = Flask(__name__, template_folder=template_folder)
        self.app.config['TESTING'] = True
        self.app.register_blueprint(gwd_bp)
        self.client = self.app.test_client()

    @patch('wserver.routes.search.render_template')
    @patch('wserver.routes.search.get_db_service')
    def test_search_by_surname_renders_correct_template(self, mock_get_db_service, mock_render):
        mock_render.return_value = '<html>search</html>'
        fake_db = SimpleNamespace()
        fake_db.get_session = lambda: 's'
        # Emulate get_all(session, Person, {'surname': 'Smith'})
        fake_db.get_all = lambda session, model, filters=None: [
            SimpleNamespace(first_name='A', surname='Smith')]
        mock_get_db_service.return_value = fake_db

        resp = self.client.get('/gwd/testbase/search?surname=Smith')
        self.assertEqual(resp.status_code, 200)
        mock_render.assert_called_once()
        args, kwargs = mock_render.call_args
        self.assertEqual(args[0], 'gwd/search_surname.html')

    @patch('wserver.routes.search.render_template')
    @patch('wserver.routes.search.get_db_service')
    def test_search_alpha_on_surname_groups_correctly(self, mock_get_db_service, mock_render):
        mock_render.return_value = '<html>alpha</html>'
        # Create persons to exercise grouping by surname initial
        p1 = SimpleNamespace(first_name='John', surname='Alpha')
        p2 = SimpleNamespace(first_name='Jane', surname='Alpha')
        p3 = SimpleNamespace(first_name='Bob', surname='Beta')

        fake_db = SimpleNamespace()
        fake_db.get_session = lambda: 's'
        # When called without filters, get_all returns all persons
        fake_db.get_all = lambda session, model, filters=None: [p1, p2, p3]
        mock_get_db_service.return_value = fake_db

        resp = self.client.get('/gwd/testbase/search?sort=alpha&on=surname')
        self.assertEqual(resp.status_code, 200)
        mock_render.assert_called_once()
        args, kwargs = mock_render.call_args
        self.assertEqual(args[0], 'gwd/search_surnames_alpha.html')
        persons_grouped = kwargs.get('persons_grouped')
        # Expect two letters groups A and B
        letters = [g['letter'].upper() for g in persons_grouped]
        self.assertIn('A', letters)
        self.assertIn('B', letters)

    @patch('wserver.routes.search.render_template')
    @patch('wserver.routes.search.get_db_service')
    def test_search_freq_on_firstname_counts_correctly(self, mock_get_db_service, mock_render):
        mock_render.return_value = '<html>freq</html>'
        # Two Johns and one Alice
        p1 = SimpleNamespace(first_name='John', surname='X')
        p2 = SimpleNamespace(first_name='John', surname='Y')
        p3 = SimpleNamespace(first_name='Alice', surname='Z')

        fake_db = SimpleNamespace()
        fake_db.get_session = lambda: 's'
        fake_db.get_all = lambda session, model, filters=None: [p1, p2, p3]
        mock_get_db_service.return_value = fake_db

        resp = self.client.get('/gwd/testbase/search?sort=freq&on=firstname')
        self.assertEqual(resp.status_code, 200)
        mock_render.assert_called_once()
        args, kwargs = mock_render.call_args
        self.assertEqual(args[0], 'gwd/search_firstnames_freq.html')
        persons_grouped = kwargs.get('persons_grouped')
        # First group should be John with count 2
        self.assertGreaterEqual(len(persons_grouped), 1)
        self.assertEqual(persons_grouped[0]['count'], 2)
