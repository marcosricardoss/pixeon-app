"""It contains UserRepository class."""

import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash

from app.exceptions import UserDataNotValid

from .models import Patient
from .repository import Repository


class PatientRepository(Repository):
    """It Contains specific method related to de Patient model."""

    def __init__(self):
        Repository.__init__(self, Patient) 