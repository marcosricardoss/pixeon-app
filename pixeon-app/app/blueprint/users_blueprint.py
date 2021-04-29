"""Blueprint to organize and group, views related
to the '/account' endpoint of HTTP REST API.
"""
import uuid
from _datetime import datetime
from pytz.reference import UTC

from flask import (
    abort, Blueprint, request, Response, make_response, jsonify
)
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)
from app.model import User, UserRepository
from app.util import ( 
    validate_json, validate_schema, validate_list_query
)
from .schemas import user

bp = Blueprint('users', __name__)

@bp.route('', methods=('GET',))
@jwt_required
@validate_list_query(sort_values=("created_at", "updated_at"))
def get_users():
    """Retrieves all users.
    
    Returns:
    response: flask.Response object with the application/json mimetype.
    """

    offset = int(request.args.get('offset')) if request.args.get('offset') else None
    limit = int(request.args.get('limit')) if request.args.get('limit') else None
    sort = request.args.get('sort')
    desc = request.args.get('desc')    

    user_repository = UserRepository()
    users, total = user_repository.get_all(offset, limit, sort, desc)

    return make_response(jsonify({        
        "metadata": {
            "type": "list",
            "offset": offset,
            "limit": limit,
            "total": total
        },
        'users': [user.serialize() for user in users]
    }), 200)


@bp.route('', methods=('POST',))
@validate_json()
@validate_schema(user)
def add_user() -> Response:
    """Adds a new user.

    Returns:
    response: flask.Response object with the application/json mimetype.
    """   

    user_repository = UserRepository()
    
    # parsing json data
    username = request.json.get('username')
    password = request.json.get('password')
    
    # check the date interval           
    if user_repository.get_by_username(username):
        return make_response(jsonify({
            'status': 'error',
            'code': 101,
            'message': "The username is already being used"
        }), 400)
    
    # saving
    user = User()
    user.public_id = uuid.uuid1().hex
    user.username = username
    user.password = password    
    user_repository.save(user)    

    return make_response(jsonify(user.serialize()), 200)


@bp.route('/<string:user_id>', methods=('GET',))
def get_user_by_id(user_id):
    """Retrieves user by public ID.

    Parameters:
    station_id (int): The user public id.

    Returns:
    response: flask.Response object with the application/json mimetype.
    """

    user_repository = UserRepository()
    user = user_repository.get_by_public_id(user_id)

    if user: 
        return make_response(jsonify(user.serialize()), 200)

    abort(404)


@bp.route('/<string:user_id>', methods=('PUT',))
@validate_json()
@validate_schema(user)
def update_user_by_id(user_id):
    """Updates a user by public ID.
    
    Parameters:
    station_id (int): The user public id.

    Returns:
    response: flask.Response object with the application/json mimetype.
    """

    user_repository = UserRepository()
    user = user_repository.get_by_public_id(user_id)

    # parsing json data
    username = request.json.get('username')
    password = request.json.get('password')

    if user: 
        user_by_username = user_repository.get_by_username(username)
        if  user_by_username and user_id != user_by_username.public_id:
            return make_response(jsonify({
                'status': 'error',
                'code': 101,
                'message': "The username is already being used"
            }), 400)
        
        user.username = username
        user.password = password
        user.updated_at = datetime.now().astimezone(UTC)                
        user_repository.update(user)
        
        return make_response(jsonify(user.serialize()), 200)

    abort(404)



@bp.route('/<string:station_id>', methods=('DELETE',))
def delete_user_by_id(station_id):
    """Deletes a user by public ID.

    Parameters:
    station_id (int): The user public id.

    Returns:
    response: flask.Response object with the application/json mimetype.
    """

    user_repository = UserRepository()
    user = user_repository.get_by_public_id(station_id)

    if user: 
        user_repository.delete(user)
        return make_response(jsonify({}), 204)

    abort(404)