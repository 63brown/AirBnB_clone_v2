#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel, Base
from models.place import Place
from models.user import User
from os import environ
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey, create_engine, Integer
from sqlalchemy.sql.schema import ForeignKey
import sqlalchemy
import models


class Review(BaseModel, Base):
    """ Review classto store review information """
    
    if environ['HBNB_TYPE_STORAGE'] == 'db':
        __tablename__ = "reviews"
        place_id = Column(String(60), ForeignKey("places.id"))
        user_id = Column(String(60), ForeignKey("users.id"))
        text = Column(String(1024), nullable=False)
        place = relationship("Place", back_populates="reviews")
    else:
        place_id = ""
        user_id = ""
        text = ""
        
    def __init__(self, *args, **kwargs):
        """initializes Review"""
        super().__init__(*args, **kwargs)
