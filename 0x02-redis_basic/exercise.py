#!/usr/bin/env python3
"""
Module for a Caching mechanism using Redis.
"""
from functools import wraps
import redis
from typing import Union, Callable, Any
import uuid


def count_calls(method: Callable) -> Callable:
    """ decorator that takes a single method """

    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """ wrapper function for counting how
        many times a function is callded """
        self.redis.incr(method.__qualname__)

        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """Represents a caching mechanism using Redis."""
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @property
    def redis(self):
        """ Getter property for the Redis client object. """
        return self._redis

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Stores the provided data in the Redis database. """
        key: str = str(uuid.uuid4())

        self.redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Callable = None) -> Union[str, int, float, bytes, None]:
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


cache = Cache()

cache.store(b"first")
print(cache.get(cache.store.__qualname__))

cache.store(b"second")
cache.store(b"third")
print(cache.get(cache.store.__qualname__))
