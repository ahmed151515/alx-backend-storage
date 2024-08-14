#!/usr/bin/env python3
"""_summary_
    """

from functools import wraps
from typing import Any, Callable, Union
import redis
import uuid


def count_calls(method: Callable) -> Callable:
    """_summary_

    Args:
        method (Callable): _description_

    Returns:
        Callable: _description_
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """_summary_

        Returns:
            Any: _description_
        """

        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """_summary_

    Args:
        method (Callable): _description_

    Returns:
        Callable: _description_
    """
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """_summary_

        Returns:
            Any: _description_
        """
        in_key = '{}:inputs'.format(method.__qualname__)
        out_key = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(in_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(out_key, output)
        return output
    return invoker


def replay(fn: Callable) -> None:
    """_summary_

    Args:
        fn (Callable): _description_
    """
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    fxn_name = fn.__qualname__
    in_key = '{}:inputs'.format(fxn_name)
    out_key = '{}:outputs'.format(fxn_name)
    fxn_call_count = 0
    if redis_store.exists(fxn_name) != 0:
        fxn_call_count = int(redis_store.get(fxn_name))
    print('{} was called {} times:'.format(fxn_name, fxn_call_count))
    fxn_inputs = redis_store.lrange(in_key, 0, -1)
    fxn_outputs = redis_store.lrange(out_key, 0, -1)
    for fxn_input, fxn_output in zip(fxn_inputs, fxn_outputs):
        print('{}(*{}) -> {}'.format(
            fxn_name,
            fxn_input.decode("utf-8"),
            fxn_output,
        ))


class Cache:

    def __init__(self) -> None:
        """_summary_
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """_summary_

        Args:
            data (Union[str, bytes, int, float]): _description_

        Returns:
            str: _description_
        """
        key = str(uuid.uuid1())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: callable = None) -> Union[str, bytes, int, float]:

        data = self._redis.get(key)
        if fn is not None:
            data = fn(data)

        return data

    def get_str(self, key: str) -> str:
        """_summary_

        Args:
            key (str): _description_

        Returns:
            str: _description_
        """
        data = (self.get(key)).decode('utf-8')
        return data

    def get_int(self, key: str) -> int:

        data = int(self.get(key))
        return data
