from flask import Blueprint

gwd_bp = Blueprint('gwd', __name__)
"""
GWD ROUTES MODULE - Explicit placeholder routes for legacy 'm' modes.

Each mode from legacy/bin/gwd/request.ml is exposed as two Flask routes:
 - /gwd/<base>/<MODE>/
 - /gwd/<base>/<MODE>/<lang>
Handlers are explicit functions and currently raise NotImplementedError..
"""

# DEFAULT / ROOT (already present)


@gwd_bp.route('/gwd', defaults={'lang': 'en'},
              methods=['GET', 'POST'], strict_slashes=False)
@gwd_bp.route('/gwd/<lang>', methods=['GET', 'POST'])
def gwd_root(lang):
    raise NotImplementedError(
        f"GWD root route not implemented yet (lang={lang})")

# BASE-ONLY (no mode) - corresponds to empty "" mode


@gwd_bp.route('/gwd/<base>/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/<lang>', methods=['GET', 'POST'])
def gwd_base_only(base, lang='en'):
    raise NotImplementedError(
        f"Route base={base}, no action yet (lang={lang})")

# Explicit action routes (one function per legacy "m" value)


@gwd_bp.route('/gwd/<base>/A/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/A/<lang>', methods=['GET', 'POST'])
def route_A(base, lang='en'):
    raise NotImplementedError("Route A not implemented yet")


@gwd_bp.route('/gwd/<base>/ADD_FAM/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/ADD_FAM/<lang>', methods=['GET', 'POST'])
def route_ADD_FAM(base, lang='en'):
    raise NotImplementedError("Route ADD_FAM not implemented yet")


@gwd_bp.route('/gwd/<base>/ADD_FAM_OK/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/ADD_FAM_OK/<lang>', methods=['GET', 'POST'])
def route_ADD_FAM_OK(base, lang='en'):
    raise NotImplementedError("Route ADD_FAM_OK not implemented yet")


@gwd_bp.route('/gwd/<base>/ADD_IND/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/ADD_IND/<lang>', methods=['GET', 'POST'])
def route_ADD_IND(base, lang='en'):
    raise NotImplementedError("Route ADD_IND not implemented yet")


@gwd_bp.route('/gwd/<base>/ADD_IND_OK/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/ADD_IND_OK/<lang>', methods=['GET', 'POST'])
def route_ADD_IND_OK(base, lang='en'):
    raise NotImplementedError("Route ADD_IND_OK not implemented yet")


@gwd_bp.route('/gwd/<base>/ADD_PAR/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/ADD_PAR/<lang>', methods=['GET', 'POST'])
def route_ADD_PAR(base, lang='en'):
    raise NotImplementedError("Route ADD_PAR not implemented yet")


@gwd_bp.route('/gwd/<base>/ADD_PAR_OK/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/ADD_PAR_OK/<lang>', methods=['GET', 'POST'])
def route_ADD_PAR_OK(base, lang='en'):
    raise NotImplementedError("Route ADD_PAR_OK not implemented yet")


@gwd_bp.route('/gwd/<base>/ANM/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/ANM/<lang>', methods=['GET', 'POST'])
def route_ANM(base, lang='en'):
    raise NotImplementedError("Route ANM not implemented yet")


@gwd_bp.route('/gwd/<base>/AN/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/AN/<lang>', methods=['GET', 'POST'])
def route_AN(base, lang='en'):
    raise NotImplementedError("Route AN not implemented yet")


@gwd_bp.route('/gwd/<base>/AD/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/AD/<lang>', methods=['GET', 'POST'])
def route_AD(base, lang='en'):
    raise NotImplementedError("Route AD not implemented yet")


@gwd_bp.route('/gwd/<base>/AM/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/AM/<lang>', methods=['GET', 'POST'])
def route_AM(base, lang='en'):
    raise NotImplementedError("Route AM not implemented yet")


@gwd_bp.route('/gwd/<base>/AS/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/AS/<lang>', methods=['GET', 'POST'])
def route_AS(base, lang='en'):
    raise NotImplementedError("Route AS not implemented yet")


@gwd_bp.route('/gwd/<base>/AS_OK/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/AS_OK/<lang>', methods=['GET', 'POST'])
def route_AS_OK(base, lang='en'):
    raise NotImplementedError("Route AS_OK not implemented yet")


@gwd_bp.route('/gwd/<base>/C/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/C/<lang>', methods=['GET', 'POST'])
def route_C(base, lang='en'):
    raise NotImplementedError("Route C not implemented yet")


@gwd_bp.route('/gwd/<base>/CAL/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/CAL/<lang>', methods=['GET', 'POST'])
def route_CAL(base, lang='en'):
    raise NotImplementedError("Route CAL not implemented yet")


@gwd_bp.route('/gwd/<base>/CHG_CHN/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/CHG_CHN/<lang>', methods=['GET', 'POST'])
def route_CHG_CHN(base, lang='en'):
    raise NotImplementedError("Route CHG_CHN not implemented yet")


@gwd_bp.route('/gwd/<base>/CHG_CHN_OK/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/CHG_CHN_OK/<lang>', methods=['GET', 'POST'])
def route_CHG_CHN_OK(base, lang='en'):
    raise NotImplementedError("Route CHG_CHN_OK not implemented yet")


@gwd_bp.route('/gwd/<base>/CHG_EVT_IND_ORD/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/CHG_EVT_IND_ORD/<lang>', methods=['GET', 'POST'])
def route_CHG_EVT_IND_ORD(base, lang='en'):
    raise NotImplementedError("Route CHG_EVT_IND_ORD not implemented yet")


@gwd_bp.route('/gwd/<base>/CHG_EVT_IND_ORD_OK/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/CHG_EVT_IND_ORD_OK/<lang>', methods=['GET', 'POST'])
def route_CHG_EVT_IND_ORD_OK(base, lang='en'):
    raise NotImplementedError("Route CHG_EVT_IND_ORD_OK not implemented yet")


@gwd_bp.route('/gwd/<base>/CHG_EVT_FAM_ORD/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/CHG_EVT_FAM_ORD/<lang>', methods=['GET', 'POST'])
def route_CHG_EVT_FAM_ORD(base, lang='en'):
    raise NotImplementedError("Route CHG_EVT_FAM_ORD not implemented yet")


@gwd_bp.route('/gwd/<base>/CHG_EVT_FAM_ORD_OK/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/CHG_EVT_FAM_ORD_OK/<lang>', methods=['GET', 'POST'])
def route_CHG_EVT_FAM_ORD_OK(base, lang='en'):
    raise NotImplementedError("Route CHG_EVT_FAM_ORD_OK not implemented yet")


@gwd_bp.route('/gwd/<base>/CHG_FAM_ORD/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/CHG_FAM_ORD/<lang>', methods=['GET', 'POST'])
def route_CHG_FAM_ORD(base, lang='en'):
    raise NotImplementedError("Route CHG_FAM_ORD not implemented yet")


@gwd_bp.route('/gwd/<base>/CHG_FAM_ORD_OK/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/CHG_FAM_ORD_OK/<lang>', methods=['GET', 'POST'])
def route_CHG_FAM_ORD_OK(base, lang='en'):
    raise NotImplementedError("Route CHG_FAM_ORD_OK not implemented yet")


@gwd_bp.route('/gwd/<base>/CONN_WIZ/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/CONN_WIZ/<lang>', methods=['GET', 'POST'])
def route_CONN_WIZ(base, lang='en'):
    raise NotImplementedError("Route CONN_WIZ not implemented yet")


@gwd_bp.route('/gwd/<base>/D/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/D/<lang>', methods=['GET', 'POST'])
def route_D(base, lang='en'):
    raise NotImplementedError("Route D not implemented yet")


@gwd_bp.route('/gwd/<base>/DAG/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/DAG/<lang>', methods=['GET', 'POST'])
def route_DAG(base, lang='en'):
    raise NotImplementedError("Route DAG not implemented yet")


@gwd_bp.route('/gwd/<base>/DEL_FAM/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/DEL_FAM/<lang>', methods=['GET', 'POST'])
def route_DEL_FAM(base, lang='en'):
    raise NotImplementedError("Route DEL_FAM not implemented yet")


@gwd_bp.route('/gwd/<base>/DEL_FAM_OK/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/DEL_FAM_OK/<lang>', methods=['GET', 'POST'])
def route_DEL_FAM_OK(base, lang='en'):
    raise NotImplementedError("Route DEL_FAM_OK not implemented yet")


@gwd_bp.route('/gwd/<base>/DEL_IMAGE/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/DEL_IMAGE/<lang>', methods=['GET', 'POST'])
def route_DEL_IMAGE(base, lang='en'):
    raise NotImplementedError("Route DEL_IMAGE not implemented yet")


@gwd_bp.route('/gwd/<base>/DEL_IMAGE_OK/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/DEL_IMAGE_OK/<lang>', methods=['GET', 'POST'])
def route_DEL_IMAGE_OK(base, lang='en'):
    raise NotImplementedError("Route DEL_IMAGE_OK not implemented yet")


@gwd_bp.route('/gwd/<base>/DEL_IMAGE_C_OK/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/DEL_IMAGE_C_OK/<lang>', methods=['GET', 'POST'])
def route_DEL_IMAGE_C_OK(base, lang='en'):
    raise NotImplementedError("Route DEL_IMAGE_C_OK not implemented yet")


@gwd_bp.route('/gwd/<base>/DEL_IND/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/DEL_IND/<lang>', methods=['GET', 'POST'])
def route_DEL_IND(base, lang='en'):
    raise NotImplementedError("Route DEL_IND not implemented yet")


@gwd_bp.route('/gwd/<base>/DEL_IND_OK/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/DEL_IND_OK/<lang>', methods=['GET', 'POST'])
def route_DEL_IND_OK(base, lang='en'):
    raise NotImplementedError("Route DEL_IND_OK not implemented yet")


@gwd_bp.route('/gwd/<base>/DOC/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/DOC/<lang>', methods=['GET', 'POST'])
def route_DOC(base, lang='en'):
    raise NotImplementedError("Route DOC not implemented yet")


@gwd_bp.route('/gwd/<base>/DOCH/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/DOCH/<lang>', methods=['GET', 'POST'])
def route_DOCH(base, lang='en'):
    raise NotImplementedError("Route DOCH not implemented yet")


@gwd_bp.route('/gwd/<base>/F/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/F/<lang>', methods=['GET', 'POST'])
def route_F(base, lang='en'):
    raise NotImplementedError("Route F not implemented yet")


@gwd_bp.route('/gwd/<base>/H/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/H/<lang>', methods=['GET', 'POST'])
def route_H(base, lang='en'):
    raise NotImplementedError("Route H not implemented yet")


@gwd_bp.route('/gwd/<base>/HIST/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/HIST/<lang>', methods=['GET', 'POST'])
def route_HIST(base, lang='en'):
    raise NotImplementedError("Route HIST not implemented yet")


@gwd_bp.route('/gwd/<base>/HIST_CLEAN/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/HIST_CLEAN/<lang>', methods=['GET', 'POST'])
def route_HIST_CLEAN(base, lang='en'):
    raise NotImplementedError("Route HIST_CLEAN not implemented yet")


@gwd_bp.route('/gwd/<base>/HIST_CLEAN_OK/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/HIST_CLEAN_OK/<lang>', methods=['GET', 'POST'])
def route_HIST_CLEAN_OK(base, lang='en'):
    raise NotImplementedError("Route HIST_CLEAN_OK not implemented yet")


@gwd_bp.route('/gwd/<base>/HIST_DIFF/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/HIST_DIFF/<lang>', methods=['GET', 'POST'])
def route_HIST_DIFF(base, lang='en'):
    raise NotImplementedError("Route HIST_DIFF not implemented yet")


@gwd_bp.route('/gwd/<base>/HIST_SEARCH/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/HIST_SEARCH/<lang>', methods=['GET', 'POST'])
def route_HIST_SEARCH(base, lang='en'):
    raise NotImplementedError("Route HIST_SEARCH not implemented yet")


@gwd_bp.route('/gwd/<base>/IM_C/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/IM_C/<lang>', methods=['GET', 'POST'])
def route_IM_C(base, lang='en'):
    raise NotImplementedError("Route IM_C not implemented yet")


@gwd_bp.route('/gwd/<base>/IM_C_S/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/IM_C_S/<lang>', methods=['GET', 'POST'])
def route_IM_C_S(base, lang='en'):
    raise NotImplementedError("Route IM_C_S not implemented yet")


@gwd_bp.route('/gwd/<base>/IM/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/IM/<lang>', methods=['GET', 'POST'])
def route_IM(base, lang='en'):
    raise NotImplementedError("Route IM not implemented yet")


@gwd_bp.route('/gwd/<base>/IMH/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/IMH/<lang>', methods=['GET', 'POST'])
def route_IMH(base, lang='en'):
    raise NotImplementedError("Route IMH not implemented yet")


@gwd_bp.route('/gwd/<base>/INV_FAM/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/INV_FAM/<lang>', methods=['GET', 'POST'])
def route_INV_FAM(base, lang='en'):
    raise NotImplementedError("Route INV_FAM not implemented yet")


@gwd_bp.route('/gwd/<base>/INV_FAM_OK/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/INV_FAM_OK/<lang>', methods=['GET', 'POST'])
def route_INV_FAM_OK(base, lang='en'):
    raise NotImplementedError("Route INV_FAM_OK not implemented yet")


@gwd_bp.route('/gwd/<base>/KILL_ANC/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/KILL_ANC/<lang>', methods=['GET', 'POST'])
def route_KILL_ANC(base, lang='en'):
    raise NotImplementedError("Route KILL_ANC not implemented yet")


@gwd_bp.route('/gwd/<base>/L/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/L/<lang>', methods=['GET', 'POST'])
def route_L(base, lang='en'):
    raise NotImplementedError("Route L not implemented yet")


@gwd_bp.route('/gwd/<base>/LB/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/LB/<lang>', methods=['GET', 'POST'])
def route_LB(base, lang='en'):
    raise NotImplementedError("Route LB not implemented yet")


@gwd_bp.route('/gwd/<base>/LD/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/LD/<lang>', methods=['GET', 'POST'])
def route_LD(base, lang='en'):
    raise NotImplementedError("Route LD not implemented yet")


@gwd_bp.route('/gwd/<base>/LINKED/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/LINKED/<lang>', methods=['GET', 'POST'])
def route_LINKED(base, lang='en'):
    raise NotImplementedError("Route LINKED not implemented yet")


@gwd_bp.route('/gwd/<base>/LL/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/LL/<lang>', methods=['GET', 'POST'])
def route_LL(base, lang='en'):
    raise NotImplementedError("Route LL not implemented yet")


@gwd_bp.route('/gwd/<base>/LM/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/LM/<lang>', methods=['GET', 'POST'])
def route_LM(base, lang='en'):
    raise NotImplementedError("Route LM not implemented yet")


@gwd_bp.route('/gwd/<base>/MRG/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/MRG/<lang>', methods=['GET', 'POST'])
def route_MRG(base, lang='en'):
    raise NotImplementedError("Route MRG not implemented yet")


@gwd_bp.route('/gwd/<base>/MRG_DUP/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/MRG_DUP/<lang>', methods=['GET', 'POST'])
def route_MRG_DUP(base, lang='en'):
    raise NotImplementedError("Route MRG_DUP not implemented yet")


@gwd_bp.route('/gwd/<base>/MRG_DUP_IND_Y_N/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/MRG_DUP_IND_Y_N/<lang>', methods=['GET', 'POST'])
def route_MRG_DUP_IND_Y_N(base, lang='en'):
    raise NotImplementedError("Route MRG_DUP_IND_Y_N not implemented yet")


@gwd_bp.route('/gwd/<base>/MRG_DUP_FAM_Y_N/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/MRG_DUP_FAM_Y_N/<lang>', methods=['GET', 'POST'])
def route_MRG_DUP_FAM_Y_N(base, lang='en'):
    raise NotImplementedError("Route MRG_DUP_FAM_Y_N not implemented yet")


@gwd_bp.route('/gwd/<base>/MRG_FAM/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/MRG_FAM/<lang>', methods=['GET', 'POST'])
def route_MRG_FAM(base, lang='en'):
    raise NotImplementedError("Route MRG_FAM not implemented yet")


@gwd_bp.route('/gwd/<base>/MRG_FAM_OK/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/MRG_FAM_OK/<lang>', methods=['GET', 'POST'])
def route_MRG_FAM_OK(base, lang='en'):
    raise NotImplementedError("Route MRG_FAM_OK not implemented yet")


@gwd_bp.route('/gwd/<base>/MRG_MOD_FAM_OK/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/MRG_MOD_FAM_OK/<lang>', methods=['GET', 'POST'])
def route_MRG_MOD_FAM_OK(base, lang='en'):
    raise NotImplementedError("Route MRG_MOD_FAM_OK not implemented yet")


@gwd_bp.route('/gwd/<base>/MRG_IND/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/MRG_IND/<lang>', methods=['GET', 'POST'])
def route_MRG_IND(base, lang='en'):
    raise NotImplementedError("Route MRG_IND not implemented yet")


@gwd_bp.route('/gwd/<base>/MRG_IND_OK/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/MRG_IND_OK/<lang>', methods=['GET', 'POST'])
def route_MRG_IND_OK(base, lang='en'):
    raise NotImplementedError("Route MRG_IND_OK not implemented yet")


@gwd_bp.route('/gwd/<base>/MRG_MOD_IND_OK/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/MRG_MOD_IND_OK/<lang>', methods=['GET', 'POST'])
def route_MRG_MOD_IND_OK(base, lang='en'):
    raise NotImplementedError("Route MRG_MOD_IND_OK not implemented yet")


@gwd_bp.route('/gwd/<base>/N/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/N/<lang>', methods=['GET', 'POST'])
def route_N(base, lang='en'):
    raise NotImplementedError("Route N not implemented yet")


@gwd_bp.route('/gwd/<base>/NG/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/NG/<lang>', methods=['GET', 'POST'])
def route_NG(base, lang='en'):
    raise NotImplementedError("Route NG not implemented yet")


@gwd_bp.route('/gwd/<base>/NOTES/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/NOTES/<lang>', methods=['GET', 'POST'])
def route_NOTES(base, lang='en'):
    raise NotImplementedError("Route NOTES not implemented yet")


@gwd_bp.route('/gwd/<base>/OA/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/OA/<lang>', methods=['GET', 'POST'])
def route_OA(base, lang='en'):
    raise NotImplementedError("Route OA not implemented yet")


@gwd_bp.route('/gwd/<base>/OE/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/OE/<lang>', methods=['GET', 'POST'])
def route_OE(base, lang='en'):
    raise NotImplementedError("Route OE not implemented yet")


@gwd_bp.route('/gwd/<base>/P/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/P/<lang>', methods=['GET', 'POST'])
def route_P(base, lang='en'):
    raise NotImplementedError("Route P not implemented yet")


@gwd_bp.route('/gwd/<base>/PERSO/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/PERSO/<lang>', methods=['GET', 'POST'])
def route_PERSO(base, lang='en'):
    raise NotImplementedError("Route PERSO not implemented yet")


@gwd_bp.route('/gwd/<base>/POP_PYR/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/POP_PYR/<lang>', methods=['GET', 'POST'])
def route_POP_PYR(base, lang='en'):
    raise NotImplementedError("Route POP_PYR not implemented yet")


@gwd_bp.route('/gwd/<base>/PS/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/PS/<lang>', methods=['GET', 'POST'])
def route_PS(base, lang='en'):
    raise NotImplementedError("Route PS not implemented yet")


@gwd_bp.route('/gwd/<base>/PPS/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/PPS/<lang>', methods=['GET', 'POST'])
def route_PPS(base, lang='en'):
    raise NotImplementedError("Route PPS not implemented yet")


@gwd_bp.route('/gwd/<base>/R/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/R/<lang>', methods=['GET', 'POST'])
def route_R(base, lang='en'):
    raise NotImplementedError("Route R not implemented yet")


@gwd_bp.route('/gwd/<base>/REFRESH/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/REFRESH/<lang>', methods=['GET', 'POST'])
def route_REFRESH(base, lang='en'):
    raise NotImplementedError("Route REFRESH not implemented yet")


@gwd_bp.route('/gwd/<base>/REQUEST/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/REQUEST/<lang>', methods=['GET', 'POST'])
def route_REQUEST(base, lang='en'):
    raise NotImplementedError("Route REQUEST not implemented yet")


@gwd_bp.route('/gwd/<base>/RESET_IMAGE_C_OK/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/RESET_IMAGE_C_OK/<lang>', methods=['GET', 'POST'])
def route_RESET_IMAGE_C_OK(base, lang='en'):
    raise NotImplementedError("Route RESET_IMAGE_C_OK not implemented yet")


@gwd_bp.route('/gwd/<base>/RL/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/RL/<lang>', methods=['GET', 'POST'])
def route_RL(base, lang='en'):
    raise NotImplementedError("Route RL not implemented yet")


@gwd_bp.route('/gwd/<base>/RLM/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/RLM/<lang>', methods=['GET', 'POST'])
def route_RLM(base, lang='en'):
    raise NotImplementedError("Route RLM not implemented yet")


@gwd_bp.route('/gwd/<base>/S/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/S/<lang>', methods=['GET', 'POST'])
def route_S(base, lang='en'):
    raise NotImplementedError("Route S not implemented yet")


@gwd_bp.route('/gwd/<base>/SND_IMAGE/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/SND_IMAGE/<lang>', methods=['GET', 'POST'])
def route_SND_IMAGE(base, lang='en'):
    raise NotImplementedError("Route SND_IMAGE not implemented yet")


@gwd_bp.route('/gwd/<base>/SND_IMAGE_OK/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/SND_IMAGE_OK/<lang>', methods=['GET', 'POST'])
def route_SND_IMAGE_OK(base, lang='en'):
    raise NotImplementedError("Route SND_IMAGE_OK not implemented yet")


@gwd_bp.route('/gwd/<base>/SND_IMAGE_C/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/SND_IMAGE_C/<lang>', methods=['GET', 'POST'])
def route_SND_IMAGE_C(base, lang='en'):
    raise NotImplementedError("Route SND_IMAGE_C not implemented yet")


@gwd_bp.route('/gwd/<base>/SND_IMAGE_C_OK/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/SND_IMAGE_C_OK/<lang>', methods=['GET', 'POST'])
def route_SND_IMAGE_C_OK(base, lang='en'):
    raise NotImplementedError("Route SND_IMAGE_C_OK not implemented yet")


@gwd_bp.route('/gwd/<base>/SRC/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/SRC/<lang>', methods=['GET', 'POST'])
def route_SRC(base, lang='en'):
    raise NotImplementedError("Route SRC not implemented yet")


@gwd_bp.route('/gwd/<base>/STAT/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/STAT/<lang>', methods=['GET', 'POST'])
def route_STAT(base, lang='en'):
    raise NotImplementedError("Route STAT not implemented yet")


@gwd_bp.route('/gwd/<base>/CHANGE_WIZ_VIS/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/CHANGE_WIZ_VIS/<lang>', methods=['GET', 'POST'])
def route_CHANGE_WIZ_VIS(base, lang='en'):
    raise NotImplementedError("Route CHANGE_WIZ_VIS not implemented yet")


@gwd_bp.route('/gwd/<base>/TP/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/TP/<lang>', methods=['GET', 'POST'])
def route_TP(base, lang='en'):
    raise NotImplementedError("Route TP not implemented yet")


@gwd_bp.route('/gwd/<base>/TT/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/TT/<lang>', methods=['GET', 'POST'])
def route_TT(base, lang='en'):
    raise NotImplementedError("Route TT not implemented yet")


@gwd_bp.route('/gwd/<base>/U/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/U/<lang>', methods=['GET', 'POST'])
def route_U(base, lang='en'):
    raise NotImplementedError("Route U not implemented yet")


@gwd_bp.route('/gwd/<base>/VIEW_WIZNOTES/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/VIEW_WIZNOTES/<lang>', methods=['GET', 'POST'])
def route_VIEW_WIZNOTES(base, lang='en'):
    raise NotImplementedError("Route VIEW_WIZNOTES not implemented yet")


@gwd_bp.route('/gwd/<base>/WIZNOTES/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/WIZNOTES/<lang>', methods=['GET', 'POST'])
def route_WIZNOTES(base, lang='en'):
    raise NotImplementedError("Route WIZNOTES not implemented yet")


@gwd_bp.route('/gwd/<base>/WIZNOTES_SEARCH/', methods=['GET', 'POST'])
@gwd_bp.route('/gwd/<base>/WIZNOTES_SEARCH/<lang>', methods=['GET', 'POST'])
def route_WIZNOTES_SEARCH(base, lang='en'):
    raise NotImplementedError("Route WIZNOTES_SEARCH not implemented yet")
