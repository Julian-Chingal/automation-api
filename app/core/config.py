import os

class Config:
    """Base configuration class."""
    PORT = os.environ.get('PORT', 8000)

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    DATABASE_URI = os.environ.get('DEV_DATABASE_URI', 'localhost:5432/devdb')

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    DATABASE_URI = os.environ.get('DATABASE_URI', 'localhost:5432/proddb')
