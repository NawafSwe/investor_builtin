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
