"""Blueprint to organize and group, views related
to the '/order' endpoint of HTTP REST API.
"""
import uuid
import dateutil.parser
from pytz.reference import UTC

from flask import (
    abort, Blueprint, request, Response, make_response, jsonify
)
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)
from app.model import Order, OrderRepository
from app.util import validate_list_query, validate_iso_date, get_default_query_args

bp = Blueprint('order', __name__)

def validate_date_range(values):
    from_time_str = values.get('from_time')
    to_time_str = values.get('to_time')
    
    if from_time_str and validate_iso_date(from_time_str):    
        if to_time_str and validate_iso_date(to_time_str):                    
            from_time = dateutil.parser.isoparse(request.args.get('from_time'))        
            to_time = dateutil.parser.isoparse(request.args.get('to_time'))   
            return from_time, to_time
        else: 
            return False
    return True

@bp.route('', methods=('GET',))
@jwt_required
@validate_list_query(sort_values=("created_at", "updated_at"))
def get_orders():
    """Retrieves all orders.
    
    Returns:
    response: flask.Response object with the application/json mimetype.
    """

    # default paramenters
    offset, limit, sort, desc = get_default_query_args(request.args)
    
    # range date range paramenters    
    from_time, to_time = None, None
    daterange = validate_date_range(request.args)    
    if not daterange:
        return make_response(jsonify({            
            'msg': "The given date range is invalid"    
        }), 400)    
    if isinstance(daterange, tuple):
        from_time, to_time = daterange 

    order_repository = OrderRepository()
    orders, total = order_repository.get_all(offset, limit, sort, desc, from_time, to_time)

    return make_response(jsonify({        
        "metadata": {
            "type": "list",
            "offset": offset,
            "limit": limit,
            "total": total,
            "from_time": from_time,
            "to_time": to_time
        },
        'orders': [order.serialize() for order in orders]
    }), 200)