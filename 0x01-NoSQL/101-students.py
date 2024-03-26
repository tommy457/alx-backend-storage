#!/usr/bin/env python3
"""
Module for the top_students function.
"""


def top_students(mongo_collection):
    """ Returns all students sorted by average score. """
    pipeline = [
        {"$unwind": "$topics"},
        {"$group": {
            "_id": "$_id",
            "name": {"$first": "$name"},
            "averageScore": {"$avg": "$topics.score"}
        }},
        {"$sort": {"averageScore": -1}}
    ]
    return mongo_collection.aggregate(pipeline)
