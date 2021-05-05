"""It contains UserRepository class."""

from typing import List

import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash

from app.exceptions import UserDataNotValid

from .models import Exam, Order, Patient, Physician
from .repository import Repository


class ExamRepository(Repository):
    """It Contains specific method related to de Exam model."""

    def __init__(self):
        Repository.__init__(self, Exam) 

    def get_all(self, offset, limit, sort, dsc, pub_patient_id, pub_physician_id) -> List[Exam]:
        """Retrieves a list of all elements in the database.

        Returns:
        list[object]: a list of model objects.
        """        

        query = self.session.query(Exam)                
        query = self.get_all_defaul_query(query, sort, dsc)      
        
        # custom query
        if pub_patient_id and pub_physician_id:
            query = query.join(Exam.orders, Exam.physician).join(Order.patient).filter(Patient.public_id == pub_patient_id and Physician.public_id == pub_physician_id)
        elif pub_patient_id:                      
            query = query.join(Exam.orders).join(Order.patient).filter(Patient.public_id == pub_patient_id)            
        elif pub_physician_id:                      
            query = query.join(Exam.physician).filter(Physician.public_id == pub_physician_id)
        
        querypage = self.get_query_paged(query, offset, limit)
        return querypage, query.count()