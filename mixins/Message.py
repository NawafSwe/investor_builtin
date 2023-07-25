from abc import ABC, abstractmethod


class Message(ABC):
    pass


class Command(Message):
    pass


class Event(Message):
    pass
