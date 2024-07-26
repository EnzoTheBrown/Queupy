# Queupy

Queupy is a Python library designed to provide a fast and safe message queuing system using PostgreSQL. It creates a dedicated table `_queupy_event` to handle event messages efficiently with both producer and consumer functionalities.

## Features

- Simple initialization and setup (no need for additional services)
- Efficient event queuing using PostgreSQL
- Easy-to-use producer and consumer interfaces for event handling

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

event_queue = init_queue(
    database_name='queupy',
    host='localhost',
    user='queupy',
    password='queupy',
)

for event in event_queue.consume('test', frequency=0.01):
    print(f"Consuming event {event}")

```

### Producer Example

Here is an example of how to use Queupy to push events to the queue.

```python
from queupy import init_queue


event_queue = init_queue(
    database_name='queupy',
    host='localhost',
    user='queupy',
    password='queupy',
)

for i in range(1000):
    event_queue.push('test', {'i': i})

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


id    | event | state |  payload   |            transaction_id            |         created_at         |         updated_at         
------|-------|-------|------------|--------------------------------------|----------------------------|----------------------------
 7148 | test  |     0 | {"i": 58}  |                                      | 2024-07-26 17:20:51.34825  | 2024-07-26 17:20:51.34825
    2 | test  |     1 | {"i": 1}   | 8000142a-42b9-4656-8518-81e3ee6bd20b | 2024-07-26 14:06:22.596648 | 2024-07-26 16:15:56.322857
    3 | test  |     1 | {"i": 2}   | a6e8b353-c53d-48fb-b8b0-5a972648b384 | 2024-07-26 14:06:22.598692 | 2024-07-26 16:15:57.381679
    

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, please open an issue on the GitHub repository or contact the author at [enzo.the@gmail.com]

---

Happy queuing with Queupy!
