#!/usr/bin/env python3
"""
Module for the insert_school function.
"""


def insert_school(mongo_collection, **kwargs):
    """ inserts a new document in a collection based on kwargs
    and returns the new _id """
    return mongo_collection.insert_one(kwargs).inserted_id
