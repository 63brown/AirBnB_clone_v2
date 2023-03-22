#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
import models
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import environ


class State(BaseModel, Base):
    """ Class attributes"""

    if environ['HBNB_TYPE_STORAGE'] == 'db':
         __tablename__ = "states"
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state")
    else:
        name = ""
        
        @property
        def cities(self):
            """
            getter attribute cities that returns list of City instances
            with state_id equals to the current State.id -> it will be
            the FileStorage relationship between State and City
            """
            result = []
            for j, i in models.storage.all(models.city.City).items():
                if (i.state_id == self.id):
                    result.append(i)
            return result
