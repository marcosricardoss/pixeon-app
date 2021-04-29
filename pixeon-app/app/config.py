"""This module contains class whose instances will be used to
load the settings according to the running environment. """

import os
import datetime


class Default():
    """Class containing the default settings for all environments."""

    API_BASE_PATH = "/api/"        
    CORS_HEADERS = 'Content-Type'
    DEBUG = False    
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=12)
    JWT_BLACKLIST_ENABLED = False
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    SECRET_KEY = os.environ.get('SECRET_KEY').encode()
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False   


class Production(Default):
    """Class containing the settings of the production environment."""

    pass
    

class Staging(Default):
    """Class containing the settings of the staging environment."""

    pass

class Development(Default):
    """Class containing the settings of the development environment."""

    DEBUG = True