# Queupy

Queupy is a Python library designed to provide a fast and safe message queuing system using PostgreSQL. It creates a dedicated table `_queupy_event` to handle event messages efficiently with both producer and consumer functionalities.

## Features

- Simple initialization and setup
- Efficient event queuing using PostgreSQL
- Easy-to-use producer and consumer interfaces
- Customizable logging for monitoring and debugging

## Installation

To install Queupy, use pip:

```bash
pip install queupy
```

## Usage

### Consumer Example

Below is an example of how to use Queupy to consume events from the queue.

```python
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
```

### Producer Example

Here is an example of how to use Queupy to push events to the queue.

```python
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
```

## Configuration

### Database Configuration

Ensure that your PostgreSQL database is properly configured and accessible. Queupy requires the following parameters for initialization:

- `database_name`: The name of your PostgreSQL database.
- `host`: The host address of your PostgreSQL server.
- `user`: The username to access your PostgreSQL database.
- `password`: The password for the PostgreSQL user.

### Table Schema

Queupy will automatically create the `_queupy_event` table in your specified database. Ensure your database user has the necessary permissions to create and modify tables.

## Logging

Queupy uses a customizable logging system. You can configure the logger to suit your needs for monitoring and debugging.

```python
from queupy.utils import getLogger

logger = getLogger(__name__)
logger.setLevel(logging.INFO)
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, please open an issue on the GitHub repository or contact the maintainer.

---

Happy queuing with Queupy!
