"""It contains UserRepository class."""

import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash

from app.exceptions import UserDataNotValid

from .models import Exam
from .repository import Repository


class ExamRepository(Repository):
    """It Contains specific method related to de Exam model."""

    def __init__(self):
        Repository.__init__(self, Exam) 