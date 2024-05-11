import pytest

from mongologger import Logger


@pytest.mark.asyncio
async def test_debug(logger: Logger):
    await logger.a_debug(message="This is a debug message")


@pytest.mark.asyncio
async def test_info(logger: Logger):
    await logger.a_info(message="This is an info message")


@pytest.mark.asyncio
async def test_warning(logger: Logger):
    await logger.a_warning(message="This is a warning message")


@pytest.mark.asyncio
async def test_error(logger: Logger):
    await logger.a_error(message="This is an error message")


@pytest.mark.asyncio
async def test_exception(logger: Logger):
    try:
        raise ValueError("This is an exception")
    except ValueError as e:
        await logger.a_exception(e, message="This is an exception message")
