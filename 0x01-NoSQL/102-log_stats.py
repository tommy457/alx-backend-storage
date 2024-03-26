#!/usr/bin/env python3
"""
Module for listing some stats about Nginx logs stored in MongoDB.
"""
from pymongo import MongoClient
if __name__ == "__main__":
    client = MongoClient("mongodb://localhost:27017/")
    db = client["logs"]
    nginx_collection = db["nginx"]

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    total_count = nginx_collection.count_documents({})

    print("{} logs\nMethods:".format(total_count))

    for method in methods:
        print("\tmethod {}: {}".format(
            method,
            nginx_collection.count_documents({"method": method})
            )
        )
    print("{} status check".format(
        nginx_collection.count_documents({
            "path": "/status",
            "method": "GET"
            })
        )
    )
    pipeline = [
        {"$group": {
            "_id": "$ip",
            "count": {"$sum": 1},
        }},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    print("IPs:")
    for ip in nginx_collection.aggregate(pipeline):
        print("\t{}: {}".format(ip["_id"], ip["count"]))
