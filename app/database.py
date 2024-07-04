from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore[import-untyped]
from motorhead import AgnosticClient, AgnosticDatabase


@lru_cache(maxsize=1)
def get_database() -> AgnosticDatabase:
    """Database provider dependency for the application."""
    mongo_connection_string = "mongodb://127.0.0.1:27017"
    database_name = "smartnow-db"
    client: AgnosticClient = AsyncIOMotorClient(mongo_connection_string)
    return client[database_name]
