import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_CONTENT

from backend.app.models.cleanings import CleaningCreate #

# This applies @pytest.mark.asyncio to every test in this file automatically
pytestmark = pytest.mark.asyncio  

@pytest.fixture
def new_cleaning():
    return CleaningCreate(
        name="test cleaning",
        description="test description",
        price=0.00,
        cleaning_type="spot_clean",
    )

class TestCleaningsRoutes:
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for("cleanings:create_cleaning"), json={})
        assert res.status_code != HTTP_404_NOT_FOUND

    async def test_invalid_input_raises_error(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for("cleanings:create_cleaning"), json={})
        # Note: Changed to UNPROCESSABLE_ENTITY (422) which is the standard
        assert res.status_code == HTTP_422_UNPROCESSABLE_CONTENT


class TestCreateCleaning:
    async def test_valid_input_creates_cleaning(
        self, app: FastAPI, client: AsyncClient, new_cleaning: CleaningCreate
    ) -> None:
        # We pass the dict directly, NOT wrapped in a "new_cleaning" key
        res = await client.post(
            app.url_path_for("cleanings:create_cleaning"), 
            json={"new_cleaning":new_cleaning.model_dump()}
        )
        assert res.status_code == HTTP_201_CREATED

        # Two-way validation!
        created_cleaning = CleaningCreate.model_validate(res.json())
        assert created_cleaning == new_cleaning