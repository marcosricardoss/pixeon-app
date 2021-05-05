"""It contains Repository generic class."""

from typing import List
from sqlalchemy import desc

from app.database import db_session
from .models import Model


class Repository:
    """This class implements the common methods used
    for all specific repositories classes. The subclasses
    of it can provide the implementation of these methods.
    """

    def __init__(self, model_class):
        self.__model_class = model_class
        self.session = db_session

    def get(self, object_id: int) -> object:
        """Retrieve a model register from database by its id.

        Parameters:
        model_id (int): Id of the model to be retrieved.

        Returns:
        object: a model object.
        """

        return self.session.query(self.__model_class).filter_by(id=object_id).first()

    def get_by_public_id(self, object_public_id: str) -> object:
        """Retrieve a model register from database by its id.

        Parameters:
        model_id (int): Id of the model to be retrieved.

        Returns:
        object: a model object.
        """

        return self.session.query(self.__model_class).filter_by(public_id=object_public_id).first()

    def get_all_defaul_query(self, query, sort, dsc):
        """ # """  

        if sort:
            if dsc:
                order_by_arg = desc(self.__model_class.__table__.c[sort])
            else: 
                order_by_arg = self.__model_class.__table__.c[sort]
            query = query.order_by(order_by_arg)
        else:
            if dsc:
                order_by_arg = desc(self.__model_class.id)
            else: 
                order_by_arg = self.__model_class.id
            query = query.order_by(order_by_arg)    

        return query     

    def get_query_paged(self, query, offset, limit):
        """ # """  

        # offset page
        if offset:
            query = query.offset(offset)

        # limit page
        if limit:
            query = query.limit(limit)  

        return query

    def get_all(self, offset, limit, sort, dsc) -> List[object]:
        """Retrieves a list of all elements in the database.

        Returns:
        list[object]: a list of model objects.
        """        

        query = self.session.query(self.__model_class)
        query = self.get_all_defaul_query(query, sort, dsc)      
        querypage = self.get_query_paged(query, offset, limit)
        return querypage, query.count()

    def save(self, obj: object) -> None:
        """Saves a model in the database.

        Parameters:
        obj(object): A model object.
        """

        self.session.add(obj)
        self.session.commit()

    def save_objects(self, objects: List[object]) -> None:
        """Saves a model in the database.

        Parameters:
        object(list[Model]): a list of model objects.
        """

        self.session.bulk_save_objects(objects)
        self.session.commit()

    def update(self, obj: object) -> None:
        """Update a existent model register in the database.

        Parameters:
        obj(object): A model object.
        """

        self.session.commit()

    def delete(self, obj: object) -> int:
        """Delete a existent model register in the database.

        Parameters:
        obj(object): A model object.

        Returns:
        int: the a model id that was deleted.
        """

        deleted = self.session.delete(obj)
        self.session.commit()

        return deleted
