#!/usr/bin/python3
"""Module for a Review class"""

from models.base_model import BaseModel


class Review(BaseModel):
    """Class for handlng review attrs"""

    place_id = ""
    user_id = ""
    text = ""

