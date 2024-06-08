import os

from motor.motor_asyncio import AsyncIOMotorClient
from pytest_asyncio import fixture

from mongologger import Logger


@fixture(params=["details", "uri", "collection"])
async def logger(request):
    logger = None

    if request.param == "details":
        logger = Logger(
            host=os.environ["MONGO_HOST"],
            port=int(os.environ["MONGO_PORT"]),
            db_name=os.environ["MONGO_DB"],
            collection_name=os.environ["MONGO_COLLECTION"],
            username=os.environ["MONGO_USER"],
            password=os.environ["MONGO_PASSWORD"],
        )

    if request.param == "uri":
        logger = Logger(
            uri=os.environ["MONGO_URI"],
            db_name=os.environ["MONGO_DB"],
            collection_name=os.environ["MONGO_COLLECTION"],
        )

    if request.param == "collection":
        client = AsyncIOMotorClient(os.environ["MONGO_URI"])
        logger = Logger(
            collection=client[os.environ["MONGO_DB"]][os.environ["MONGO_COLLECTION"]],
        )

    assert logger is not None
    assert logger.collection is not None

    try:
        yield logger
    finally:
        assert logger.collection is not None
        await logger.collection.delete_many({})
