from flask import Flask, request, g
from flask_babel import Babel


def get_locale():
    """
    Determine the best locale based on URL path,
    cookie, URL param, or Accept-Language header.
    """
    # Check if locale was set in the view (from URL path parameter)
    if hasattr(g, 'locale') and g.locale:
        return g.locale
    # Check for 'lang' in URL query parameter (most common)
    lang = request.args.get('lang')
    if lang:
        return lang
    # Check for locale in cookie
    locale = request.cookies.get('locale')
    if locale:
        return locale
    # Fall back to Accept-Language header
    return request.accept_languages.best_match(['en', 'fr']) or 'en'


def create_app():
    """Create and configure the Flask app.

    Returns:
        Flask: Configured Flask app instance.
    """
    app = Flask(__name__)

    # Configure Babel for i18n
    app.config.setdefault('BABEL_DEFAULT_LOCALE', 'en')
    app.config.setdefault('BABEL_TRANSLATION_DIRECTORIES', 'translations')
    Babel(app, locale_selector=get_locale)

    from .routes import register_routes
    register_routes(app)
    return app
