import uuid
import click
import names
import dateutil

from typing import List
from datetime import datetime, timedelta
from flask.cli import with_appcontext

from app.model import Exam, Patient, Order, Physician
from app.model import PatientRepository, PhysicianRepository, OrderRepository, ExamRepository
from app.exceptions import UserDataNotValid

def register_commands(app):
    """Add commands to the line command input.

    Parameters:
    app (flask.app.Flask): The application instance.
    """

    app.cli.add_command(add_user_command)
    app.cli.add_command(seed_command)


@click.command('adduser')
@click.argument('username')
@click.argument('password')
@with_appcontext
def add_user_command(username: str, password: str) -> None:
    """This function is executed through the 'user' line command.
    e.g.: flask adduser demo demo
    
    Parameters:
    username (str): The username of the user.
    password (str): The password of the user.
    """

    add_user(username, password)


def add_user(username: str, password: str) -> None:
    """Create a new user.
    
    Parameters:
    username (str): The username of the user.
    password (str): The password of the user.
    """

    from app.model import User
    from app.model import UserRepository

    user_repository = UserRepository()
    user = User()
    user.public_id = uuid.uuid1().hex
    user.username = username
    user.password = password

    try:        
        user_repository.save(user)
        click.echo('API USER CREATED SUCCESSFULLY!')
    except UserDataNotValid as e:
        click.echo('API USER ALREADY REGISTERED.')       
    except BaseException:
        click.echo('ERROR CREATING API USER')    


@click.command('seed')
@with_appcontext
def seed_command() -> None:
    """This function is executed through the 'seed' line command.
    e.g.: flask seed.

    """

    seed_func()


def seed_func() -> None:
    """Create a seed.

    Parameters:
    videos(object): a list os video objects.
    """  
    
    # Physicians
         
    physician1 = create_physician('female')   
    physician2 = create_physician('female')   
    physician3 = create_physician('male')       

    # Patients
    
    patient1 = create_patient("famale", 65, 1.68)     
    patient2 = create_patient("famale", 72, 1.78)     
    patient3 = create_patient("famale", 30, 1.60)   
    patient4 = create_patient("male", 68, 1.70)     
    patient5 = create_patient("male", 78, 1.78)     
    patient6 = create_patient("male", 100, 1.78)     
    

    # Patient's orderr        

    # order #1
    patient1_order = create_order(patient1)
    patient2_order = create_order(patient2)
    patient3_order = create_order(patient3)
    patient4_order = create_order(patient4)
    patient5_order = create_order(patient5, dateutil.parser.isoparse("2021-01-01T00:00:00Z"))
    patient6_order = create_order(patient6, dateutil.parser.isoparse("2021-01-02T00:00:00Z"))    

    # Patient's exames        

    exam1 = create_exam(physician1, patient1_order)
    exam2 = create_exam(physician2, patient2_order)
    exam3 = create_exam(physician3, patient3_order)
    exam4 = create_exam(physician1, patient4_order)
    exam5 = create_exam(physician2, patient5_order)
    exam6 = create_exam(physician3, patient6_order)    

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