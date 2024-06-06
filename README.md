# Distributed Key-Value In-Memory Storage

Welcome to the repository for the **Distributed Key-Value In-Memory Storage** project. This project is developed as a course work for the **MTDS** class. More detailed description will be added soon.

## Project Overview

This repository contains a distributed key-value in-memory storage system, designed to provide efficient and scalable data storage solutions. The system is built using Python and leverages the power of distributed computing to handle large volumes of data with minimal latency.

## Authors

- **Olha Mishchuk**
- **Oleksandr Horovyi**

## Documentation

For detailed information about the project's design and implementation, please refer to the [Design Document](https://docs.google.com/document/d/1XD8Jmv1R3rU5i7TODRxDkQDlvKBmiipOmU6FJeioUWg/edit?usp=sharing).

## Features


## Getting Started

### Prerequisites

1. Install python 3.10 from https://python.org or use [pipenv](https://pipenv.pypa.io/en/latest/) 
2. Install poetry from the [official website](https://python-poetry.org/docs/#installation)
3. Change your working directory to one of the three desired poetry projects:
   - `cd client`
   - `cd master`
   - `cd slave`
4. Execute `poetry install` command to install all dependencies

Optionally you may omit steps above, if you have docker and 
docker-compose installed. Simply run `docker-compose up` to 
start the project

### How to use

1. For the `master` service:
   - `cd master`
   - `poetry run python server.py` to launch master/coordinator service
   - `poetry run pytest` to run tests
2. For the `slave` service :
   - `cd slave`
   - `poetry run python slave/edge_node.py` to launch slave service
   - `poetry run pytest` to run tests
3. To work with client code:
   - `cd client`
   - Now you may [create python scripts using client library](#client-library-usage-example)
   - Or you may run tests via `poetry run pytest`


### Client library usage example:
```python
from client.database_client import DatabaseClient


db = DatabaseClient("http://localhost:5000")

db.set("test_key", "test_value")

# Prints "test_value", even on any other machines
print(db.get("test_key"))
```