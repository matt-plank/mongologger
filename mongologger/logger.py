import asyncio
import traceback
from datetime import datetime
from typing import Any, Callable, Type

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection


class Logger:
    """MongoDB async logger."""

    def __init__(self, host: str, port: int, db_name: str, collection_name: str):
        """Initialise with a PyMongo collection."""
        self.host = host
        self.port = port
        self.db_name = db_name
        self.collection_name = collection_name

        self.uri = f"mongodb://{self.host}:{self.port}/"
        self.client = AsyncIOMotorClient(self.uri)
        self.collection: AsyncIOMotorCollection = self.client[self.db_name][self.collection_name]

        self.serializers: dict[Type, Callable] = {}

    def serializer(self, kwarg_type: Type) -> Callable:
        """Decorator to add a serializer for a kwarg."""

        def wrapper(serializer: Callable) -> Callable:
            self.add_serializer(kwarg_type, serializer)
            return serializer

        return wrapper

    def add_serializer(self, kwarg_type: Type, serializer: Callable) -> None:
        """Add a serializer for a kwarg."""
        if not isinstance(kwarg_type, type):
            raise ValueError("kwarg_type must be a type.")

        if not callable(serializer):
            raise ValueError("Serializer must be a callable.")

        self.serializers[kwarg_type] = serializer

    async def _insert_document(self, document: dict[str, Any]) -> None:
        """Insert a document to mongo (separated for better control)."""
        await self.collection.insert_one(document)

    async def _write(self, **kwargs) -> None:
        """Write a single log to the log backend."""
        time = datetime.utcnow()
        self._serialize_kwargs(kwargs)

        await self._insert_document(
            {
                "timestamp": time,
                **kwargs,
            }
        )

    def _serialize_kwargs(self, kwargs: dict[str, Any]):
        """In-place serialization of kwargs."""
        for kwarg in kwargs:
            if hasattr(kwargs[kwarg], "__mongo__") and callable(kwargs[kwarg].__mongo__):
                kwargs[kwarg] = kwargs[kwarg].__mongo__()
            elif kwarg in self.serializers:
                kwargs[kwarg] = self.serializers[kwarg](kwargs[kwarg])

    def debug(self, **kwargs) -> None:
        """Write a log at the DEBUG level."""
        asyncio.create_task(self._write(level="DEBUG", **kwargs))

    def info(self, **kwargs) -> None:
        """Write a log at the INFO level."""
        asyncio.create_task(self._write(level="INFO", **kwargs))

    def warning(self, **kwargs) -> None:
        """Write a log at the WARNING level."""
        asyncio.create_task(self._write(level="WARNING", **kwargs))

    def error(self, **kwargs) -> None:
        """Write a log at the ERROR level."""
        asyncio.create_task(self._write(level="ERROR", **kwargs))

    def exception(self, exception: Exception, **kwargs) -> None:
        """Write a log at the ERROR level with an exception."""
        asyncio.create_task(
            self._write(
                level="EXCEPTION",
                exception={
                    "type": type(exception).__name__,
                    "message": str(exception),
                    "traceback": traceback.format_exc(),
                },
                **kwargs,
            )
        )
