# eWarehousing Solutions Python Library

This library provides convenient access to the eWarehousing Solutions API from applications written in the Python
language.

[![CI](https://github.com/ewarehousing-solutions/ewhs-api-python/actions/workflows/test_and_release.yml/badge.svg)](https://github.com/ewarehousing-solutions/ewhs-api-python/actions/workflows/test_and_release.yml)
[![PyPI](https://img.shields.io/pypi/v/ewhs-api-python)](https://pypi.org/project/ewhs-api-python/)


## Documentation

https://api.docs.ewarehousing-solutions.com/


## Installation

```
pip install ewhs-api-python
```

### Requirements

- Python 3.7+

## Usage

```python

from ewhs.client import EwhsClient

client = EwhsClient(...)

# list orders
orders = client.order.list()

# get order
order = client.order.get(id)

# create order
order = client.order.create({
    "external_reference": "EXAMPLE_ORD_001",
    # ...
})
```

## Development

This project is managed using the tool [Poetry](https://github.com/python-poetry/poetry). Poetry is a tool for
dependency management and packaging in Python.

Make sure to install Poetry

```shell
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

Install dependencies

```shell
poetry install
```

Running tests

```shell
poetry run pytest
```

# Support
[www.ewarehousing-solutions.nl](https://ewarehousing-solutions.nl/) — info@ewarehousing-solutions.nl
