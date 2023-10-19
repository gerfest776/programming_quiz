from abc import ABC, abstractmethod
from typing import Any


class StorageI(ABC):
    def __init__(self):
        self._storage = {}

    @abstractmethod
    def insert_value(self, key, data):
        pass

    @abstractmethod
    def get_values(self, key: int):
        pass


class InMemoryStorage(StorageI):
    def insert_value(self, key, data):
        self._storage[key] = data

    def get_values(self, key: int):
        return self._storage[key]


storage = InMemoryStorage()
