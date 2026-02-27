import warnings
import os

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager

from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from databases import Database

import alembic
from alembic.config import Config
from backend.app.db.repositories.cleanings import CleaningsRepository
from backend.app.models.cleanings import CleaningCreate, CleaninginDb


# Apply migrations at beginning and end of testing session
@pytest.fixture(scope="session")
def apply_migrations():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    os.environ["TESTING"] = "1"
    config = Config("alembic.ini")

    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")


# Create a new application for testing
@pytest.fixture
def app(apply_migrations: None) -> FastAPI:
    from backend.app.api.server import get_application

    return get_application()


# Grab a reference to our database when needed
@pytest.fixture
def db(app: FastAPI) -> Database:
    return app.state._db


# Make requests in our tests
@pytest_asyncio.fixture
async def client(app: FastAPI):
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(
            transport=transport,
            base_url="http://testserver",
            headers={"Content-Type": "application/json"},
        ) as client:
            yield client


@pytest_asyncio.fixture
async def test_cleaning(db: Database) -> CleaninginDb:
    cleaning_repo = CleaningsRepository(db)
    new_cleaning = CleaningCreate(
        name="test cleaning",
        description="test description",
        price=0.00,
        cleaning_type="spot_clean",
    )
    return await cleaning_repo.create_cleaning(new_cleaning=new_cleaning)
