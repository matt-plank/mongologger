import pytest

from mongologger import Logger


@pytest.mark.asyncio
async def test_debug(logger: Logger):
    await logger.debug(message="This is a debug message")

    assert logger.collection is not None

    doc = await logger.collection.find_one({"level": "DEBUG"})

    assert doc is not None
    assert doc["message"] == "This is a debug message"


@pytest.mark.asyncio
async def test_info(logger: Logger):
    await logger.info(message="This is an info message")

    assert logger.collection is not None

    doc = await logger.collection.find_one({"level": "INFO"})

    assert doc is not None
    assert doc["message"] == "This is an info message"


@pytest.mark.asyncio
async def test_warning(logger: Logger):
    await logger.warning(message="This is a warning message")

    assert logger.collection is not None

    doc = await logger.collection.find_one({"level": "WARNING"})

    assert doc is not None
    assert doc["message"] == "This is a warning message"


@pytest.mark.asyncio
async def test_error(logger: Logger):
    await logger.error(message="This is an error message")

    assert logger.collection is not None

    doc = await logger.collection.find_one({"level": "ERROR"})

    assert doc is not None
    assert doc["message"] == "This is an error message"


@pytest.mark.asyncio
async def test_exception(logger: Logger):
    try:
        raise ValueError("This is an exception")
    except ValueError as e:
        await logger.exception(e, message="This is an exception message")

    assert logger.collection is not None

    doc = await logger.collection.find_one({"level": "EXCEPTION"})

    assert doc is not None
    assert doc["exception"] is not None
    assert doc["exception"]["type"] == "ValueError"
    assert doc["exception"]["message"] == "This is an exception"
    assert doc["exception"]["traceback"] is not None
