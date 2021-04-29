"""This module define all models (persistent objects - PO) of application. Each model
is a subclasse of the Base class (base declarative) from app.model.database module.
The declarative extension in SQLAlchemy allows to define tables and models in one go,
that is in the same class.
"""

import pytz

from datetime import datetime
from pytz.reference import UTC

from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base


class Model:
    """The Model class declare the serialize() method that is
    supposed to serializes the model data. The Model's subclasses
    can provide a implementation of this method."""

    def serialize(self) -> dict:
        """Serialize the object attributes values into a dictionary."""

        return {} # pragma: no cover

    def remove_session(self):
        """Removes an object from the session its current session."""

        from sqlalchemy import inspect

        session = inspect(self).session
        if session: # pragma: no cover
            session.expunge(self)


class CreationModificationDateMixin(object):
    created_at = Column(DateTime(), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime())  


class User(Base, Model, CreationModificationDateMixin):
    """ User's model class.
    
    Column:
    id              (interger, primary key)
    public_id*      (str): public ID
    username*       (string, unique)
    password*       (string)    
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    public_id = Column(String(50), unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(256), nullable=False)

    def serialize(self, timezone=UTC) -> dict:
        """Serialize the object attributes values into a dictionary.

        Returns:
        dict: a dictionary containing the attributes values
        """

        data = {
            "public_id": self.public_id,
            'username': self.username,
            "created_at": self.created_at.astimezone(timezone).isoformat(),
            "updated_at": self.updated_at.astimezone(timezone).isoformat() if self.updated_at else ''            
        }

        return data

    def __repr__(self) -> str:
        return '<User %r>' % (self.username)


class Physician(Base, Model, CreationModificationDateMixin):
    """ Physician's model class.
    
    Column:
    id              (interger, primary key)
    public_id*      (str): public ID
    name*           (string)
    
    """

    __tablename__ = 'physician'

    id = Column(Integer, primary_key=True)
    public_id = Column(String(50), unique=True, nullable=False)
    name = Column(String(250), nullable=False)    

    def serialize(self, timezone=UTC) -> dict:
        """Serialize the object attributes values into a dictionary.

        Returns:
        dict: a dictionary containing the attributes values
        """

        data = {
            "public_id": self.public_id,
            'name': self.name,
            "created_at": self.created_at.astimezone(timezone).isoformat(),
            "updated_at": self.updated_at.astimezone(timezone).isoformat() if self.updated_at else ''            
        }

        return data

    def __repr__(self) -> str:
        return '<Physician %r>' % (self.name)       


class Patient(Base, Model, CreationModificationDateMixin):
    """ Patient's model class.
    
    Column:
    id              (interger, primary key)
    public_id*      (str): public ID
    name*           (string)
    
    """

    __tablename__ = 'patient'

    id = Column(Integer, primary_key=True)
    public_id = Column(String(50), unique=True, nullable=False)
    name = Column(String(250), nullable=False)    

    def serialize(self, timezone=UTC) -> dict:
        """Serialize the object attributes values into a dictionary.

        Returns:
        dict: a dictionary containing the attributes values
        """

        data = {
            "public_id": self.public_id,
            'name': self.name,
            "created_at": self.created_at.astimezone(timezone).isoformat(),
            "updated_at": self.updated_at.astimezone(timezone).isoformat() if self.updated_at else ''            
        }

        return data

    def __repr__(self) -> str:
        return '<Patient %r>' % (self.name)


class Order(Base, Model, CreationModificationDateMixin):
    """ User's model class.
    
    Column:
    id              (interger, primary key)
    public_id*      (str): public ID
    name*           (string)
    
    """

    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    public_id = Column(String(50), unique=True, nullable=False)    

    def serialize(self, timezone=UTC) -> dict:
        """Serialize the object attributes values into a dictionary.

        Returns:
        dict: a dictionary containing the attributes values
        """

        data = {
            "public_id": self.public_id,            
            "created_at": self.created_at.astimezone(timezone).isoformat(),
            "updated_at": self.updated_at.astimezone(timezone).isoformat() if self.updated_at else ''            
        }

        return data


class Exam(Base, Model, CreationModificationDateMixin):
    """ User's model class.
    
    Column:
    id              (interger, primary key)
    public_id*      (str): public ID
    name*           (string)
    
    """

    __tablename__ = 'exam'

    id = Column(Integer, primary_key=True)
    public_id = Column(String(50), unique=True, nullable=False)
    name = Column(String(250), nullable=False)    

    def serialize(self, timezone=UTC) -> dict:
        """Serialize the object attributes values into a dictionary.

        Returns:
        dict: a dictionary containing the attributes values
        """

        data = {
            "public_id": self.public_id,
            'name': self.name,
            "created_at": self.created_at.astimezone(timezone).isoformat(),
            "updated_at": self.updated_at.astimezone(timezone).isoformat() if self.updated_at else ''            
        }

        return data

    def __repr__(self) -> str:
        return '<Exam %r>' % (self.name)         


  