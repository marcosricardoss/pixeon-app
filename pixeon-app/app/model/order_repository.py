"""It contains UserRepository class."""
from typing import List

import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash

from app.exceptions import UserDataNotValid

from .models import Order
from .repository import Repository


class OrderRepository(Repository):
    """It Contains specific method related to de Order model."""

    def __init__(self):
        Repository.__init__(self, Order) 


    def get_all(self, offset, limit, sort, dsc, from_time, to_time) -> List[Order]:
        """Retrieves a list of all elements in the database.

        Returns:
        list[object]: a list of model objects.
        """        

        query = self.session.query(Order)                
        query = self.get_all_defaul_query(query, sort, dsc)      
        
        # custom query
        if from_time and to_time:
            query = query.filter(Order.created_at >= from_time, Order.created_at < to_time)                    
        
        querypage = self.get_query_paged(query, offset, limit)
        return querypage, query.count()