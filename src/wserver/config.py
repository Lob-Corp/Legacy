class Config:
    SECRET_KEY = "None"

class DevConfig(Config):
    DEBUG = True

class ProdConfig(Config):
    DEBUG = False
