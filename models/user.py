#!/usr/bin/python3
"""Module for a User class"""
from models.base_model import BaseModel


class User(BaseModel):
    """Class for handling user attrs"""

    email = ""
    password = ""
    first_name = ""
    last_name = ""
