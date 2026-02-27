import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_CONTENT,
    HTTP_200_OK,
)

from backend.app.models.cleanings import CleaningCreate, CleaninginDb


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

    async def test_invalid_input_raises_error(
        self, app: FastAPI, client: AsyncClient
    ) -> None:
        res = await client.post(app.url_path_for("cleanings:create_cleaning"), json={})
        assert res.status_code == HTTP_422_UNPROCESSABLE_CONTENT


class TestCreateCleaning:
    async def test_valid_input_creates_cleaning(
        self, app: FastAPI, client: AsyncClient, new_cleaning: CleaningCreate
    ) -> None:
        # We pass the dict directly, NOT wrapped in a "new_cleaning" key
        res = await client.post(
            app.url_path_for("cleanings:create_cleaning"),
            json={"new_cleaning": new_cleaning.model_dump()},
        )
        assert res.status_code == HTTP_201_CREATED

        # Two-way validation!
        created_cleaning = CleaningCreate.model_validate(res.json())
        assert created_cleaning == new_cleaning

    @pytest.mark.parametrize(
        "invalid_payload,status_code",
        (
            (None, HTTP_422_UNPROCESSABLE_CONTENT),
            ({}, HTTP_422_UNPROCESSABLE_CONTENT),
            ({"name": "test cleaning"}, HTTP_422_UNPROCESSABLE_CONTENT),
            ({"description": "test description"}, HTTP_422_UNPROCESSABLE_CONTENT),
            ({"price": 0.00}, HTTP_422_UNPROCESSABLE_CONTENT),
            ({"cleaning_type": "spot_clean"}, HTTP_422_UNPROCESSABLE_CONTENT),
            (
                {"name": "test cleaning", "cleaning_type": "spot_clean"},
                HTTP_422_UNPROCESSABLE_CONTENT,
            ),
            (
                {"price": "NORMAL PRICE", "cleaning_type": "spot_clean"},
                HTTP_422_UNPROCESSABLE_CONTENT,
            ),
        ),
    )
    async def test_invalid_cleaning_type_raises_error(
        self, app: FastAPI, client: AsyncClient, invalid_payload, status_code
    ) -> None:
        res = await client.post(
            app.url_path_for("cleanings:create_cleaning"),
            json={"new_cleaning": invalid_payload},
        )
        assert res.status_code == status_code


class TestGetCleaning:
    async def test_get_cleaning_by_id(
        self, app: FastAPI, client: AsyncClient, test_cleaning
    ):
        res = await client.get(
            app.url_path_for("cleanings:get_cleaning_by_id", id=test_cleaning.ID)
        )

        assert res.status_code == HTTP_200_OK
        cleaning = CleaninginDb.model_validate(res.json())
        assert cleaning.ID == test_cleaning.ID

    @pytest.mark.parametrize(
        "invalid_id,status_code",
        (
            (9999, HTTP_404_NOT_FOUND),
            (500, HTTP_404_NOT_FOUND),
            (-1, HTTP_404_NOT_FOUND),
            ("invalid_id", HTTP_422_UNPROCESSABLE_CONTENT),
            (None, HTTP_422_UNPROCESSABLE_CONTENT),
        ),
    )
    async def test_get_cleaning_by_id_with_invalid_id(
        self, app: FastAPI, client: AsyncClient, invalid_id: int, status_code
    ):
        res = await client.get(
            app.url_path_for("cleanings:get_cleaning_by_id", id=invalid_id)
        )
        assert res.status_code == status_code
