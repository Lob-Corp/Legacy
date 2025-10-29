from .gwsetup import gwsetup_bp
from .gwd import gwd_bp
from .images import images_bp


def register_routes(app):
    app.register_blueprint(gwsetup_bp)
    app.register_blueprint(gwd_bp)
    app.register_blueprint(images_bp)  # Register images blueprint
