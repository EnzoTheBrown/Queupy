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

    for i in range(1000):
        logger.info(f"Pushing event {i}")
        event_queue.push('test', {'i': i})


if __name__ == '__main__':
    main()
