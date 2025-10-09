from wserver import config

def test_config_has_secret_key():
    c = config.Config()
    assert hasattr(c, "SECRET_KEY")
    assert isinstance(c.SECRET_KEY, str)
    assert c.SECRET_KEY

def test_dev_config_inherits_and_debug():
    c = config.DevConfig()
    assert hasattr(c, "SECRET_KEY")
    assert hasattr(c, "DEBUG")
    assert c.DEBUG is True

def test_prod_config_inherits_and_debug():
    c = config.ProdConfig()
    assert hasattr(c, "SECRET_KEY")
    assert hasattr(c, "DEBUG")
    assert c.DEBUG is False
