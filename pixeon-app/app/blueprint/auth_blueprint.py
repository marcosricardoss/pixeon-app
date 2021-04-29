"""Blueprint to organize and group, views related
to the '/auth' endpoint of HTTP REST API.
"""
import uuid

from flask import (
    current_app, abort, Blueprint, request, 
    Response, make_response, jsonify
)
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_refresh_token_required, get_jwt_identity
)
from app.model import User, UserRepository
from app.util import (
    validate_json, validate_schema
)
from .schemas import user

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=('POST',))
@validate_json()
@validate_schema(user)
def login() -> Response:
    """User's login.
    
    Returns:
    response: flask.Response object with the application/json mimetype.
    """

    data = request.json   

    # authenticating the user
    user = UserRepository().authenticate(data.get('username'), data.get('password'))
    if not user:
        response = make_response(jsonify({
            "status": "error",
            "message": "Login error. Invalid username or password."            
        }), 401)

    else:
        access_token_encoded = create_access_token(identity=user.username)
        refresh_token_encoded = create_refresh_token(identity=user.username)        

        response = make_response(jsonify({            
            'tokens': {
                'access': access_token_encoded,
                'refresh': refresh_token_encoded
            }
        }), 200)

    return response

@bp.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    """Create a new access token.
    Returns:
        response: flask.Response object with the application/json mimetype.
    """

    current_user = get_jwt_identity()
    print("user", current_user)
    access_token_encoded = create_access_token(identity=current_user)    

    return make_response(jsonify({        
        'tokens': {'access': access_token_encoded}
    }), 200)
