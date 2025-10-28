from flask import Blueprint, request, make_response
from ..services.template_loader import TemplateService
# Blueprint exposed for legacy gw setup endpoints
gwsetup_bp = Blueprint('gwsetup', __name__, url_prefix='/gwsetup')
_template_service = TemplateService()


def _render_setup(fname: str, lang: str):
    """
    Small wrapper used by the Flask routes:
      - fname e.g. 'welcome.htm'
      - lang e.g. 'fr'
    """
    # build params dict for TemplateService (host/port/o)
    host = request.host.split(':')[0]
    port = request.host.split(':')[1] if ':' in request.host else ""
    params = {  # noqa: F841
        "host": host,
        "port": port,
        "o": request.args.get("o", "")
    }
    html_str = _template_service.render_gwsetup_template(fname)
    resp = make_response(html_str)
    resp.headers["Content-Type"] = "text/html; charset=utf-8"
    return resp


@gwsetup_bp.route('/welcome/<lang>', methods=['GET', 'POST'])
def route_welcome(lang):
    return _render_setup("welcome.htm", lang)


@gwsetup_bp.route('/delete/<lang>', methods=['GET', 'POST'])
def route_delete(lang):
    return _render_setup("delete.htm", lang)


@gwsetup_bp.route('/delete_1/<lang>', methods=['GET', 'POST'])
def route_delete_1(lang):
    return _render_setup("delete_1.htm", lang)


@gwsetup_bp.route('/list/<lang>', methods=['GET', 'POST'])
def route_list(lang):
    return _render_setup("list.htm", lang)


@gwsetup_bp.route('/main/<lang>', methods=['GET', 'POST'])
def route_main(lang):
    return _render_setup("main.htm", lang)


@gwsetup_bp.route('/traces/<lang>', methods=['GET', 'POST'])
def route_traces(lang):
    return _render_setup("traces.htm", lang)


@gwsetup_bp.route('/gwc/<lang>', methods=['GET', 'POST'])
def route_gwc(lang):
    return _render_setup("gwc.htm", lang)


@gwsetup_bp.route('/gwu/<lang>', methods=['GET', 'POST'])
def route_gwu(lang):
    return _render_setup("gwu.htm", lang)
# overview of the routes and endpoints will be refactor


@gwsetup_bp.route('/robots.txt')
def robots_txt_route():
    raise NotImplementedError(
        "Route /robots.txt (robots_txt_route) not implemented yet"
    )


@gwsetup_bp.route('/backg.htm')
def backg_htm():
    raise NotImplementedError(
        "Route /backg.htm (backg_htm) not implemented yet"
    )


@gwsetup_bp.route('/bsc.htm')
def bsc_htm():
    raise NotImplementedError(
        "Route /bsc.htm (bsc_htm) not implemented yet"
    )


@gwsetup_bp.route('/bsi_cache_files.htm')
def bsi_cache_files_htm():
    raise NotImplementedError(
        "Route /bsi_cache_files.htm (bsi_cache_files_htm) not implemented yet"
    )


@gwsetup_bp.route('/bsi_connnex.htm')
def bsi_connnex_htm():
    raise NotImplementedError(
        "Route /bsi_connnex.htm (bsi_connnex_htm) not implemented yet"
    )


@gwsetup_bp.route('/bsi_diff.htm')
def bsi_diff_htm():
    raise NotImplementedError(
        "Route /bsi_diff.htm (bsi_diff_htm) not implemented yet"
    )


@gwsetup_bp.route('/bsi_err.htm')
def bsi_err_htm():
    raise NotImplementedError(
        "Route /bsi_err.htm (bsi_err_htm) not implemented yet"
    )


@gwsetup_bp.route('/bsi_fix.htm')
def bsi_fix_htm():
    raise NotImplementedError(
        "Route /bsi_fix.htm (bsi_fix_htm) not implemented yet"
    )


@gwsetup_bp.route('/bsi.htm')
def bsi_htm():
    raise NotImplementedError(
        "Route /bsi.htm (bsi_htm) not implemented yet"
    )


@gwsetup_bp.route('/bso_comm.htm')
def bso_comm_htm():
    raise NotImplementedError(
        "Route /bso_comm.htm (bso_comm_htm) not implemented yet"
    )


@gwsetup_bp.route('/bso_err.htm')
def bso_err_htm():
    raise NotImplementedError(
        "Route /bso_err.htm (bso_err_htm) not implemented yet"
    )


@gwsetup_bp.route('/bso_log.htm')
def bso_log_htm():
    raise NotImplementedError(
        "Route /bso_log.htm (bso_log_htm) not implemented yet"
    )


@gwsetup_bp.route('/bso_ok.htm')
def bso_ok_htm():
    raise NotImplementedError(
        "Route /bso_ok.htm (bso_ok_htm) not implemented yet"
    )


@gwsetup_bp.route('/bso.htm')
def bso_htm():
    raise NotImplementedError(
        "Route /bso.htm (bso_htm) not implemented yet"
    )


@gwsetup_bp.route('/cache_file_ok.htm')
def cache_file_ok_htm():
    raise NotImplementedError(
        "Route /cache_file_ok.htm (cache_file_ok_htm) not implemented yet"
    )


@gwsetup_bp.route('/cache_files.htm')
def cache_files_htm():
    raise NotImplementedError(
        "Route /cache_files.htm (cache_files_htm) not implemented yet"
    )


@gwsetup_bp.route('/clean_ok.htm')
def clean_ok_htm():
    raise NotImplementedError(
        "Route /clean_ok.htm (clean_ok_htm) not implemented yet"
    )


@gwsetup_bp.route('/cleanup.htm')
def cleanup_htm():
    raise NotImplementedError(
        "Route /cleanup.htm (cleanup_htm) not implemented yet"
    )


@gwsetup_bp.route('/cleanup1.htm')
def cleanup1_htm():
    raise NotImplementedError(
        "Route /cleanup1.htm (cleanup1_htm) not implemented yet"
    )


@gwsetup_bp.route('/connex_ok.htm')
def connex_ok_htm():
    raise NotImplementedError(
        "Route /connex_ok.htm (connex_ok_htm) not implemented yet"
    )


@gwsetup_bp.route('/connex.htm')
def connex_htm():
    raise NotImplementedError(
        "Route /connex.htm (connex_htm) not implemented yet"
    )


@gwsetup_bp.route('/consang.htm')
def consang_htm():
    raise NotImplementedError(
        "Route /consang.htm (consang_htm) not implemented yet"
    )


@gwsetup_bp.route('/consg_ok.htm')
def consg_ok_htm():
    raise NotImplementedError(
        "Route /consg_ok.htm (consg_ok_htm) not implemented yet"
    )


@gwsetup_bp.route('/del_ok.htm')
def del_ok_htm():
    raise NotImplementedError(
        "Route /del_ok.htm (del_ok_htm) not implemented yet"
    )


@gwsetup_bp.route('/delete_1.htm')
def delete_1_htm():
    raise NotImplementedError(
        "Route /delete_1.htm (delete_1_htm) not implemented yet"
    )


@gwsetup_bp.route('/delete.htm')
def delete_htm():
    raise NotImplementedError(
        "Route /delete.htm (delete_htm) not implemented yet"
    )


@gwsetup_bp.route('/err_acc.htm')
def err_acc_htm():
    raise NotImplementedError(
        "Route /err_acc.htm (err_acc_htm) not implemented yet"
    )


@gwsetup_bp.route('/err_cnfl.htm')
def err_cnfl_htm():
    raise NotImplementedError(
        "Route /err_cnfl.htm (err_cnfl_htm) not implemented yet"
    )


@gwsetup_bp.route('/err_miss.htm')
def err_miss_htm():
    raise NotImplementedError(
        "Route /err_miss.htm (err_miss_htm) not implemented yet"
    )


@gwsetup_bp.route('/err_name.htm')
def err_name_htm():
    raise NotImplementedError(
        "Route /err_name.htm (err_name_htm) not implemented yet"
    )


@gwsetup_bp.route('/err_ndir.htm')
def err_ndir_htm():
    raise NotImplementedError(
        "Route /err_ndir.htm (err_ndir_htm) not implemented yet"
    )


@gwsetup_bp.route('/err_ngw.htm')
def err_ngw_htm():
    raise NotImplementedError(
        "Route /err_ngw.htm (err_ngw_htm) not implemented yet"
    )


@gwsetup_bp.route('/err_outd.htm')
def err_outd_htm():
    raise NotImplementedError(
        "Route /err_outd.htm (err_outd_htm) not implemented yet"
    )


@gwsetup_bp.route('/err_reco.htm')
def err_reco_htm():
    raise NotImplementedError(
        "Route /err_reco.htm (err_reco_htm) not implemented yet"
    )


@gwsetup_bp.route('/err_smdr.htm')
def err_smdr_htm():
    raise NotImplementedError(
        "Route /err_smdr.htm (err_smdr_htm) not implemented yet"
    )


@gwsetup_bp.route('/err_unkn.htm')
def err_unkn_htm():
    raise NotImplementedError(
        "Route /err_unkn.htm (err_unkn_htm) not implemented yet"
    )


@gwsetup_bp.route('/ged2gwd.htm')
def ged2gwd_htm():
    raise NotImplementedError(
        "Route /ged2gwd.htm (ged2gwd_htm) not implemented yet"
    )


@gwsetup_bp.route('/gw2gd_ok.htm')
def gw2gd_ok_htm():
    raise NotImplementedError(
        "Route /gw2gd_ok.htm (gw2gd_ok_htm) not implemented yet"
    )


@gwsetup_bp.route('/gwb2ged.htm')
def gwb2ged_htm():
    raise NotImplementedError(
        "Route /gwb2ged.htm (gwb2ged_htm) not implemented yet"
    )


@gwsetup_bp.route('/gwc.htm')
def gwc_htm():
    raise NotImplementedError(
        "Route /gwc.htm (gwc_htm) not implemented yet"
    )


@gwsetup_bp.route('/gwd_info.htm')
def gwd_info_htm():
    raise NotImplementedError(
        "Route /gwd_info.htm (gwd_info_htm) not implemented yet"
    )


@gwsetup_bp.route('/gwd_ok.htm')
def gwd_ok_htm():
    raise NotImplementedError(
        "Route /gwd_ok.htm (gwd_ok_htm) not implemented yet"
    )


@gwsetup_bp.route('/gwd.htm')
def gwd_htm():
    raise NotImplementedError(
        "Route /gwd.htm (gwd_htm) not implemented yet"
    )


@gwsetup_bp.route('/gwdiff_ok.htm')
def gwdiff_ok_htm():
    raise NotImplementedError(
        "Route /gwdiff_ok.htm (gwdiff_ok_htm) not implemented yet"
    )


@gwsetup_bp.route('/gwdiff.htm')
def gwdiff_htm():
    raise NotImplementedError(
        "Route /gwdiff.htm (gwdiff_htm) not implemented yet"
    )


@gwsetup_bp.route('/gwf_1.htm')
def gwf_1_htm():
    raise NotImplementedError(
        "Route /gwf_1.htm (gwf_1_htm) not implemented yet"
    )


@gwsetup_bp.route('/gwf_ok.htm')
def gwf_ok_htm():
    raise NotImplementedError(
        "Route /gwf_ok.htm (gwf_ok_htm) not implemented yet"
    )


@gwsetup_bp.route('/gwfix_ok.htm')
def gwfix_ok_htm():
    raise NotImplementedError(
        "Route /gwfix_ok.htm (gwfix_ok_htm) not implemented yet"
    )


@gwsetup_bp.route('/gwfix.htm')
def gwfix_htm():
    raise NotImplementedError(
        "Route /gwfix.htm (gwfix_htm) not implemented yet"
    )


@gwsetup_bp.route('/gwu_ok.htm')
def gwu_ok_htm():
    raise NotImplementedError(
        "Route /gwu_ok.htm (gwu_ok_htm) not implemented yet"
    )


@gwsetup_bp.route('/gwu.htm')
def gwu_htm():
    raise NotImplementedError(
        "Route /gwu.htm (gwu_htm) not implemented yet"
    )


@gwsetup_bp.route('/intro.htm')
def intro_htm():
    raise NotImplementedError(
        "Route /intro.htm (intro_htm) not implemented yet"
    )


@gwsetup_bp.route('/list.htm')
def list_htm():
    raise NotImplementedError(
        "Route /list.htm (list_htm) not implemented yet"
    )


@gwsetup_bp.route('/macros.htm')
def macros_htm():
    raise NotImplementedError(
        "Route /macros.htm (macros_htm) not implemented yet"
    )


@gwsetup_bp.route('/main.htm')
def main_htm():
    raise NotImplementedError(
        "Route /main.htm (main_htm) not implemented yet"
    )


@gwsetup_bp.route('/merge_1.htm')
def merge_1_htm():
    raise NotImplementedError(
        "Route /merge_1.htm (merge_1_htm) not implemented yet"
    )


@gwsetup_bp.route('/merge.htm')
def merge_htm():
    raise NotImplementedError(
        "Route /merge.htm (merge_htm) not implemented yet"
    )


@gwsetup_bp.route('/recover.htm')
def recover_htm():
    raise NotImplementedError(
        "Route /recover.htm (recover_htm) not implemented yet"
    )


@gwsetup_bp.route('/recover1.htm')
def recover1_htm():
    raise NotImplementedError(
        "Route /recover1.htm (recover1_htm) not implemented yet"
    )


@gwsetup_bp.route('/recover2.htm')
def recover2_htm():
    raise NotImplementedError(
        "Route /recover2.htm (recover2_htm) not implemented yet"
    )


@gwsetup_bp.route('/ren_ok.htm')
def ren_ok_htm():
    raise NotImplementedError(
        "Route /ren_ok.htm (ren_ok_htm) not implemented yet"
    )


@gwsetup_bp.route('/rename.htm')
def rename_htm():
    raise NotImplementedError(
        "Route /rename.htm (rename_htm) not implemented yet"
    )


@gwsetup_bp.route('/save.htm')
def save_htm():
    raise NotImplementedError(
        "Route /save.htm (save_htm) not implemented yet"
    )


@gwsetup_bp.route('/simple.htm')
def simple_htm():
    raise NotImplementedError(
        "Route /simple.htm (simple_htm) not implemented yet"
    )


@gwsetup_bp.route('/traces.htm')
def traces_htm():
    raise NotImplementedError(
        "Route /traces.htm (traces_htm) not implemented yet"
    )


@gwsetup_bp.route('/update_nldb_ok.htm')
def update_nldb_ok_htm():
    raise NotImplementedError(
        "Route /update_nldb_ok.htm (update_nldb_ok_htm) not implemented yet"
    )


@gwsetup_bp.route('/update_nldb.htm')
def update_nldb_htm():
    raise NotImplementedError(
        "Route /update_nldb.htm (update_nldb_htm) not implemented yet"
    )


@gwsetup_bp.route('/welcome.htm')
def welcome_htm():
    raise NotImplementedError(
        "Route /welcome.htm (welcome_htm) not implemented yet"
    )
