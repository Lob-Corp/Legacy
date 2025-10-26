import unittest
from unittest.mock import patch
from flask import Flask
from wserver.routes.gwsetup import gwsetup_bp

class TestBaseRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(gwsetup_bp)
        self.client = self.app.test_client()

    @patch('wserver.routes.gwsetup._template_service')
    def test_route_welcome(self, mock_service):
        mock_service.render_gwsetup_template.return_value = '<html>ok</html>'
        response = self.client.get('gwsetup/welcome/fr')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ok', response.data)

    @patch('wserver.routes.gwsetup._template_service')
    def test_route_delete(self, mock_service):
        mock_service.render_gwsetup_template.return_value = '<html>ok</html>'
        response = self.client.get('gwsetup/delete/fr')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ok', response.data)

    def test_not_implemented_routes(self):
        not_implemented_routes = [
            '/robots.txt', '/backg.htm', '/bsc.htm', '/bsi_cache_files.htm',
            '/bsi_connnex.htm', '/bsi_diff.htm', '/bsi_err.htm', '/bsi_fix.htm',
            '/bsi.htm', '/bso_comm.htm', '/bso_err.htm', '/bso_log.htm',
            '/bso_ok.htm', '/bso.htm', '/cache_file_ok.htm', '/cache_files.htm',
            '/clean_ok.htm', '/cleanup.htm', '/cleanup1.htm', '/connex_ok.htm',
            '/connex.htm', '/consang.htm', '/consg_ok.htm', '/del_ok.htm',
            '/delete_1.htm', '/delete.htm', '/err_acc.htm', '/err_cnfl.htm',
            '/err_miss.htm', '/err_name.htm', '/err_ndir.htm', '/err_ngw.htm',
            '/err_outd.htm', '/err_reco.htm', '/err_smdr.htm', '/err_unkn.htm',
            '/ged2gwd.htm', '/gw2gd_ok.htm', '/gwb2ged.htm', '/gwc.htm',
            '/gwd_info.htm', '/gwd_ok.htm', '/gwd.htm', '/gwdiff_ok.htm',
            '/gwdiff.htm', '/gwf_1.htm', '/gwf_ok.htm', '/gwfix_ok.htm',
            '/gwfix.htm', '/gwu_ok.htm', '/gwu.htm', '/intro.htm', '/list.htm',
            '/macros.htm', '/main.htm', '/merge_1.htm', '/merge.htm',
            '/recover.htm', '/recover1.htm', '/recover2.htm', '/ren_ok.htm',
            '/rename.htm', '/save.htm', '/simple.htm', '/traces.htm',
            '/update_nldb_ok.htm', '/update_nldb.htm', '/welcome.htm'
        ]
        for route in not_implemented_routes:
            resp = self.client.get('gwsetup' + route)
            self.assertEqual(
                resp.status_code, 500,
                msg=f"Route {route} should return 500 NotImplementedError"
            )

if __name__ == '__main__':
    unittest.main()
