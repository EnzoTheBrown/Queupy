from queupy.models import EventQueue

class PushAgent:
    def __init__(self, queue : EventQueue, event : str, frequency : int = 1):
        self.queue = queue
        self.event = event

    def emit(self):
        while True:
            payload = yield
            self.queue.push(self.event, payload)
