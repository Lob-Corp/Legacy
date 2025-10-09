class Config:
    """Base config."""
    SECRET_KEY = "NO SECRET YET"


class DevConfig(Config):
    """Development config."""
    DEBUG = True


class ProdConfig(Config):
    """Production config."""
    DEBUG = False
