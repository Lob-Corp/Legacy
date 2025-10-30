from flask import request, render_template

from ..i18n import get_translator


def implem_route_ANM(base):
    """Render the anniversaries (ANM) page for the given base.

    Mirrors the style of `gwd_root_impl`: use the translator, build a data
    mapping and render the `gwd/anm.html.j2` template from
    `src/wserver/templates_jinja`.
    """
    req_lang = request.args.get('lang') or 'en'
    translator = get_translator()

    def _(key, capitalize_first=True):
        return translator.gettext(key, req_lang, capitalize_first)

    data = {
        'lang': req_lang,
        'title': _('anniversaries'),
        'base': base,
        'prefix': f'/gwd/{base}/',
        'link_AN': f'/gwd/{base}/AN?lang={req_lang}'
        if req_lang else f'/gwd/{base}/AN',
        'link_AD': f'/gwd/{base}/AD?lang={req_lang}'
        if req_lang else f'/gwd/{base}/AD',
        'link_AM': f'/gwd/{base}/AM?lang={req_lang}'
        if req_lang else f'/gwd/{base}/AM',
        '_': _,
    }

    # Use Flask's render_template so the app's jinja environment (and
    # globals like url_for) are available and base templates resolve.
    return render_template('gwd/anm.html', **data)
