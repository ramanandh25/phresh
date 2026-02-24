# backend/app/core/tasks.py
from fastapi import FastAPI
from backend.app.db.tasks import connect_to_db, close_db_connection


async def startup(app: FastAPI) -> None:
    """
    Application startup logic.
    """
    await connect_to_db(app)


async def shutdown(app: FastAPI) -> None:
    """
    Application shutdown logic.
    """
    await close_db_connection(app)

