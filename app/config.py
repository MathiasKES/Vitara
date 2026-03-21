import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-dev-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session configurations
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 31536000  # 1 year
    SESSION_COOKIE_HTTPONLY = True

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, '..', 'vitara.db')

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # In production, cookies should be secure:
    # SESSION_COOKIE_SECURE = True
    # REMEMBER_COOKIE_SECURE = True

config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
