#!/usr/bin/env python3
"""_summary_
    """

from typing import Union
import redis
import uuid


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
