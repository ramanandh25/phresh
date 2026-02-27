from fastapi import FastAPI
from databases import Database
from backend.app.core.config import DATABASE_URL, DB_MIN_CONNECTIONS, DB_MAX_CONNECTIONS
import logging
import os


logger = logging.getLogger(__name__)


async def connect_to_db(app: FastAPI) -> None:
    """
    Connect to the database when the application starts.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    try:
        DB_URL = (
            f"{DATABASE_URL}_test" if os.environ.get("TESTING") == "1" else DATABASE_URL
        )
        database = Database(
            DB_URL, min_size=DB_MIN_CONNECTIONS, max_size=DB_MAX_CONNECTIONS
        )
        await database.connect()
        app.state._db = database
        logger.info("Successfully connected to the database.")
    except Exception as e:
        logger.error(f"Failed to connect to the database: {e}")


async def close_db_connection(app: FastAPI) -> None:
    """
    Close the database connection when the application shuts down.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    try:
        database: Database = app.state._db
        await database.disconnect()
        logger.info("Successfully disconnected from the database.")
    except Exception as e:
        logger.error(f"Failed to disconnect from the database: {e}")
