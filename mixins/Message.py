from abc import ABC


class Message(ABC):
    """
    Message interface to be used as abstraction to encapsulate data and send it to the broker or consume it as command
    """
    pass


class Command(Message):
    """
    Command interface to be used as abstraction to encapsulate data and send it to the broker or consume it as command
    """
    pass


class Event(Message):
    """
    Event interface to be used as abstraction to encapsulate data and send it to the broker or consume it as event
    """
    pass
