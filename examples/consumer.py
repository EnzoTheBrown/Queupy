from queupy import init_queue
from queupy.utils import getLogger

logger = getLogger(__name__)


def concat_logs(*args):
    logger.info(' '.join(args))


def main():
    event_queue = init_queue(
        database_name='queupy',
        host='postgres',
        user='queupy',
        password='queupy',
        callback=concat_logs,
    )

    for event in event_queue.consume('test', frequency=1):
        logger.info(f"Consuming event {event}")


if __name__ == '__main__':
    main()
