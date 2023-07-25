from abc import ABC, abstractmethod

from mixins.Message import Message


class Repository(ABC):
    """
    Repository interface to be used as abstraction to access data layer and return objects
    """

    @abstractmethod
    def create(self, command: Message):
        raise NotImplementedError("create method not implemented")

    @abstractmethod
    def find_all(self):
        raise NotImplementedError("find_all method not implemented")

    @abstractmethod
    def find_by_id(self, id: str):
        raise NotImplementedError("find_by_id method not implemented")

    @abstractmethod
    def update_by_id(self, id: str, command: Message):
        raise NotImplementedError("update_by_id method not implemented")

    @abstractmethod
    def delete_by_id(self, id: str):
        raise NotImplementedError("delete_by_id method not implemented")
