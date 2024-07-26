from playhouse.postgres_ext import BinaryJSONField
from datetime import datetime
import peewee
import uuid
import time


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


LOCK_TEMPLATE = """
BEGIN WORK;
LOCK TABLE {table_name};
{query};
COMMIT WORK;
"""

class EventQueue(peewee.Model):
    """
    A model for a queue table in a database.

    :param event: The event name.
    :param state: The state of the event.
    :param payload: The payload of the event.
    :param created_at: The time the event was created.
    :param updated_at: The time the event was last updated.

    """
    event = peewee.CharField()
    state = peewee.IntegerField()
    payload = BinaryJSONField()
    created_at = peewee.DateTimeField(default=datetime.now)
    updated_at = peewee.DateTimeField(default=datetime.now)
    transaction_id = peewee.UUIDField(null=True)

    @classmethod
    def push(cls, event, payload):
        event = cls.create(
            event=event,
            payload=payload,
            state=0,
            created_at=datetime.now()
        )
        return event

    @classmethod
    def execute_lock(cls, query):
        query = query.sql()
        lock_query_string = LOCK_TEMPLATE.format(
            table_name=cls._meta.table_name,
            query=query[0]
        )
        cls._meta.database.execute_sql(lock_query_string, query[1])

    @classmethod
    def pop(cls, event, priority):
        try:
            transaction_id = uuid.uuid4()
            query = cls.update({
                        cls.transaction_id: transaction_id,
                        cls.updated_at: datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        cls.state: 1
                }).where(
                    (cls.event == event) &
                    (cls.state == 0) &
                    priority()
            )
            cls.execute_lock(query)
            event_queue = cls.get(cls.transaction_id == transaction_id)
            return event_queue
        except cls.DoesNotExist:
            raise ExceptionQueueEmpty()

    @classmethod
    def consume(cls, event : str, frequency : float = 1.0):
        while True:
            try:
                payload = cls.pop(event)
                yield payload
            except ExceptionQueueEmpty:
                pass
            time.sleep(frequency)

    def produce(self, generator):
        for event, payload in generator:
            cls.push(event, payload)

