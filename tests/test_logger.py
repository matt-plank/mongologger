import pytest

from mongologger import Logger


@pytest.mark.asyncio
async def test_debug(logger_from_details: Logger):
    await logger_from_details.a_debug(message="This is a debug message")


@pytest.mark.asyncio
async def test_info(logger_from_details: Logger):
    await logger_from_details.a_info(message="This is an info message")


@pytest.mark.asyncio
async def test_warning(logger_from_details: Logger):
    await logger_from_details.a_warning(message="This is a warning message")


@pytest.mark.asyncio
async def test_error(logger_from_details: Logger):
    await logger_from_details.a_error(message="This is an error message")


@pytest.mark.asyncio
async def test_exception(logger_from_details: Logger):
    try:
        raise ValueError("This is an exception")
    except ValueError as e:
        await logger_from_details.a_exception(e, message="This is an exception message")
