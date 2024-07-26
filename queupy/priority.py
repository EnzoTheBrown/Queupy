from peewee import fn
from abc import ABC, abstractmethod


class PriorityEventQueue(ABC):
    """
    A model for a priority queue table in a database.

    :param priority: The priority of the event.
    """
    def __init__(self, model):
        self.model = model

    def __call__(self):
        pass


class FIFOEventQueue(PriorityEventQueue):
    """
    A model for a FIFO queue table in a database.
    """
    def __call__(self):
        return self.model.created_at <= (
            self.model.select(fn.MIN(self.model.created_at)).where(
                (self.model.event == self.model.event) &
                (self.model.state == 0)
            )
        )


class LIFOEventQueue(PriorityEventQueue):
    """
    A model for a LIFO queue table in a database.
    """
    def __call__(self):
        return self.model.created_at >= (
            self.model.select(fn.MAX(self.model.created_at)).where(
                (self.model.event == self.model.event) &
                (self.model.state == 0)
            )
        )

