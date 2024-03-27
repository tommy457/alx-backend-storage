#!/usr/bin/env python3
"""
Module for a Caching mechanism using Redis.
"""
import redis
from typing import Union, Callable
import uuid


class Cache:
    """Represents a caching mechanism using Redis."""
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @property
    def redis(self):
        """ Getter property for the Redis client object. """
        return self._redis

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Stores the provided data in the Redis database. """
        key: str = str(uuid.uuid4())

        self.redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable) -> Union[str, int, float, bytes]:
        """ Converts the returned redis byte string to the
        desired format with the callable `fn`"""
        if fn:
            return fn(self.redis.get(key))
        return self.redis.get(key)

    def get_int(self, key: str) -> int:
        """ Converts the returned redis byte string to an int. """
        return int(self.redis.get(key))

    def get_str(self, key: str) -> str:
        """ Converts the returned redis byte string to an str. """
        return str(self.redis.get(key))
