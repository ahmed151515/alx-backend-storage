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
        key = str(uuid.uuid1())
        self._redis.set(key, data)
        return key
