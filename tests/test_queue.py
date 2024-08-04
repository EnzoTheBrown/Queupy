import pytest
import time
from queupy import init_queue, FIFOEventQueue, LIFOEventQueue
from tests.assets import COMPLEX_JSON, JSON_WITH_NONE
from threading import Thread


def test_push(event_queue):
    event_queue.push("event1", {"key": "value1"})
    event_queue.push("event1", {"key": "value2"})
    conn = event_queue.conn
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {event_queue.table_name} WHERE state = 0")
    conn.commit()
    result = cur.fetchall()
    cur.close()
    assert len(result) == 2


def test_pop(event_queue):
    event_queue.push("event1", {"key": "value1"})

    conn = event_queue.conn
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {event_queue.table_name} WHERE state = 0")
    conn.commit()
    result = cur.fetchall()
    assert len(result) == 1

    payload = event_queue.pop("event1")
    assert payload == {"key": "value1"}

    cur.execute(f"SELECT * FROM {event_queue.table_name} WHERE state = 0")
    conn.commit()
    result = cur.fetchall()
    assert len(result) == 0
    cur.close()


def test_complex_json(event_queue):
    event_queue.push("event1", COMPLEX_JSON)
    payload = event_queue.pop("event1")
    assert payload == COMPLEX_JSON


def test_json_with_none(event_queue):
    event_queue.push("event1", JSON_WITH_NONE)
    payload = event_queue.pop("event1")
    assert payload == JSON_WITH_NONE


def test_fifo(event_queue):
    event_queue.push("event1", {"key": "value1"})
    event_queue.push("event1", {"key": "value2"})
    payload1 = event_queue.pop("event1")
    payload2 = event_queue.pop("event1")
    assert payload1 == {"key": "value1"}
    assert payload2 == {"key": "value2"}


def test_lifo(event_queue_lifo):
    event_queue_lifo.push("event1", {"key": "value1"})
    event_queue_lifo.push("event1", {"key": "value2"})
    payload2 = event_queue_lifo.pop("event1")
    payload1 = event_queue_lifo.pop("event1")
    assert payload1 == {"key": "value1"}
    assert payload2 == {"key": "value2"}


def test_select(event_queue):
    event_queue.push("event1", {"key": "value1"})

    events = event_queue.select()

    assert len(events) == 1
    assert events[0]['event'] == "event1"
    assert events[0]['state'] == 0
    assert events[0]['payload'] == {"key": "value1"}
    assert events[0]['transaction_id'] is None
    assert events[0]['created_at'] is not None
    assert events[0]['updated_at'] is not None

    event_queue.pop("event1")

    events = event_queue.select()

    assert len(events) == 1
    assert events[0]['event'] == "event1"
    assert events[0]['state'] == 1
    assert events[0]['payload'] == {"key": "value1"}
    assert events[0]['transaction_id'] is not None
    assert events[0]['created_at'] is not None
    assert events[0]['updated_at'] is not None


    event_queue.push("event2", {"key": "value2"})

    events = event_queue.select()

    assert len(events) == 2
    assert events[0]['event'] == "event2"
    assert events[0]['state'] == 0
    assert events[0]['payload'] == {"key": "value2"}
    assert events[0]['transaction_id'] is None
    assert events[0]['created_at'] is not None
    assert events[0]['updated_at'] is not None

    assert events[1]['event'] == "event1"
    assert events[1]['state'] == 1
    assert events[1]['payload'] == {"key": "value1"}
    assert events[1]['transaction_id'] is not None
    assert events[1]['created_at'] is not None
    assert events[1]['updated_at'] is not None

