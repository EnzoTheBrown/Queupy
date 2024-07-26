from .model import EventQueue
from .priority import FIFOEventQueue, LIFOEventQueue
import peewee


def init_queue(
        database_name : str,
        host : str,
        user : str,
        password : str,
        port : int = 5432,
        db_schema : str = 'public',
        db_table_name : str = '_queupy_event_queue',
        priority : peewee.Expression = FIFOEventQueue):
    """
    Initialize a queue table in the database.

    :param database_name: The name of the database to connect to.
    :param host: The host to connect to.
    :param port: The port to connect to.
    :param user: The user to connect as.
    :param password: The password to connect with.
    :param db_schema: The schema to create the table in.
    :param db_table_name: The name of the table to create.
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

        @classmethod
        def pop(cls, event):
            return super().pop(event, priority(cls))

    if not db.table_exists(_EventQueue):
        db.create_tables([_EventQueue])

    return _EventQueue

