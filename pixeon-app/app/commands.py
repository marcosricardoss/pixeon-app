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