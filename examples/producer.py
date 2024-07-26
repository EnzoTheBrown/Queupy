from queupy import init_queue
from queupy.utils import getLogger
import time

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

    for i in range(1000):
        logger.info(f"Pushing event {i}")
        event_queue.push('test', {'i': i})
        time.sleep(1)


if __name__ == '__main__':
    main()
