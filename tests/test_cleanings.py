import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_CONTENT,
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
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
        res = await client.post(app.url_path_for("cleanings:create-cleaning"), json={})
        assert res.status_code != HTTP_404_NOT_FOUND

    async def test_invalid_input_raises_error(
        self, app: FastAPI, client: AsyncClient
    ) -> None:
        res = await client.post(app.url_path_for("cleanings:create-cleaning"), json={})
        assert res.status_code == HTTP_422_UNPROCESSABLE_CONTENT


class TestCreateCleaning:
    async def test_valid_input_creates_cleaning(
        self, app: FastAPI, client: AsyncClient, new_cleaning: CleaningCreate
    ) -> None:
        # We pass the dict directly, NOT wrapped in a "new_cleaning" key
        res = await client.post(
            app.url_path_for("cleanings:create-cleaning"),
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
            app.url_path_for("cleanings:create-cleaning"),
            json={"new_cleaning": invalid_payload},
        )
        assert res.status_code == status_code


class TestGetCleaning:
    async def test_get_cleaning_by_id(
        self, app: FastAPI, client: AsyncClient, test_cleaning: CleaninginDb
    ):
        res = await client.get(
            app.url_path_for("cleanings:get-cleaning-by-id", id=test_cleaning.id)
        )

        assert res.status_code == HTTP_200_OK
        cleaning = CleaninginDb.model_validate(res.json())
        assert cleaning.id == test_cleaning.id

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
            app.url_path_for("cleanings:get-cleaning-by-id", id=invalid_id)
        )
        assert res.status_code == status_code

    async def test_get_all_cleanings(
        self, app: FastAPI, client: AsyncClient, test_cleaning: CleaninginDb
    ):
        res = await client.get(app.url_path_for("cleanings:get-all-cleanings"))
        assert res.status_code == HTTP_200_OK
        assert isinstance(res.json(), list)
        cleanings = [CleaninginDb.model_validate(cleaning) for cleaning in res.json()]
        assert test_cleaning in cleanings


class TestUpdateCleaning:
    @pytest.mark.parametrize(
        "attrs_to_update,values_to_update",
        (
            (["name"], ["fake updated name"]),
            (["description"], ["fake updated description"]),
            (["price"], [100.00]),
            (["cleaning_type"], ["full_clean"]),
            (
                ["name", "description"],
                ["fake updated name", "fake updated description"],
            ),
            (["name", "price"], ["fake updated name", 100.00]),
            (["name", "cleaning_type"], ["fake updated name", "full_clean"]),
            (["description", "price"], ["fake updated description", 100.00]),
            (
                ["description", "cleaning_type"],
                ["fake updated description", "full_clean"],
            ),
            (["price", "cleaning_type"], [100.00, "full_clean"]),
        ),
    )
    async def test_update_cleaning(
        self,
        app: FastAPI,
        client: AsyncClient,
        test_cleaning: CleaninginDb,
        attrs_to_update,
        values_to_update,
    ):
        update_json = dict(zip(attrs_to_update, values_to_update))
        res = await client.put(
            app.url_path_for("cleanings:update-cleaning", id=test_cleaning.id),
            json={"cleaning_update": update_json},
        )

        assert res.status_code == HTTP_200_OK
        updated_cleaning = CleaninginDb.model_validate(res.json())
        assert updated_cleaning.id == test_cleaning.id

        for attr, value in update_json.items():
            assert getattr(updated_cleaning, attr) == value
            assert getattr(test_cleaning, attr) != value

        for key, value in updated_cleaning.model_dump().items():
            if key not in update_json:
                assert getattr(test_cleaning, key) == value

    @pytest.mark.parametrize(
        "id,payload,status_code",
        (
            (9999, {"name": "fake updated name"}, HTTP_404_NOT_FOUND),
            (200, {"name": "UR CLEANINGSS"}, HTTP_404_NOT_FOUND),
            (0, {"name": "fake updated name"}, HTTP_422_UNPROCESSABLE_CONTENT),
            (-1, {"name": "fake updated name"}, HTTP_422_UNPROCESSABLE_CONTENT),
            (
                "invalid_id",
                {"name": "fake updated name"},
                HTTP_422_UNPROCESSABLE_CONTENT,
            ),
            (None, {"name": "fake updated name"}, HTTP_422_UNPROCESSABLE_CONTENT),
            (
                1,
                {"cleaning_type": "invalid_cleaning_type"},
                HTTP_422_UNPROCESSABLE_CONTENT,
            ),
            (1, {"price": "invalid_price"}, HTTP_422_UNPROCESSABLE_CONTENT),
            (1, {"cleaning_type": None}, HTTP_400_BAD_REQUEST),
        ),
    )
    async def test_update_cleaning_with_invalid_input(
        self, app: FastAPI, client: AsyncClient, id, payload, status_code
    ):
        res = await client.put(
            app.url_path_for("cleanings:update-cleaning", id=id),
            json={"cleaning_update": payload},
        )

        assert res.status_code == status_code


class TestDeleteCleaning:
    async def test_delete_successful(
        self, app: FastAPI, client: AsyncClient, test_cleaning: CleaninginDb
    ) -> None:
        res = await client.delete(
            app.url_path_for("cleanings:delete-cleaning-by-id", id=test_cleaning.id)
        )
        assert res.status_code == HTTP_200_OK

        res = await client.get(
            app.url_path_for("cleanings:get-cleaning-by-id", id=test_cleaning.id)
        )

        assert res.status_code == HTTP_404_NOT_FOUND

    @pytest.mark.parametrize(
        "id,status_code",
        (
            (500, HTTP_404_NOT_FOUND),
            (0, HTTP_422_UNPROCESSABLE_CONTENT),
            (-1, HTTP_422_UNPROCESSABLE_CONTENT),
            (None, HTTP_422_UNPROCESSABLE_CONTENT),
        ),
    )
    async def test_delete_invalid_ids(
        self, app: FastAPI, client: AsyncClient, id, status_code
    ) -> None:
        res = await client.delete(
            app.url_path_for("cleanings:delete-cleaning-by-id", id=id)
        )

        assert res.status_code == status_code
