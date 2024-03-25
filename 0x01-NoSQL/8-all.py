#!/usr/bin/env python3
"""
Module for the list_all function.
"""
from pymongo.collection import Collection
from typing import List, Dict


def list_all(mongo_collection: Collection) -> List[Dict[str, str]]:
    """ Lists all documents in a collection  """
    return mongo_collection.find()
