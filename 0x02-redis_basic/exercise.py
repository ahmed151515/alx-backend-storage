#!/usr/bin/env python3
"""_summary_
    """

import redis
import uuid


class Cache:

    def __init__(self) -> None:
        """_summary_
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: object) -> str:
        key = str(uuid.uuid1())
        self._redis.set(key, data)
        return key
