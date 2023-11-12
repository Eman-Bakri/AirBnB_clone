#!/usr/bin/python3
"""Module for a FileStorage class."""
import datetime
import os
import json


class FileStorage:

    """Class data storage and retrieve"""
    _pathfile = "file.json"
    _objs = {}

    def myclasses(self):
        """Returns  classes as a dictionary."""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        dictclasses = {"BaseModel": BaseModel,
                   "User": User,
                   "State": State,
                   "City": City,
                   "Amenity": Amenity,
                   "Place": Place,
                   "Review": Review}
        return dictclasses

    def myattributes(self):
        """Returns the attrs with their classess"""
        attrsClasses = {
            "BaseModel":
                     {"id": str,
                      "created_at": datetime.datetime,
                      "updated_at": datetime.datetime},
            "User":
                     {"email": str,
                      "password": str,
                      "first_name": str,
                      "last_name": str},
            "State":
                     {"name": str},
            "City":
                     {"state_id": str,
                      "name": str},
            "Amenity":
                     {"name": str},
            "Place":
                     {"city_id": str,
                      "user_id": str,
                      "name": str,
                      "description": str,
                      "number_rooms": int,
                      "number_bathrooms": int,
                      "max_guest": int,
                      "price_by_night": int,
                      "latitude": float,
                      "longitude": float,
                      "amenity_ids": list},
            "Review":
            {"place_id": str,
                         "user_id": str,
                         "text": str}
        }
        return attrsClasses

    def new(self, obj):
        """Manages objs with keys"""
        qk = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage._objs[qk] = obj

    def all(self):
        """returns the dictionary _objs"""
        return FileStorage._objs

    def save(self):
        """ serialization of _objs to JSON file."""
        with open(FileStorage._pathfile, "w", encoding="utf-8") as file1:
            d = {qk: val.to_dict() for qk, val in FileStorage._objs.items()}
            json.dump(d, file1)

    def reload(self):
        """Objects Reload"""
        if not os.path.isfile(FileStorage._pathfile):
            return
        with open(FileStorage._pathfile, "r", encoding="utf-8") as f:
            obj_dict = json.load(f)
            obj_dict = {k: self.classes()[v["__class__"]](**v)
                        for k, v in obj_dict.items()}
            FileStorage.__objects = obj_dict

