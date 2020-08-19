import abc

class NotificationInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def send(self, Message: str) -> bool: pass