# ZDK

## Installation
Install zdk release via pip

```pip install zdk```

## How to use
To use zdk , you must import its client and tell what API you are going to use:
```jason=
from zdk import client
api = client("api_name")
api.funciont_api(**data)
```
Now when you have an API resource, you can make request and process from the API. To use the API resource you must to send through its functions the data  request object represented by a dictionary.
```jason=
api.funciont_api(**data)
```