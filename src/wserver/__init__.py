from flask import Flask


def create_app():
    """Create and configure the Flask app.

    Returns:
        Flask: Configured Flask app instance.
    """
    app = Flask(__name__)
    from .routes import register_routes
    register_routes(app)
    return app
