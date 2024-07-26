from queupy import init_queue
from queupy.utils import getLogger

logger = getLogger(__name__)

def main():
    event_queue = init_queue(
        database_name='queupy',
        host='localhost',
        user='queupy',
        password='queupy',
    )

    for event in event_queue.consume('test', frequency=0.01):
        logger.info(f"Consuming event {event}")


if __name__ == '__main__':
    main()
