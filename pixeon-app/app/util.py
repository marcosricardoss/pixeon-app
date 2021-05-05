import os
import re
import json
import uuid
import names

from functools import wraps
from jsonschema import Draft7Validator, draft7_format_checker

from flask import Flask, abort, request, make_response, jsonify

from app.model import Exam, Patient, Order, Physician
from app.model import PatientRepository, PhysicianRepository, OrderRepository, ExamRepository

iso_regex_date = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$'
match_regex_date = re.compile(iso_regex_date).match

def validate_json(multipart=False):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            if ((not multipart and not request.is_json) or (multipart and not request.form)):
                abort(400)
            return f(*args, **kw)
        return wrapper
    return decorator


def validate_schema(schema):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            validator = Draft7Validator(
                schema, format_checker=draft7_format_checker)

            data = None
            if request.content_type == 'application/json':
                data = request.json
            else:
                data = dict(request.form)
                data = json.loads(data['data'])

            if not validator.is_valid(data):
                errors = sorted(validator.iter_errors(data),
                                key=lambda e: e.schema_path)
                erros_output = list()

                for error in errors:
                    erros_output.append({
                        "message": error.message,
                        "property": '.'.join(error.absolute_path) if error.absolute_path else '',
                        "validator_value":  error.validator_value,
                        "validator": error.validator,
                    })

                return make_response(jsonify({
                    'status': 'error',
                    'code': 1,
                    'message': "Invalid input",
                    'errors': erros_output
                }), 400)
            return f(*args, **kw)
        return wrapper
    return decorator


def validate_list_query(sort_values):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):

            # default values

            offset = request.args.get('offset')
            limit = request.args.get('limit')
            sort = request.args.get('sort')
            desc = request.args.get('desc')

            if offset and not offset.isdigit(): 
                abort(400)                
            
            if limit and not limit.isdigit(): 
                abort(400)
            
            if sort and sort not in sort_values:
                abort(400)

            if desc and desc != "1":
                abort(400)
            
            return f(*args, **kw)
        return wrapper
    return decorator


def get_default_query_args(values):    
    offset = int(values.get('offset')) if values.get('offset') else None
    limit = int(values.get('limit')) if values.get('limit') else None
    sort = values.get('sort')
    desc = values.get('desc')

    return offset, limit, sort, desc


def load_config(app: Flask, test_config) -> None:
    """Load the application's config

    Parameters:
        app (flask.app.Flask): The application instance Flask that'll be running
        test_config (dict):
    """

    if test_config:
        if test_config.get('TESTING'):
            app.config.from_mapping(test_config)
        else:
            app.config.from_object(
                f'app.config.{test_config.get("FLASK_ENV").capitalize()}')
    else:
        app.config.from_object(
            f'app.config.{os.environ.get("FLASK_ENV").capitalize()}')


def init_instance_folder(app: Flask) -> None:
    """Ensure the instance folder exists.

    Parameters:
        app (flask.app.Flask): The application instance Flask that'll be running
    """

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


def validate_iso_date(value):
    try:            
        if match_regex_date(value) is not None:
            return True
    except:        
        return False


def create_physician(gender):
    """  """

    prefix = "Dra." if gender == "female" else "Dr."
    physician = Physician()
    physician.public_id = uuid.uuid1().hex
    physician.name = f"{prefix} {names.get_full_name(gender=gender)}"    

    repository = PhysicianRepository()
    repository.save(physician)
    
    return physician


def create_patient(gender, weight, height):
    """  """

    patient = Patient()
    patient.public_id = uuid.uuid1().hex
    patient.name = names.get_full_name(gender=gender)
    patient.weight = weight
    patient.height = height  

    repository = PatientRepository()
    repository.save(patient)

    return patient


def create_order(patient, created_at=None):
    """  """

    patient_order = Order()
    patient_order.public_id = uuid.uuid1().hex
    patient_order.patient = patient    
    if created_at:
        patient_order.created_at = created_at  

    repository = OrderRepository()
    repository.save(patient_order)

    return patient_order


def create_exam(physician, patient_order):
    """  """

    exam = Exam()
    exam.public_id = uuid.uuid1().hex
    exam.name = f"Exame Name - {physician.name}"
    exam.physician = physician
    exam.order = patient_order  

    repository = ExamRepository()
    repository.save(exam)

    return exam        