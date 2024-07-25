from playhouse.postgres_ext import BinaryJSONField
from datetime import datetime
import peewee


class EventQueue(peewee.Model):
    """
    A model for a queue table in a database.
    """
    event = peewee.CharField()
    state = peewee.IntegerField()
    payload = BinaryJSONField()
    created_at = peewee.DateTimeField(default=datetime.now)
    updated_at = peewee.DateTimeField(default=datetime.now)

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
    def pop(cls, event):
        try:
            event = cls.select().where(
                    (cls.event == event) &
                    (cls.state == 0) &
                    (cls.created_at <= (
                        cls.select(peewee.fn.MIN(cls.created_at)).where(
                            (cls.event == event) &
                            (cls.state == 0)
                        )
                    ))
            ).get()
            event.state = 1
            event.updated_at = datetime.now()
            event.save()
            return event
        except cls.DoesNotExist:
            raise ExceptionQueueEmpty()


class ExceptionQueueEmpty(Exception):
    """
    Exception raised when the queue is empty.
    """
    pass


def init_queue(
        database_name : str,
        host : str,
        port : int,
        user : str,
        password : str,
        db_schema : str = 'public',
        db_table_name : str = '_queupy_event_queue'):
    """
    Initialize a queue table in the database.

    :param database_name: The name of the database to connect to.
    :param host: The host to connect to.
    :param port: The port to connect to.
    :param user: The user to connect as.
    :param password: The password to connect with.
    :param schema: The schema to create the table in.
    :param table_name: The name of the table to create.
    :return: The Queue model.
    """

    db = peewee.PostgresqlDatabase(
        database_name,
        host=host,
        port=port,
        user=user,
        password=password
    )

    class _EventQueue(EventQueue):
        class Meta:
            database = db
            schema = db_schema
            table_name = db_table_name

    if not db.table_exists(_EventQueue):
        db.create_tables([_EventQueue])

    return _EventQueue

