from typing import Optional

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ServerSelectionTimeoutError

from fimed.config import settings
from fimed.logger import logger

_connection: Optional[Database] = None


def get_connection() -> Database:
    """
    Returns -or creates- global database connection.
    """
    global _connection

    if not _connection:
        logger.debug("Connecting to database for the first time")
        client = MongoClient(settings.MONGO_DNS)
        try:
            client.server_info()
        except ServerSelectionTimeoutError:
            raise ConnectionError(f"Could not connect to database with connection string {settings.MONGO_DNS}")
        _connection = client.fimed
    return _connection




