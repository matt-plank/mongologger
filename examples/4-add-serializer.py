"""Sometimes, when you want to keep the serializer definitions separate from
the logger initialization, you may want to add serializers manually.
"""

import os
from dataclasses import dataclass

from mongologger import Logger


# e.g. models/user.py
@dataclass
class User:
    id: int
    username: str
    firstname: str
    lastname: str


# e.g. logging/users.py
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


# e.g. main.py
logger = Logger(
    host=os.environ["MONGO_HOST"],
    port=int(os.environ["MONGO_PORT"]),
    db_name="logs",
    collection_name="logs",
)

logger.add_serializer(User, user_log_serializer)

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
