"""Register application routes."""

from .base import base_bp


def register_routes(app):
    """Attach all blueprints to the app."""
    app.register_blueprint(base_bp)
