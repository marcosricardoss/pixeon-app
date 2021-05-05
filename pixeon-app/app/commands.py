import uuid
import click

from datetime import datetime, timedelta
from typing import List

from flask.cli import with_appcontext

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

    import uuid
    from app.model import Exam, Patient, Order, Physician
    from app.model import PatientRepository, PhysicianRepository, OrderRepository

    physician_repository = PhysicianRepository()
    patient_repository = PatientRepository()
    order_repository = OrderRepository()

    # Physicians
         
    physician1 = Physician()
    physician1.public_id = uuid.uuid1().hex
    physician1.name = "Dra Jane Doe"

    physician2 = Physician()
    physician2.public_id = uuid.uuid1().hex
    physician2.name = "Dra Jhon Doe"         

    physician_repository.save(physician1)     
    physician_repository.save(physician2)   

    # Patients
    
    patient1 = Patient()
    patient1.public_id = uuid.uuid1().hex
    patient1.name = "Jane Doe" 
    patient1.weight = 30
    patient1.height = 1.60    
    
    patient2 = Patient()
    patient2.public_id = uuid.uuid1().hex
    patient2.name = "John Doe"
    patient2.weight = 95
    patient2.height = 1.78

    patient_repository.save(patient1)
    patient_repository.save(patient2)         
    
    # Patient's order        

    # order #1
    patient1_order = Order()
    patient1_order.public_id = uuid.uuid1().hex
    patient1_order.patient_id = patient1.id

    exam1 = Exam()
    exam1.public_id = uuid.uuid1().hex
    exam1.name = "Exam 1"
    exam1.physician_id = physician1.id
    patient1_order.exams.append(exam1)        

    # order #2
    patient2_order = Order()
    patient2_order.public_id = uuid.uuid1().hex
    patient2_order.patient_id = patient2.id
    
    exam2 = Exam()
    exam2.public_id = uuid.uuid1().hex
    exam2.name = "Exam 2"
    exam2.physician_id = physician2.id
    patient2_order.exams.append(exam2)
    
    order_repository.save(patient1_order)
    order_repository.save(patient2_order)