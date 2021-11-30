# eWarehousing Solutions Python Library
This library provides convenient access to the eWarehousing Solutions API from applications written in the Python language.


## Documentation
-- Work in progress --


## Installation

```
pip install <coming_soon>
```

### Requirements
- Python 3.7+


## Usage

```python

import EwhsClient from ewhs.client

client = EwhsClient(...)

# list orders
orders = client.order.list()

# get order
order = client.order.get(id)

# create order
order = client.order.create({
    "external_reference": "EXAMPLE_ORD_001",
    ...
})
```


