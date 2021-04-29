"""It contains UserRepository class."""

import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash

from app.exceptions import UserDataNotValid

from .models import User
from .repository import Repository


class UserRepository(Repository):
    """It Contains specific method related to de User model."""

    def __init__(self):
        Repository.__init__(self, User)  

    def save(self, user: User) -> None:
        try:
            user.password = generate_password_hash(user.password)
            self.session.add(user)
            self.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            raise UserDataNotValid(str(e))

    def update(self, user: User) -> None:
        """Update a existent user in the database.
        Parameters:
        model (object): A user model object.
        """

        user.password = generate_password_hash(user.password)
        self.session.commit()

    def authenticate(self, username: str, password: str) -> bool:
        """checks user authenticity by username and password.
        
        Parameters:
        username (str): The username of the user.
        password (str): The password of the user.
        
        Returns:
        bool: A boolean indicating the user authenticity.
        """

        user = self.get_by_username(username)
        if user and check_password_hash(user.password, password):
            return user

        return False

    def get_by_username(self, username: str) -> User:
        """Retrive a users from database by its username.
        
        Parameters:
        username (str): The username of the user.
        
        Returns:
        User: User model object.
        """

        return self.session.query(User).filter_by(username=username).first()