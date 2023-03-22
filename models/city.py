#!/usr/bin/python
""" City Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import environ
from models.state import State


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    
    if environ['HBNB_TYPE_STORAGE'] == 'db':
        __tablename__ = "cities"
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('state.id'))
        places = relationship('Place', cascade='all, delete', backref='cities')
        
    else:
        state_id = ""
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes city"""
        super().__init__(*args, **kwargs)
