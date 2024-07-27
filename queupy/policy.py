from abc import ABC, abstractmethod


class PolicyEventQueue(ABC):
    """
    A model for a policy queue table in a database.

    :param policy: The policy of the event.
    """
    def __init__(self, model):
        self.model = model

    @abstractmethod
    def __call__(self, event):
        pass


class FIFOEventQueue(PolicyEventQueue):
    """
    A model for a FIFO queue table in a database.
    """
    def __call__(self, event):
        min_created_at = f"""(
            {self.model.table_name}.created_at <= (SELECT MIN(created_at)
            FROM {self.model.table_name}
            WHERE event = '{event}' AND state = 0))
        """
        return min_created_at


class LIFOEventQueue(PolicyEventQueue):
    """
    A model for a LIFO queue table in a database.
    """
    def __call__(self, event):
        min_created_at = f"""(
            {self.model.table_name}.created_at >= (SELECT MAX(created_at)
            FROM {self.model.table_name}
            WHERE event = '{event}' AND state = 0))
        """
        return min_created_at

