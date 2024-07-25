from .database import EventQueue


def produce(queue : EventQueue, event : str, payload : dict):
    queue.push(event, payload)
