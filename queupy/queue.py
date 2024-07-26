from .model import EventQueue
from .priority import FIFOEventQueue, LIFOEventQueue
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
        priority=FIFOEventQueue,
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

    class _EventQueue(EventQueue):
        table_name = db_table_name
        schema = db_schema

        def pop(cls, event):
            return super().pop(event, priority(cls))

    cur = conn.cursor()
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS "{db_schema}"."{db_table_name}" (
            id SERIAL PRIMARY KEY,
            event TEXT NOT NULL,
            state INTEGER NOT NULL DEFAULT 0,
            payload JSONB NOT NULL,
            transaction_id UUID,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        );
    """)

    return _EventQueue(conn, callback=callback)

