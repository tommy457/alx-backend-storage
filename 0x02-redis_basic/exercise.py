#!/usr/bin/env python3
"""
Module for a Caching mechanism using Redis.
"""
import redis
from typing import Union
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
