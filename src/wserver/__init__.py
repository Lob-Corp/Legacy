from flask import Flask


def create_app(config="wserver.config.DevConfig"):
    """Create and configure the Flask app.

    Args:
        config (str): Config class path. Defaults to "wserver.config.DevConfig".

    Returns:
        Flask: Configured Flask app instance.
    """
    app = Flask(__name__)
    app.config.from_object(config)
    from .routes import register_routes
    register_routes(app)
    return app
