from .details import implem_gwd_details
from wserver.routes.fiefs import route_fiefs
from .homepage import route_homepage
from .search import route_search
from .add_family import implem_route_ADD_FAM
from .mod_individual import implem_route_MOD_IND
from ..routes.gwd_root_impl import implem_route_gwd_root
from .anm_impl import implem_route_ANM
from .titles import route_titles
from flask import Blueprint, request

gwd_bp = Blueprint('gwd', __name__, url_prefix='/gwd')

"""
GWD ROUTES MODULE - Explicit placeholder routes for legacy 'm' modes.
Handlers are explicit functions and currently raise NotImplementedError..
"""


@gwd_bp.route("<base>", methods=['GET', 'POST'])
def gwd_homepage(base: str):
    lang = request.args.get("lang", "en")
    previous_url = request.args.get("previous_url", None)
    return route_homepage(base, lang, previous_url)


@gwd_bp.route("<base>/search", methods=['GET', 'POST'])
def gwd_search(base: str):
    lang = request.args.get("lang", "en")
    sort = request.args.get("sort", None)
    on = request.args.get("on", None)
    surname = request.args.get("surname", None)
    firstname = request.args.get("firstname", None)
    previous_url = request.args.get("previous_url", None)
    return route_search(base, lang, sort, on, surname, firstname, previous_url)


@gwd_bp.route("<base>/titles", methods=['GET', 'POST'])
def gwd_titles(base: str):
    lang = request.args.get("lang", "en")
    title = request.args.get("title", None)
    fief = request.args.get("fief", None)
    previous_url = request.args.get("previous_url", None)
    return route_titles(base, lang, title, fief, previous_url)


@gwd_bp.route("<base>/fiefs", methods=['GET', 'POST'])
def gwd_fiefs(base: str):
    lang = request.args.get("lang", "en")
    previous_url = request.args.get("previous_url", None)
    return route_fiefs(base, lang, previous_url)


@gwd_bp.route('', methods=['GET', 'POST'], strict_slashes=False)
def gwd_root():
    return implem_route_gwd_root()


@gwd_bp.route('<base>/A/', methods=['GET', 'POST'])
def route_A(base):
    raise NotImplementedError("Route A not implemented yet")


@gwd_bp.route('<base>/details', methods=['GET', 'POST'], strict_slashes=False)
@gwd_bp.route('<base>/details?<lang>', methods=['GET', 'POST'])
def route_details(base, lang='en'):
    return implem_gwd_details(base, lang)


@gwd_bp.route('<base>/ADD_FAM/', methods=['GET', 'POST'], strict_slashes=False)
def route_ADD_FAM(base):
    lang = request.args.get('lang') or 'en'
    return implem_route_ADD_FAM(base, lang)


@gwd_bp.route('<base>/ADD_FAM_OK/', methods=['GET', 'POST'])
def route_ADD_FAM_OK(base):
    raise NotImplementedError("Route ADD_FAM_OK not implemented yet")


@gwd_bp.route('<base>/ADD_IND/', methods=['GET', 'POST'])
def route_ADD_IND(base):
    raise NotImplementedError("Route ADD_IND not implemented yet")


@gwd_bp.route('<base>/ADD_IND_OK/', methods=['GET', 'POST'])
def route_ADD_IND_OK(base):
    raise NotImplementedError("Route ADD_IND_OK not implemented yet")


@gwd_bp.route('<base>/ADD_PAR/', methods=['GET', 'POST'])
def route_ADD_PAR(base):
    raise NotImplementedError("Route ADD_PAR not implemented yet")


@gwd_bp.route('<base>/ADD_PAR_OK/', methods=['GET', 'POST'])
def route_ADD_PAR_OK(base):
    raise NotImplementedError("Route ADD_PAR_OK not implemented yet")


@gwd_bp.route('<base>/ANM/', methods=['GET', 'POST'])
def route_ANM(base):
    return implem_route_ANM(base)


@gwd_bp.route('<base>/AN/', methods=['GET', 'POST'])
def route_AN(base):
    raise NotImplementedError("Route AN not implemented yet")


@gwd_bp.route('<base>/AD/', methods=['GET', 'POST'])
def route_AD(base):
    raise NotImplementedError("Route AD not implemented yet")


@gwd_bp.route('<base>/AM/', methods=['GET', 'POST'])
def route_AM(base):
    raise NotImplementedError("Route AM not implemented yet")


@gwd_bp.route('<base>/AS/', methods=['GET', 'POST'])
def route_AS(base):
    raise NotImplementedError("Route AS not implemented yet")


@gwd_bp.route('<base>/AS_OK/', methods=['GET', 'POST'])
def route_AS_OK(base):
    raise NotImplementedError("Route AS_OK not implemented yet")


@gwd_bp.route('<base>/C/', methods=['GET', 'POST'])
def route_C(base):
    raise NotImplementedError("Route C not implemented yet")


@gwd_bp.route('<base>/CAL/', methods=['GET', 'POST'])
def route_CAL(base):
    raise NotImplementedError("Route CAL not implemented yet")


@gwd_bp.route('<base>/CHG_CHN/', methods=['GET', 'POST'])
def route_CHG_CHN(base):
    raise NotImplementedError("Route CHG_CHN not implemented yet")


@gwd_bp.route('<base>/CHG_CHN_OK/', methods=['GET', 'POST'])
def route_CHG_CHN_OK(base):
    raise NotImplementedError("Route CHG_CHN_OK not implemented yet")


@gwd_bp.route('<base>/CHG_EVT_IND_ORD/', methods=['GET', 'POST'])
def route_CHG_EVT_IND_ORD(base):
    raise NotImplementedError("Route CHG_EVT_IND_ORD not implemented yet")


@gwd_bp.route('<base>/CHG_EVT_IND_ORD_OK/', methods=['GET', 'POST'])
def route_CHG_EVT_IND_ORD_OK(base):
    raise NotImplementedError("Route CHG_EVT_IND_ORD_OK not implemented yet")


@gwd_bp.route('<base>/CHG_EVT_FAM_ORD/', methods=['GET', 'POST'])
def route_CHG_EVT_FAM_ORD(base):
    raise NotImplementedError("Route CHG_EVT_FAM_ORD not implemented yet")


@gwd_bp.route('<base>/CHG_EVT_FAM_ORD_OK/', methods=['GET', 'POST'])
def route_CHG_EVT_FAM_ORD_OK(base):
    raise NotImplementedError("Route CHG_EVT_FAM_ORD_OK not implemented yet")


@gwd_bp.route('<base>/CHG_FAM_ORD/', methods=['GET', 'POST'])
def route_CHG_FAM_ORD(base):
    raise NotImplementedError("Route CHG_FAM_ORD not implemented yet")


@gwd_bp.route('<base>/CHG_FAM_ORD_OK/', methods=['GET', 'POST'])
def route_CHG_FAM_ORD_OK(base):
    raise NotImplementedError("Route CHG_FAM_ORD_OK not implemented yet")


@gwd_bp.route('<base>/CONN_WIZ/', methods=['GET', 'POST'])
def route_CONN_WIZ(base):
    raise NotImplementedError("Route CONN_WIZ not implemented yet")


@gwd_bp.route('<base>/D/', methods=['GET', 'POST'])
def route_D(base):
    raise NotImplementedError("Route D not implemented yet")


@gwd_bp.route('<base>/DAG/', methods=['GET', 'POST'])
def route_DAG(base):
    raise NotImplementedError("Route DAG not implemented yet")


@gwd_bp.route('<base>/DEL_FAM/', methods=['GET', 'POST'])
def route_DEL_FAM(base):
    raise NotImplementedError("Route DEL_FAM not implemented yet")


@gwd_bp.route('<base>/DEL_FAM_OK/', methods=['GET', 'POST'])
def route_DEL_FAM_OK(base):
    raise NotImplementedError("Route DEL_FAM_OK not implemented yet")


@gwd_bp.route('<base>/DEL_IMAGE/', methods=['GET', 'POST'])
def route_DEL_IMAGE(base):
    raise NotImplementedError("Route DEL_IMAGE not implemented yet")


@gwd_bp.route('<base>/DEL_IMAGE_OK/', methods=['GET', 'POST'])
def route_DEL_IMAGE_OK(base):
    raise NotImplementedError("Route DEL_IMAGE_OK not implemented yet")


@gwd_bp.route('<base>/DEL_IMAGE_C_OK/', methods=['GET', 'POST'])
def route_DEL_IMAGE_C_OK(base):
    raise NotImplementedError("Route DEL_IMAGE_C_OK not implemented yet")


@gwd_bp.route('<base>/DEL_IND/', methods=['GET', 'POST'])
def route_DEL_IND(base):
    raise NotImplementedError("Route DEL_IND not implemented yet")


@gwd_bp.route('<base>/DEL_IND_OK/', methods=['GET', 'POST'])
def route_DEL_IND_OK(base):
    raise NotImplementedError("Route DEL_IND_OK not implemented yet")


@gwd_bp.route('<base>/DOC/', methods=['GET', 'POST'])
def route_DOC(base):
    raise NotImplementedError("Route DOC not implemented yet")


@gwd_bp.route('<base>/DOCH/', methods=['GET', 'POST'])
def route_DOCH(base):
    raise NotImplementedError("Route DOCH not implemented yet")


@gwd_bp.route('<base>/F/', methods=['GET', 'POST'])
def route_F(base):
    raise NotImplementedError("Route F not implemented yet")


@gwd_bp.route('<base>/H/', methods=['GET', 'POST'])
def route_H(base):
    raise NotImplementedError("Route H not implemented yet")


@gwd_bp.route('<base>/HIST/', methods=['GET', 'POST'])
def route_HIST(base):
    raise NotImplementedError("Route HIST not implemented yet")


@gwd_bp.route('<base>/HIST_CLEAN/', methods=['GET', 'POST'])
def route_HIST_CLEAN(base):
    raise NotImplementedError("Route HIST_CLEAN not implemented yet")


@gwd_bp.route('<base>/HIST_CLEAN_OK/', methods=['GET', 'POST'])
def route_HIST_CLEAN_OK(base):
    raise NotImplementedError("Route HIST_CLEAN_OK not implemented yet")


@gwd_bp.route('<base>/HIST_DIFF/', methods=['GET', 'POST'])
def route_HIST_DIFF(base):
    raise NotImplementedError("Route HIST_DIFF not implemented yet")


@gwd_bp.route('<base>/HIST_SEARCH/', methods=['GET', 'POST'])
def route_HIST_SEARCH(base):
    raise NotImplementedError("Route HIST_SEARCH not implemented yet")


@gwd_bp.route('<base>/IM_C/', methods=['GET', 'POST'])
def route_IM_C(base):
    raise NotImplementedError("Route IM_C not implemented yet")


@gwd_bp.route('<base>/IM_C_S/', methods=['GET', 'POST'])
def route_IM_C_S(base):
    raise NotImplementedError("Route IM_C_S not implemented yet")


@gwd_bp.route('<base>/IM/', methods=['GET', 'POST'])
def route_IM(base):
    raise NotImplementedError("Route IM not implemented yet")


@gwd_bp.route('<base>/IMH/', methods=['GET', 'POST'])
def route_IMH(base):
    raise NotImplementedError("Route IMH not implemented yet")


@gwd_bp.route('<base>/INV_FAM/', methods=['GET', 'POST'])
def route_INV_FAM(base):
    raise NotImplementedError("Route INV_FAM not implemented yet")


@gwd_bp.route('<base>/INV_FAM_OK/', methods=['GET', 'POST'])
def route_INV_FAM_OK(base):
    raise NotImplementedError("Route INV_FAM_OK not implemented yet")


@gwd_bp.route('<base>/KILL_ANC/', methods=['GET', 'POST'])
def route_KILL_ANC(base):
    raise NotImplementedError("Route KILL_ANC not implemented yet")


@gwd_bp.route('<base>/L/', methods=['GET', 'POST'])
def route_L(base):
    raise NotImplementedError("Route L not implemented yet")


@gwd_bp.route('<base>/LB/', methods=['GET', 'POST'])
def route_LB(base):
    raise NotImplementedError("Route LB not implemented yet")


@gwd_bp.route('<base>/LD/', methods=['GET', 'POST'])
def route_LD(base):
    raise NotImplementedError("Route LD not implemented yet")


@gwd_bp.route('<base>/LINKED/', methods=['GET', 'POST'])
def route_LINKED(base):
    raise NotImplementedError("Route LINKED not implemented yet")


@gwd_bp.route('<base>/LL/', methods=['GET', 'POST'])
def route_LL(base):
    raise NotImplementedError("Route LL not implemented yet")


@gwd_bp.route('<base>/LM/', methods=['GET', 'POST'])
def route_LM(base):
    raise NotImplementedError("Route LM not implemented yet")


@gwd_bp.route('<base>/MRG/', methods=['GET', 'POST'])
def route_MRG(base):
    raise NotImplementedError("Route MRG not implemented yet")


@gwd_bp.route('<base>/MOD_FAM/', methods=['GET', 'POST'])
@gwd_bp.route('<base>/MOD_FAM/<lang>', methods=['GET', 'POST'])
def route_MOD_FAM(base, lang='en'):
    raise NotImplementedError("Route MOD_FAM not implemented yet")


@gwd_bp.route('<base>/modify_individual', methods=['GET', 'POST'])
def route_MOD_IND(base):
    id = request.args.get('id', type=int)
    lang = request.args.get('lang', 'en')
    if id is None:
        return "Missing 'id' parameter", 400
    return implem_route_MOD_IND(base, id, lang)


@gwd_bp.route('<base>/MRG_DUP/', methods=['GET', 'POST'])
def route_MRG_DUP(base):
    raise NotImplementedError("Route MRG_DUP not implemented yet")


@gwd_bp.route('<base>/MRG_DUP_IND_Y_N/', methods=['GET', 'POST'])
def route_MRG_DUP_IND_Y_N(base):
    raise NotImplementedError("Route MRG_DUP_IND_Y_N not implemented yet")


@gwd_bp.route('<base>/MRG_DUP_FAM_Y_N/', methods=['GET', 'POST'])
def route_MRG_DUP_FAM_Y_N(base):
    raise NotImplementedError("Route MRG_DUP_FAM_Y_N not implemented yet")


@gwd_bp.route('<base>/MRG_FAM/', methods=['GET', 'POST'])
def route_MRG_FAM(base):
    raise NotImplementedError("Route MRG_FAM not implemented yet")


@gwd_bp.route('<base>/MRG_FAM_OK/', methods=['GET', 'POST'])
def route_MRG_FAM_OK(base):
    raise NotImplementedError("Route MRG_FAM_OK not implemented yet")


@gwd_bp.route('<base>/MRG_MOD_FAM_OK/', methods=['GET', 'POST'])
def route_MRG_MOD_FAM_OK(base):
    raise NotImplementedError("Route MRG_MOD_FAM_OK not implemented yet")


@gwd_bp.route('<base>/MRG_IND/', methods=['GET', 'POST'])
def route_MRG_IND(base):
    raise NotImplementedError("Route MRG_IND not implemented yet")


@gwd_bp.route('<base>/MRG_IND_OK/', methods=['GET', 'POST'])
def route_MRG_IND_OK(base):
    raise NotImplementedError("Route MRG_IND_OK not implemented yet")


@gwd_bp.route('<base>/MRG_MOD_IND_OK/', methods=['GET', 'POST'])
def route_MRG_MOD_IND_OK(base):
    raise NotImplementedError("Route MRG_MOD_IND_OK not implemented yet")


@gwd_bp.route('<base>/N/', methods=['GET', 'POST'])
def route_N(base):
    raise NotImplementedError("Route N not implemented yet")


@gwd_bp.route('<base>/NG/', methods=['GET', 'POST'])
def route_NG(base):
    raise NotImplementedError("Route NG not implemented yet")


@gwd_bp.route('<base>/NOTES/', methods=['GET', 'POST'])
def route_NOTES(base):
    raise NotImplementedError("Route NOTES not implemented yet")


@gwd_bp.route('<base>/OA/', methods=['GET', 'POST'])
def route_OA(base):
    raise NotImplementedError("Route OA not implemented yet")


@gwd_bp.route('<base>/OE/', methods=['GET', 'POST'])
def route_OE(base):
    raise NotImplementedError("Route OE not implemented yet")


@gwd_bp.route('<base>/P/', methods=['GET', 'POST'])
def route_P(base):
    raise NotImplementedError("Route P not implemented yet")


@gwd_bp.route('<base>/PERSO/', methods=['GET', 'POST'])
def route_PERSO(base):
    raise NotImplementedError("Route PERSO not implemented yet")


@gwd_bp.route('<base>/POP_PYR/', methods=['GET', 'POST'])
def route_POP_PYR(base):
    raise NotImplementedError("Route POP_PYR not implemented yet")


@gwd_bp.route('<base>/PS/', methods=['GET', 'POST'])
def route_PS(base):
    raise NotImplementedError("Route PS not implemented yet")


@gwd_bp.route('<base>/PPS/', methods=['GET', 'POST'])
def route_PPS(base):
    raise NotImplementedError("Route PPS not implemented yet")


@gwd_bp.route('<base>/R/', methods=['GET', 'POST'])
def route_R(base):
    raise NotImplementedError("Route R not implemented yet")


@gwd_bp.route('<base>/REFRESH/', methods=['GET', 'POST'])
def route_REFRESH(base):
    raise NotImplementedError("Route REFRESH not implemented yet")


@gwd_bp.route('<base>/REQUEST/', methods=['GET', 'POST'])
def route_REQUEST(base):
    raise NotImplementedError("Route REQUEST not implemented yet")


@gwd_bp.route('<base>/RESET_IMAGE_C_OK/', methods=['GET', 'POST'])
def route_RESET_IMAGE_C_OK(base):
    raise NotImplementedError("Route RESET_IMAGE_C_OK not implemented yet")


@gwd_bp.route('<base>/RL/', methods=['GET', 'POST'])
def route_RL(base):
    raise NotImplementedError("Route RL not implemented yet")


@gwd_bp.route('<base>/RLM/', methods=['GET', 'POST'])
def route_RLM(base):
    raise NotImplementedError("Route RLM not implemented yet")


@gwd_bp.route('<base>/S/', methods=['GET', 'POST'])
def route_S(base):
    raise NotImplementedError("Route S not implemented yet")


@gwd_bp.route('<base>/SND_IMAGE/', methods=['GET', 'POST'])
def route_SND_IMAGE(base):
    raise NotImplementedError("Route SND_IMAGE not implemented yet")


@gwd_bp.route('<base>/SND_IMAGE_OK/', methods=['GET', 'POST'])
def route_SND_IMAGE_OK(base):
    raise NotImplementedError("Route SND_IMAGE_OK not implemented yet")


@gwd_bp.route('<base>/SND_IMAGE_C/', methods=['GET', 'POST'])
def route_SND_IMAGE_C(base):
    raise NotImplementedError("Route SND_IMAGE_C not implemented yet")


@gwd_bp.route('<base>/SND_IMAGE_C_OK/', methods=['GET', 'POST'])
def route_SND_IMAGE_C_OK(base):
    raise NotImplementedError("Route SND_IMAGE_C_OK not implemented yet")


@gwd_bp.route('<base>/SRC/', methods=['GET', 'POST'])
def route_SRC(base):
    raise NotImplementedError("Route SRC not implemented yet")


@gwd_bp.route('<base>/STAT/', methods=['GET', 'POST'])
def route_STAT(base):
    raise NotImplementedError("Route STAT not implemented yet")


@gwd_bp.route('<base>/CHANGE_WIZ_VIS/', methods=['GET', 'POST'])
def route_CHANGE_WIZ_VIS(base):
    raise NotImplementedError("Route CHANGE_WIZ_VIS not implemented yet")


@gwd_bp.route('<base>/TP/', methods=['GET', 'POST'])
def route_TP(base):
    raise NotImplementedError("Route TP not implemented yet")


@gwd_bp.route('<base>/TT/', methods=['GET', 'POST'])
def route_TT(base):
    raise NotImplementedError("Route TT not implemented yet")


@gwd_bp.route('<base>/U/', methods=['GET', 'POST'])
def route_U(base):
    raise NotImplementedError("Route U not implemented yet")


@gwd_bp.route('<base>/VIEW_WIZNOTES/', methods=['GET', 'POST'])
def route_VIEW_WIZNOTES(base):
    raise NotImplementedError("Route VIEW_WIZNOTES not implemented yet")


@gwd_bp.route('<base>/WIZNOTES/', methods=['GET', 'POST'])
def route_WIZNOTES(base):
    raise NotImplementedError("Route WIZNOTES not implemented yet")


@gwd_bp.route('<base>/WIZNOTES_SEARCH/', methods=['GET', 'POST'])
def route_WIZNOTES_SEARCH(base):
    raise NotImplementedError("Route WIZNOTES_SEARCH not implemented yet")
