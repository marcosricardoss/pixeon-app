"""This package is Flask HTTP REST API Template template that already has the database bootstrap
implemented and also all feature related with the user authentications.

Application features:
    Python 3.8
    Flask
    PEP-8 for code style

This module contains the factory function 'create_app' that is
responsible for initializing the application according
to a previous configuration.
"""

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from app.database import init_database
from app.commands import register_commands
from app.util import load_config, init_instance_folder
from app.authentication import init_authentication
from app.blueprint.handlers import register_handler
from app.blueprint import ( 
    auth_blueprint, 
    database_status_blueprint,
    exam_blueprint,
    index_blueprint, 
    orders_blueprint,
    patient_blueprint,
    physician_blueprint,
    spec_blueprint, 
    users_blueprint, 
)

def create_app(package_name: str = None, test_config: dict = {}) -> Flask:
    """This function is responsible to create a Flask instance according
    a previous setting passed from environment. In that process, it also
    initialise the database source.

    Parameters:
    test_config (dict): settings coming from test environment

    Returns:
    flask.app.Flask: The application instance
    """

    package_name = package_name if package_name else __name__

    app = Flask(package_name, instance_relative_config=True)      

    load_config(app, test_config)
    init_instance_folder(app)
    register_commands(app)
    init_database(app)  

    # blueprints
    register_handler(app)
    app.register_blueprint(index_blueprint.bp)
    app.register_blueprint(spec_blueprint.bp, url_prefix=f"{app.config['API_BASE_PATH']}v1.0/spec")            
    app.register_blueprint(auth_blueprint.bp, url_prefix=f"{app.config['API_BASE_PATH']}v1.0/auth")            
    app.register_blueprint(users_blueprint.bp, url_prefix=f"{app.config['API_BASE_PATH']}v1.0/users")            
    
    app.register_blueprint(physician_blueprint.bp, url_prefix=f"{app.config['API_BASE_PATH']}v1.0/physician")    
    app.register_blueprint(patient_blueprint.bp, url_prefix=f"{app.config['API_BASE_PATH']}v1.0/patient")    
    app.register_blueprint(orders_blueprint.bp, url_prefix=f"{app.config['API_BASE_PATH']}v1.0/order")
    app.register_blueprint(exam_blueprint.bp, url_prefix=f"{app.config['API_BASE_PATH']}v1.0/exam")
    app.register_blueprint(database_status_blueprint.bp, url_prefix=f"{app.config['API_BASE_PATH']}v1.0/status")

    # cors
    cors = CORS(app, resources={r"{}*".format(app.config['API_BASE_PATH'])},
                origins='*',
                headers=['Content-Type', 'Authorization', 'api_key'],
                allow_headers=['Content-Type', 'Authorization', 'api_key'],
                expose_headers=['Content-Type', 'Authorization', 'api_key'],
                support_credentials=True)

    # jwt
    jwt = JWTManager(app)
    init_authentication(jwt)  
    
    return app
