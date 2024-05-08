"""Sometimes you might have custom classes, for example database models, that you want to include in your logs.

This can be done using the __mongo__ method, giving you full control over how the object is represented in the log.
"""

import os
from dataclasses import dataclass

from mongologger import Logger

logger = Logger(
    host=os.environ["MONGO_HOST"],
    port=int(os.environ["MONGO_PORT"]),
    db_name="logs",
    collection_name="logs",
)


@dataclass
class User:
    id: int
    username: str
    firstname: str
    lastname: str

    def __mongo__(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": {
                "first": self.firstname,
                "last": self.lastname,
                "full": f"{self.firstname} {self.lastname}",
            },
        }


new_user = User(
    id=1,
    username="test",
    firstname="Test",
    lastname="User",
)


logger.info(
    event="new-user",
    detail="manual",
    user=new_user,
)
