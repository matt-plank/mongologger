"""In it's simplest form, the logger can be used to log messages with different levels of severity.

The kwargs are arbitrary, and can be supplied however is best for your project.
e.g. You could use "dir" instead of "location", or "msg" instead of "message".
"""

import os

from mongologger import Logger

logger = Logger(
    host=os.environ["MONGO_HOST"],
    port=int(os.environ["MONGO_PORT"]),
    db_name="logs",
    collection_name="logs",
)

logger.debug(message="This is a debug message")
logger.info(message="This is an info message")
logger.warning(message="This is a warning message", detail="This is an arbitrary detail")
logger.error(message="This is an error message", location="arbitrary/simple.py", detail="This is an arbitrary detail")
