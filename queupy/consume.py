import time
from .database import ExceptionQueueEmpty, EventQueue
from logging import getLogger

logger = getLogger(__name__)


def consume(queue : EventQueue, event : str, frequency : float = 1.0):
    while True:
        try:
            payload = queue.pop(event)
            yield payload
        except ExceptionQueueEmpty:
            pass
        time.sleep(frequency)

