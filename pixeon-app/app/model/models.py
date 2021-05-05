"""This module define all models (persistent objects - PO) of application. Each model
is a subclasse of the Base class (base declarative) from app.model.database module.
The declarative extension in SQLAlchemy allows to define tables and models in one go,
that is in the same class.
"""

import pytz

from datetime import datetime
from pytz.reference import UTC

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, Float
from sqlalchemy.orm import relationship
from app.database import Base


class Model:
    """The Model class declare the serialize() method that is
    supposed to serializes the model data. The Model's subclasses
    can provide a implementation of this method."""

    def serialize(self) -> dict:
        """Serialize the object attributes values into a dictionary."""

        return {} # pragma: no cover

    def remove_session(self):
        """Removes an model from its current session."""

        from sqlalchemy import inspect

        session = inspect(self).session
        if session: # pragma: no cover
            session.expunge(self)


class CreationModificationDateMixin(object):
    created_at = Column(DateTime(), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime())  


association_exam_order = Table('exame_order', Base.metadata,
                                Column('order_id', Integer, ForeignKey('order.id')),
                                Column('exam_id', Integer, ForeignKey('exam.id')))


association_physician_exam = Table('physician_exame', Base.metadata,
                                Column('physician_id', Integer, ForeignKey('physician.id')),
                                Column('exam_id', Integer, ForeignKey('exam.id')))
                                

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
        return f'<User {self.username}>'        


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
    exams = relationship("Exam", backref='physician')

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
        return f'<Physician {self.name}>'


class Patient(Base, Model, CreationModificationDateMixin):
    """ Patient's model class.
    
    Column:
    id              (interger, primary key)
    public_id*      (str): public ID
    name*           (string)
    weight*         (Float)
    height*         (Float)
    
    """

    __tablename__ = 'patient'

    id = Column(Integer, primary_key=True)
    public_id = Column(String(50), unique=True, nullable=False)
    name = Column(String(250), nullable=False)    
    weight = Column(Float(), nullable=False)
    height = Column(Float(), nullable=False)
    orders = relationship("Order", backref='patient')

    def serialize(self, timezone=UTC) -> dict:
        """Serialize the object attributes values into a dictionary.

        Returns:
        dict: a dictionary containing the attributes values
        """

        data = {
            "public_id": self.public_id,
            'name': self.name,
            'weight': self.weight,
            "height": self.height,
            "created_at": self.created_at.astimezone(timezone).isoformat(),
            "updated_at": self.updated_at.astimezone(timezone).isoformat() if self.updated_at else ''            
        }

        return data

    def __repr__(self) -> str:
        return f'<Patient {self.name}>'        


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
    patient_id = Column(Integer, ForeignKey('patient.id'))
    exams = relationship("Exam",
                            secondary=association_exam_order,                            
                            backref="orders")

    def serialize(self, timezone=UTC) -> dict:
        """Serialize the object attributes values into a dictionary.

        Returns:
        dict: a dictionary containing the attributes values
        """

        data = {
            "public_id": self.public_id,            
            # "patient": self.patient.name, 
            "patient": self.patient.serialize(),
            "created_at": self.created_at.astimezone(timezone).isoformat(),
            "updated_at": self.updated_at.astimezone(timezone).isoformat() if self.updated_at else ''            
        }

        return data

    def __repr__(self) -> str:
        return f'<Order {self.public_id}>'        


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
    physician_id = Column(Integer, ForeignKey('physician.id'))

    def serialize(self, timezone=UTC) -> dict:
        """Serialize the object attributes values into a dictionary.

        Returns:
        dict: a dictionary containing the attributes values
        """

        data = {
            "public_id": self.public_id,
            'name': self.name,
            "created_at": self.created_at.astimezone(timezone).isoformat(),
            "updated_at": self.updated_at.astimezone(timezone).isoformat() if self.updated_at else '',
            # "physician": [p.serialize() for p in self.physician],
            "physician": self.physician.serialize(),
            "order": [o.serialize() for o in self.orders]
        }

        return data

    def __repr__(self) -> str:
        return f'<Exam {self.name}>'        


  