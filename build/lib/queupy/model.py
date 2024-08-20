import uuid
import time
import json
from datetime import datetime
from .policy import PolicyEventQueue, FIFOEventQueue
import pickle


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


class PostgresMutex:
    def __init__(self, conn, cur, table_name, schema='public'):
        self.conn = conn
        self.cur = cur
        self.table_name = table_name
        self.schema = schema

    def __enter__(self):
        self.cur.execute('BEGIN WORK;')
        self.cur.execute(f'LOCK TABLE {self.schema}."{self.table_name}";')

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cur.execute('COMMIT WORK;')
        self.conn.commit()


class EventQueue:
    """
    A model for a queue table in a database.

    :param event: The event name.
    :param state: The state of the event.
    :param payload: The payload of the event.
    :param created_at: The time the event was created.
    :param updated_at: The time the event was last updated.

    """

    table_name = '_queupy_event'
    schema = 'public'
    conn = None
    callback = None

    @classmethod
    def create_table(cls):
        with cls.conn.cursor() as cur:
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS "{cls.schema}"."{cls.table_name}" (
                    id SERIAL PRIMARY KEY,
                    event TEXT NOT NULL,
                    state INTEGER NOT NULL DEFAULT 0,
                    payload JSONB NOT NULL,
                    transaction_id UUID,
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW()
                );
            """)

    @classmethod
    def push(cls, event : str, payload : dict | list) -> None:
        payload_json = json.dumps(payload)
        with cls.conn.cursor() as cur:
            cur.execute(f"""
                INSERT INTO "{cls.schema}"."{cls.table_name}" (event, payload)
                VALUES (%s, %s::jsonb);
            """, (event, payload_json,))
            if cls.callback:
                cls.callback('push', event)
            cls.conn.commit()

    @classmethod
    def pop(cls, event_name : str, policy : PolicyEventQueue = FIFOEventQueue) -> dict | list:
        transaction_id = uuid.uuid4()
        with cls.conn.cursor() as cur:
            with PostgresMutex(cls.conn, cur, cls.table_name) as mut:
                cur.execute(
                    f"""UPDATE {cls.table_name}
                    SET transaction_id = %s, updated_at = %s, state = 1
                    WHERE event = %s AND state = 0 AND {policy(event_name)};
                    """, (str(transaction_id), datetime.now(), event_name,)
                )
            cls.conn.commit()
            cur.execute(f"""
                SELECT payload FROM {cls.table_name} WHERE transaction_id = %s;
            """, (str(transaction_id),))
            cls.conn.commit()
            result = cur.fetchone()
        if cls.callback:
            cls.callback('pop', event_name)
        if not result:
            raise ExceptionQueueEmpty()
        return result[0]

    @classmethod
    def flush(cls, event_name : str = None) -> None:
        with cls.conn.cursor() as cur:
            if not event_name:
                cur.execute(f"""
                    DELETE FROM {cls.table_name};
                """)
            else:
                cur.execute(f"""
                    DELETE FROM {cls.table_name} WHERE event = %s;
                """, (event_name,))
        cls.conn.commit()

    @classmethod
    def select(cls) -> list:
        with cls.conn.cursor() as cur:
            cur.execute(f"""
                SELECT id, event, state, payload, transaction_id, created_at, updated_at
                FROM {cls.table_name}
                ORDER BY created_at DESC;
            """)
            result = cur.fetchall()
            events = []

            for row in result:
                event = {
                    'id': row[0],
                    'event': row[1],
                    'state': row[2],
                    'payload': row[3],
                    'transaction_id': row[4],
                    'created_at': row[5],
                    'updated_at': row[6]
                }
                events.append(event)

        return events

    @classmethod
    def consume(cls, event: str, frequency: float = 1.0):
        while True:
            try:
                payload = cls.pop(event)
                yield payload
            except ExceptionQueueEmpty:
                pass
            time.sleep(frequency)

    @classmethod
    def produce(cls, generator):
        for event, payload in generator:
            cls.push(event, payload)

    @classmethod
    def length(cls, event : str = None) -> int:
        with cls.conn.cursor() as cur:
            if not event:
                cur.execute(f"""
                    SELECT COUNT(*) FROM {cls.table_name} WHERE state = 0;
                """)
            else:
                cur.execute(f"""
                    SELECT COUNT(*) FROM {cls.table_name} WHERE event = %s and state = 0;
                """, (event,))
            result = cur.fetchone()
        return result[0]
