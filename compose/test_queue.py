import pytest
import time
from queupy import init_queue, FIFOEventQueue, LIFOEventQueue
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

    event_queue.pop("event1")

    cur.execute(f"SELECT * FROM {event_queue.table_name} WHERE state = 0")
    conn.commit()
    result = cur.fetchall()
    assert len(result) == 0
    cur.close()

