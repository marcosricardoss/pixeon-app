"""Blueprint to organize and group, views related
to the '/physician' endpoint of HTTP REST API.
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
from app.model import Physician, PhysicianRepository
from app.util import validate_list_query, get_default_query_args

bp = Blueprint('physicians', __name__)

@bp.route('', methods=('GET',))
@jwt_required
@validate_list_query(sort_values=("created_at", "updated_at"))
def get_physician():
    """Retrieves all physicians.
    
    Returns:
    response: flask.Response object with the application/json mimetype.
    """

    # default paramenters
    offset, limit, sort, desc = get_default_query_args(request.args)

    physician_repository = PhysicianRepository()
    physicians, total = physician_repository.get_all(offset, limit, sort, desc)

    return make_response(jsonify({        
        "metadata": {
            "type": "list",
            "offset": offset,
            "limit": limit,
            "total": total
        },
        'physicians': [physician.serialize() for physician in physicians]
    }), 200)