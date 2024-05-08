"""In the case that you want to log classes that you don't have control over,
or don't want to couple to your logging, you can use the serializer decorators.

This allows you to define how a class should be serialized for logging, without modifying the class itself.
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


@logger.serializer(User)
def user_log_serializer(user: User):
    return {
        "id": user.id,
        "username": user.username,
        "name": {
            "first": user.firstname,
            "last": user.lastname,
            "full": f"{user.firstname} {user.lastname}",
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
