"""This module is responsible to initial configuration of the test. On that, 
it creates fixtures to get an applicationinstance and simulates interactions over it.
"""

import os
import uuid
import pytest
from datetime import datetime

from sqlalchemy import create_engine
from flask_jwt_extended import create_access_token

from app import create_app
from app.database import Base, engine

def init_db() -> None:
    """Import all modules here that might define models so that
    they will be registered properly on the metadata.
    """    
    
    Base.metadata.create_all(bind=engine)


def drop_db() -> None:
    """Remove all table from database."""
    
    if os.environ.get('DATABASE_URL').startswith('sqlite:///'):
        sqlite_s, sqlite_f = os.environ.get('DATABASE_URL').split("sqlite:///")        
        os.unlink(sqlite_f)
    else:        
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def app(request):
    """ Create a application instance from given settings.

    Parameters:
        request (FixtureRequest): A request for a fixture from a test or fixture function

    Returns:
        flask.app.Flask: The application instance
    """        

    # app instance
    app = create_app("testing_app", {
        'API_BASE_PATH': "/api/",
        'TESTING': True,        
        'SECRET_KEY': 'test',                
    })

    # add to the scope
    ctx = app.app_context()
    ctx.push()

    def teardown():        
        init_db()
        ctx.pop()        

    init_db()

    request.addfinalizer(teardown)
    yield app    
    
    drop_db()    


@pytest.fixture(scope='function')
def client(app):
    """Create a client with app.test_client() using app fixture.
    Tests will use the client to make requests to the application

    Parameters:
        app (flask.app.Flask): The application instance.

    Returns:
        FlaskClient: A client to allow make requests to the application.
    """

    return app.test_client()


@pytest.fixture(scope='function')
def session(app, request):
    """Creates a new database session for a test.

    Parameters:    
        app (flask.app.Flask): The application instance.
        request (FixtureRequest): A request for a fixture from a test or fixture function

    Returns:
        db_session: a SLQAlchmey Session object.
    """

    from app.database import db_session

    def teardown():
        db_session.remove()

    request.addfinalizer(teardown)
    return db_session


@pytest.fixture(scope='function')
def runner(app):
    """Create a runner with app.test_cli_runner() using app fixture, that
    can call the Click commands registered with the application.

    Parameters:
        app (flask.app.Flask): The application instance.

    Returns:
        flask.testing.FlaskCliRunner: A client to allow make requests to the application.
    """

    return app.test_cli_runner()


@pytest.fixture    
def access_token(request):
    return create_access_token(identity="test")