# Mongologger

Logging with files doesn't scale well: they're hard to search, filter, and aggregate.

Mongologger is a simple async logging library for Python into MongoDB. It's easy to use and easy to extend, giving you scalable, production ready logs.

The sooner you integrate scalable, document-based logging into your application, the more time you save down the road.

## Quick Start

Install with pip

```bash
pip install git@github.com:matt-plank/mongologger.git
```

Create a logging client

```python
from mongologger import Logger

logger = Logger(
    host='localhost',
    port=27017,
    db_name='logs',
    collection_name='log'
)
```

Interface consistent with what you're used to.

```python
logger.debug(message="Debug message")
logger.info(message="Hello, World!")
logger.warning(message="User might be up to no good", user=bad_user)
logger.error(message="Something went wrong")

try:
    risky_function()
except Exception as e:
    logger.exception(e)
```

Use the `__mongo__` method to add easy serialization to your classes.

```python
class MyCustomUser:
    id: int
    username: str
    email: str
    firstname: str  # Want to combine this with lastname
    lastname: str
    age: int
    password_hash: str  # Do not want to include this in logs

    def __mongo__(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": {
                "first": self.firstname,
                "last": self.lastname
            },
            "email": self.email,
            "age": self.age
        }


logger.info(user=MyCustomUser(...))
```

Write simple serializers for external classes that you can't control.

```python
from external_package import ExternalUser

from .config import logger

def external_user_serializer(user: ExternalUser):
    return {
        "id": user.id,
        "username": user.username,
        "name": {
            "first": user.firstname,
            "last": user.lastname
        },
        "email": user.email,
        "age": user.age
    }

logger.add_serializer(ExternalUser, external_user_serializer)


logger.info(external_user=some_external_user)
```

Or use the decorator

```python
@logger.serializer(ExternalUser)
def external_user_serializer(user: ExternalUser):
    return {
        "id": user.id,
        "username": user.username,
        "name": {
            "first": user.firstname,
            "last": user.lastname
        },
        "email": user.email,
        "age": user.age
    }
```
