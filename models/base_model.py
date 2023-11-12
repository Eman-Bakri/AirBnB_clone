#!/usr/bin/python3
"""Module for the base model Class"""

from datetime import datetime
from models import storage
import uuid


class BaseModel:

    """Parent Class will inherit others."""

    def __init__(self, *args, **kwargs):
        """Initializes instance attributes

        Args:
            - *args: list of arguments
            - **kwargs: key-values arguments dict.
        """

        if kwargs is not None and kwargs != {}:
            for qk in kwargs:
                if qk == "created_at":
                    self.__dict__["created_at"] = datetime.strptime(
                        kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
                elif qk == "updated_at":
                    self.__dict__["updated_at"] = datetime.strptime(
                        kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    self.__dict__[qk] = kwargs[qk]
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def to_dict(self):
        """returns all keys/values of __dict__ dictionary. """

        _dictin = self.__dict__.copy()
        _dictin["__class__"] = type(self).__name__
        _dictin["created_at"] = _dictin["created_at"].isoformat()
        _dictin["updated_at"] = _dictin["updated_at"].isoformat()
        return _dictin

    def __str__(self):
        """Shows an official representation of string """

        return "[{}] ({}) {}".\
            format(type(self).__name__, self.id, self.__dict__)

    def save(self):
        """Saves and updates the attribute updated_at"""

        self.updated_at = datetime.now()
        storage.save()
