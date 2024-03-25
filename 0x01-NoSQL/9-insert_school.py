#!/usr/bin/env python3
"""
Module for the insert_school function.
"""
from pymongo.collection import Collection


def insert_school(mongo_collection: Collection, **kwargs: str) -> str:
    """ inserts a new document in a collection based on kwargs
    and returns the new _id """
    return mongo_collection.insert_one(kwargs).inserted_id
