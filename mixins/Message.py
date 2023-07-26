from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict

from typing import TypedDict


class Message(ABC):
    """
    Message interface to be used as abstraction to encapsulate data and send it to the broker or consume it as command
    """

    @abstractmethod
    def dict(self):
        raise NotImplementedError("dict method is not implemented")


@dataclass
class Command(Message):
    """
    Command interface to be used as abstraction to encapsulate data and send it to the broker or consume it as command
    """

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}


@dataclass
class Event(Message):
    """
    Event interface to be used as abstraction to encapsulate data and send it to the broker or consume it as event
    """

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}
