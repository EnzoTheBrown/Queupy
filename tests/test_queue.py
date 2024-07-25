from queupy import ExceptionQueueEmpty


def test_queue_push(queue):
    event = "test_event"
    payload = {"test": "payload"}
    queue.push(event, payload)
    assert queue.pop(event).payload == payload


def test_queue_pop(queue):
    event = "test_event"
    payload = {"test": "payload"}
    queue.push(event, payload)
    assert queue.pop(event).payload == payload
    try:
        queue.pop(event)
        assert False
    except ExceptionQueueEmpty:
        pass
    except Exception as e:
        assert False, e

