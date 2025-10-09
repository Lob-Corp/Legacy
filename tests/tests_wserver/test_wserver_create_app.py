from wserver import create_app

def test_create_app_default():
    app = create_app()
    assert app is not None
    assert app.config["DEBUG"] is True

def test_create_app_prod():
    app = create_app("wserver.config.ProdConfig")
    assert app.config["DEBUG"] is False
