"""This module provides means to perform operations on the database
using the SQLAlchemy library."""

import os
import sys

from flask import Flask
from flask_migrate import Migrate

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

try:
    engine = create_engine(os.environ.get('DATABASE_URL'))
except BaseException as e:
    sys.exit(1)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# The declarative extension in SQLAlchemy allows to define
# tables and models in one go, that is in the same class
Base = declarative_base()
Base.query = db_session.query_property()

def init_database(app: Flask) -> None:
    """This function initialize the SQLAlchemy ORM, providing a session
    and command line to create the tables in the database.

    Parameters:    
        app (flask.app.Flask): The application instance.
    """    
    
    # attach the shutdown_session function to be execute when a request ended.
    app.teardown_appcontext(shutdown_session)

    # Using Flask-Migrate as the handler for database migration.
    from .model import User
    migrate = Migrate(app, Base)


def shutdown_session(exception=None) -> None:
    """Remove the session by send it back to the pool."""

    db_session.remove()
