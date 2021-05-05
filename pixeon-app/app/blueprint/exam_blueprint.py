"""Blueprint to organize and group, views related
to the '/exam' endpoint of HTTP REST API.
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
from app.model import Exam, ExamRepository
from app.util import validate_list_query, get_default_query_args

bp = Blueprint('exam', __name__)

@bp.route('', methods=('GET',))
@jwt_required
@validate_list_query(sort_values=("created_at", "updated_at"))
def get_exams():
    """Retrieves all orders.
    
    Returns:
    response: flask.Response object with the application/json mimetype.
    """

    # default paramenters
    offset, limit, sort, desc = get_default_query_args(request.args)    
    # Patient Id
    patient_id = request.args.get('patient_id')
    # Physician Id
    physician_id = request.args.get('physician_id')
    # BMI
    bmi = request.args.get('bmi')

    exam_repository = ExamRepository()
    exams, total = exam_repository.get_all(offset, limit, sort, desc, patient_id, physician_id, bmi)

    return make_response(jsonify({        
        "metadata": {
            "type": "list",
            "offset": offset,
            "limit": limit,
            "total": total, 
            "BMI": bmi
        },
        'exams': [exam.serialize() for exam in exams]
    }), 200)