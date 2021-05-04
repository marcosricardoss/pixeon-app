"""Blueprint to organize and group, views related
to the '/status' endpoint of HTTP REST API.
"""

import os
from flask import (
    Blueprint, make_response, jsonify
)
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

bp = Blueprint('database_status', __name__)

@bp.route('', methods=('GET',))
@jwt_required
def status():
    """
    Checks the database connection, and retrieve 
    whether the connection is up or down.
    
    Returns:
    response: flask.Response object with the application/json mimetype.
    """    
    
    try:
        # DATABASE_URL = postgresql+psycopg2://postgres:123456@pixeon-postgres:5432/pixeon
        engine = create_engine(os.environ.get('DATABASE_URL'))
        engine.connect()
        return make_response(jsonify({                
            'status': "up",
            'msg': "The database is UP!"
        }), 200)        
    except BaseException as e:
        return make_response(jsonify({                
            'status': "down",
            'msg': "The database is DOWN!"
        }), 503)

    