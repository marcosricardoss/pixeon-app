"""It contains UserRepository class."""

import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash

from app.exceptions import UserDataNotValid

from .models import Order
from .repository import Repository


class OrderRepository(Repository):
    """It Contains specific method related to de Order model."""

    def __init__(self):
        Repository.__init__(self, Order) 