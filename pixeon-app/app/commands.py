import uuid
import click
import dateutil

from typing import List
from datetime import datetime, timedelta
from flask.cli import with_appcontext

from app.exceptions import UserDataNotValid
from app.util import create_physician, create_patient, create_order, create_exam

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

    # Patient's orders
        
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

