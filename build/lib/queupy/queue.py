from .model import EventQueue
from .policy import FIFOEventQueue, LIFOEventQueue
from queupy.utils import getLogger
import psycopg2

logger = getLogger(__name__)


def init_queue(
        database_name: str,
        host: str,
        user: str,
        password: str,
        port: int = 5432,
        db_schema: str = 'public',
        db_table_name: str = '_queupy_event',
        policy=FIFOEventQueue,
        callback : callable = None):
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
    conn = psycopg2.connect(
        dbname=database_name,
        host=host,
        user=user,
        password=password,
        port=port
    )
    _callback = callback
    _conn = conn

    class _EventQueue(EventQueue):
        table_name = db_table_name
        schema = db_schema
        conn = _conn
        callback = _callback

        @classmethod
        def pop(cls, event):
            return super().pop(event, policy(cls))

    _EventQueue.create_table()

    return _EventQueue

