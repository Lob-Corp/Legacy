from flask import Flask, request, g
from flask_babel import Babel


def get_locale():
    """Determine the best locale based on URL path, cookie, URL param, or Accept-Language header."""
    # Check if locale was set in the view (from URL path parameter)
    if hasattr(g, 'locale') and g.locale:
        return g.locale
    # Check for locale in cookie
    locale = request.cookies.get('locale')
    if locale:
        return locale
    # Check for locale in URL query parameter
    locale = request.args.get('locale')
    if locale:
        return locale
    # Fall back to Accept-Language header
    return request.accept_languages.best_match(['en', 'fr'])


def create_app(config="wserver.config.DevConfig"):
    """Create and configure the Flask app.

    Args:
        config (str): Config class path.
        Defaults to "wserver.config.DevConfig".

    Returns:
        Flask: Configured Flask app instance.
    """
    app = Flask(__name__)
    app.config.from_object(config)
    
    # Configure Babel for i18n
    app.config.setdefault('BABEL_DEFAULT_LOCALE', 'en')
    app.config.setdefault('BABEL_TRANSLATION_DIRECTORIES', 'translations')
    babel = Babel(app, locale_selector=get_locale)
    
    from .routes import register_routes
    register_routes(app)
    return app
