import unittest
from types import SimpleNamespace
from unittest.mock import patch
from flask import Flask

from wserver.routes.gwd import gwd_bp


class TestGwdHomepage(unittest.TestCase):
    def setUp(self):
        import os
        test_dir = os.path.dirname(os.path.abspath(__file__))
        template_folder = os.path.join(
            test_dir, '..', 'src', 'wserver', 'templates')
        self.app = Flask(__name__, template_folder=template_folder)
        self.app.config['TESTING'] = True
        self.app.register_blueprint(gwd_bp)
        self.client = self.app.test_client()

    @patch('wserver.routes.homepage.render_template')
    @patch('wserver.routes.homepage.get_db_service')
    def test_homepage_renders_and_passes_total(self, mock_get_db_service, mock_render):
        mock_render.return_value = '<html>home</html>'
        fake_db = SimpleNamespace()
        fake_db.get_session = lambda: 'session'
        fake_db.get_all = lambda session, model: [
            SimpleNamespace(), SimpleNamespace(), SimpleNamespace()]
        mock_get_db_service.return_value = fake_db

        resp = self.client.get('/gwd/testbase')
        self.assertEqual(resp.status_code, 200)
        mock_render.assert_called_once()
        args, kwargs = mock_render.call_args
        self.assertEqual(args[0], 'gwd/homepage.html')
        # total_persons should match the number returned by fake_db.get_all
        self.assertEqual(kwargs['total_persons'], 3)
