from flask import url_for, request
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from ..i18n import get_translator


def implem_route_gwd_root(lang=None):
    """Render the GWD root page.

    Accept an optional `lang` argument to set the language.
    Prefer the query parameter `lang` if present.
    """
    req_lang = request.args.get('lang') or lang or 'en'
    translator = get_translator()

    def _(key):
        return translator.gettext(key, req_lang)

    folder = Path("bases")
    bases = [f.name[:-3] for f in folder.iterdir() if f.is_file()]
    bases_list = ', '.join(bases)
    bases_list_links = []
    for b in bases:
        href = f"/gwd/{b}"
        if req_lang:
            href = f"{href}?lang={req_lang}"
        bases_list_links.append(f'<a href="{href}">{b}</a>')

    data = {
        'lang': req_lang,
        'title': 'Base',
        'robots': 'none',
        'images_prefix': '/static/images/',
        'css': (
            f'<link rel="stylesheet" href="{url_for("static", filename="css/bootstrap.min.css")}">'  # noqa: E501
            f'<link rel="stylesheet" href="{url_for("static", filename="css/all.min.css")}">'  # noqa: E501
            f'<link rel="stylesheet" href="{url_for("static", filename="css/css.css")}">'  # noqa: E501
        ),
        'prefix': '',
        'bases_list': bases_list,
        'bases_list_links': ', '.join(bases_list_links),
        'languages': [
            ('en', 'English'),
            ('fr', 'français'),
            ('es', 'Español'),
        ],
        'templ': '',
        'version': 'dev',
        'connections': '',
        'doc_link': 'https://geneweb.tuxfamily.org/wiki',
        '_': _,
    }
    base_dir = (Path(__file__).parent.parent / "templates_jinja").resolve()
    env = Environment(
        loader=FileSystemLoader(base_dir),
        autoescape=select_autoescape(['html', 'xml'])
    )
    tmpl = env.get_template('gwd/index.html.j2')
    return tmpl.render(**data)
