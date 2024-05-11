import asyncio
import os

from pytest import fixture

from mongologger import Logger


@fixture
def logger() -> Logger:
    return Logger(
        host=os.environ["MONGO_HOST"],
        port=int(os.environ["MONGO_PORT"]),
        db_name=os.environ["MONGO_DB"],
        collection_name=os.environ["MONGO_COLLECTION"],
        username=os.environ["MONGO_USER"],
        password=os.environ["MONGO_PASSWORD"],
    )
