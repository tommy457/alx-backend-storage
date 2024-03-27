#!/usr/bin/env python3
"""
Module for a web cache and tracker.
"""
import redis
import requests


def get_page(url: str) -> str:
    """ Obtain the HTML content of a particular `url` and returns """
    responce = requests.get(url).text
    client = redis.Redis()

    key = f"count:{url}"
    client.incr(key)
    client.expire(key, 10)

    return responce
