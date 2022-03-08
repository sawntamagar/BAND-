import os


class Config(object):
    
    DEBUG = True
    SECRET_KEY = '1234567789'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:9845721938@localhost/band'
    UPLOAD_FOLDER = 'static/uploads'
    UPLOAD_FOLDER = UPLOAD_FOLDER
    MAX_CONTENT_LENGTH = 4 * 1024 * 1024
    
    
    def init_app(app):
        pass
    
    
class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = '1234567789'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:9845721938@localhost/band'
    DB_NAME = "band"
    DB_USERNAME = "postgres"
    DB_PASSWORD = "9845721938"
    DB_HOST = "localhost"
    SQLALCHEMY_ECHO = True
    UPLOAD_FOLDER = 'static/uploads'
    UPLOAD_FOLDER = UPLOAD_FOLDER
    MAX_CONTENT_LENGTH = 4 * 1024 * 1024
    
    
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:9845721938@localhost/band'
    
    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:9845721938@localhost/band'
    
    
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}    
        
        
        