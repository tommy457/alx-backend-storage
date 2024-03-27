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
    responce_key = f"res:{url}"
    client.set(responce_key, responce)

    client.incr(key)
    client.setex(responce_key, 10, responce)

    return responce
