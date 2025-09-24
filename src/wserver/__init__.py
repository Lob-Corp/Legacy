from flask import Flask

def create_app(config="wserver.config.DevConfig"):
    app = Flask(__name__)
    app.config.from_object(config)
    from .routes import register_routes
    register_routes(app)
    return app
