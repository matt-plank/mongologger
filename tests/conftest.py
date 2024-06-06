import os

from motor.motor_asyncio import AsyncIOMotorClient
from pytest import fixture

from mongologger import Logger


@fixture(params=["details", "uri"])
def logger_from_details(request) -> Logger:
    if request.param == "details":
        return Logger(
            host=os.environ["MONGO_HOST"],
            port=int(os.environ["MONGO_PORT"]),
            db_name=os.environ["MONGO_DB"],
            collection_name=os.environ["MONGO_COLLECTION"],
            username=os.environ["MONGO_USER"],
            password=os.environ["MONGO_PASSWORD"],
        )

    if request.param == "uri":
        return Logger(
            uri=os.environ["MONGO_URI"],
            db_name=os.environ["MONGO_DB"],
            collection_name=os.environ["MONGO_COLLECTION"],
        )

    if request.param == "collection":
        client = AsyncIOMotorClient(os.environ["MONGO_URI"])
        return Logger(
            collection=client[os.environ["MONGO_DB"]][os.environ["MONGO_COLLECTION"]],
        )

    assert False, "Invalid param"
