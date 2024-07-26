import uuid
import time
import json
from datetime import datetime


class ExceptionQueueEmpty(Exception):
    """
    Exception raised when the queue is empty.
    """
    pass


class ExceptionQueueColision(Exception):
    """
    Exception raised when a colision is detected.
    """
    pass


class EventQueue:
    """
    A model for a queue table in a database.

    :param event: The event name.
    :param state: The state of the event.
    :param payload: The payload of the event.
    :param created_at: The time the event was created.
    :param updated_at: The time the event was last updated.

    """
    def __init__(self, conn, callback=None):
        self.conn = conn
        self.callback = callback

    def push(self, event, payload):
        payload_json = json.dumps(payload)
        cur = self.conn.cursor()
        cur.execute(f"""
            INSERT INTO "{self.schema}"."{self.table_name}" (event, payload)
            VALUES (%s, %s::jsonb);
        """, (event, payload_json,))
        if self.callback:
            self.callback('push', event)
        self.conn.commit()
        cur.close()

    def pop(self, event_name, priority):
        transaction_id = uuid.uuid4()
        cur = self.conn.cursor()
        cur.execute("BEGIN WORK;")
        cur.execute(f"LOCK TABLE {self.table_name};")
        cur.execute(f"""UPDATE {self.table_name}
        SET transaction_id = %s, updated_at = %s, state = 1
        WHERE event = %s AND state = 0 AND {priority(event_name)};
        """, (str(transaction_id), datetime.now(), event_name,))
        cur.execute(f'COMMIT WORK;')
        self.conn.commit()
        cur.execute(f"""
            SELECT payload FROM {self.table_name} WHERE transaction_id = %s;
        """, (str(transaction_id),))
        self.conn.commit()
        result = cur.fetchone()
        if self.callback:
            self.callback('pop', event_name)
        if not result:
            raise ExceptionQueueEmpty()
        cur.close()
        return result[0]

    def consume(self, event: str, frequency: float = 1.0):
        while True:
            try:
                payload = self.pop(event)
                yield payload
            except ExceptionQueueEmpty:
                pass
            time.sleep(frequency)

    def produce(self, generator):
        for event, payload in generator:
            self.push(event, payload)

