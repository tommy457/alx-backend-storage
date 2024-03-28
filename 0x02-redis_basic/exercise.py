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
    def wrapper(self, *args: Any, **kwargs: Any) -> Any:
        """ wrapper function for counting how
        many times a function is callded """
        self._redis.incr(method.__qualname__)

        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """ decorator that takes a single method """

    @wraps(method)
    def wrapper(self, *args: Any, **kwargs: Any) -> Any:
        """ wrapper function for counting how
        many times a function is callded """
        name = method.__qualname__
        result = method(self, *args, **kwargs)
        self._redis.rpush(f"{name}:inputs", str(args))
        self._redis.rpush(f"{name}:outputs", result)

        return result
    return wrapper


def replay(method: Callable) -> None:
    """ Displays the history of calls of a particular function """
    client = redis.Redis()
    name = method.__qualname__

    totatl = client.get(name)
    inputs = f"{name}:inputs"
    outputs = f"{name}:outputs"

    inputs_list = [inp.decode("utf-8") for inp in client.lrange(inputs, 0, -1)]
    outputs_list = [outp.decode("utf-8")
                    for outp in client.lrange(outputs, 0, -1)]

    print("{} was called {} times:".format(name, int(totatl)))

    for key, value in zip(inputs_list, outputs_list):
        print("{}(*({},)) -> {}".format(name, key, value))


class Cache:
    """Represents a caching mechanism using Redis."""
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Stores the provided data in the Redis database. """
        key: str = str(uuid.uuid4())

        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Callable = None) -> Union[str, int, float, bytes, None]:
        """ Converts the returned redis byte string to the
        desired format with the callable `fn`"""
        if fn:
            return fn(self._redis.get(key))
        return self._redis.get(key)

    def get_int(self, key: str) -> int:
        """ Converts the returned redis byte string to an int. """
        return int(self._redis.get(key))

    def get_str(self, key: str) -> str:
        """ Converts the returned redis byte string to an str. """
        return str(self._redis.get(key))
