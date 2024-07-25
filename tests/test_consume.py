from queupy import consume


def test_consume_push(queue):
    event = "test_event"
    payload = {"test": "payload"}

    queue.push(event, payload)

    assert next(consume(queue, event)).payload == payload
