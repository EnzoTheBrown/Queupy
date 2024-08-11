from queupy import init_queue
from queupy.utils import getLogger
import uuid

logger = getLogger(__name__)


def concat_logs(*args):
    logger.info(' '.join(args))


def main():
    with open(str(uuid.uuid4()) + '.logs', 'w') as f:
        event_queue = init_queue(
            database_name='queupy',
            host='postgres',
            user='queupy',
            password='queupy',
            callback=concat_logs,
        )

        for event in event_queue.consume('test', frequency=0.01):
            logger.info(f"Consuming event {event}")
            f.write(f"{event['i']}\n")


if __name__ == '__main__':
    main()
