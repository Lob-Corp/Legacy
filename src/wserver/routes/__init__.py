from .base import base_bp
from .gwd import gwd_bp

def register_routes(app):
    app.register_blueprint(base_bp)
    app.register_blueprint(gwd_bp)
