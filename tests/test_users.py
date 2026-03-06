import pytest
from httpx import AsyncClient
from databases import Database
from fastapi import FastAPI
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_422_UNPROCESSABLE_CONTENT,
)
from backend.app.models.users import UserCreate, UserUpdate, UserInDB
from backend.app.db.repositories.users import UsersRepository
from backend.app.services import auth_service


pytestmark = pytest.mark.asyncio


class TestUsersRoutes:
    async def test_route_exist(self, app: FastAPI, client: AsyncClient) -> None:
        new_user = {
            "email": "test@email.io",
            "username": "test_username",
            "password": "TestPassword@123",
        }
        res = await client.post(
            app.url_path_for("users:register-new-user"), json={"new_user": new_user}
        )
        assert res.status_code != HTTP_404_NOT_FOUND


class TestUserRegistration:
    async def test_users_can_register_successfully(
        self, app: FastAPI, client: AsyncClient, db: Database
    ) -> None:

        user_repository = UsersRepository(db=db)
        new_user = {
            "email": "shakira@shakira.io",
            "username": "shakirashakira",
            "password": "Chantaje@124",
        }
        user_in_db = await user_repository.get_user_by_email(
            email=new_user.get("email")
        )
        assert user_in_db is None
        res = await client.post(
            app.url_path_for("users:register-new-user"), json={"new_user": new_user}
        )

        assert res.status_code == HTTP_201_CREATED

        user_in_db = await user_repository.get_user_by_email(email=new_user["email"])
        assert user_in_db is not None
        assert user_in_db.email == new_user["email"]
        assert user_in_db.username == new_user["username"]

        #created_user = UserInDB(
        #    **res.json(), password="random", salt="random"
        #).model_dump(exclude={"password", "salt"})
        created_user = UserInDB(**res.json(),password="Pavan@1234").model_dump(exclude = {"password"})

        assert created_user == user_in_db.model_dump(exclude={"password"})

    @pytest.mark.parametrize(
        "attr,value,status_code",
        [
            ("password", "short", HTTP_422_UNPROCESSABLE_CONTENT),
            ("username", "ram@%#", HTTP_422_UNPROCESSABLE_CONTENT),
            ("username", "jin", HTTP_422_UNPROCESSABLE_CONTENT),
            ("email", "ram123", HTTP_422_UNPROCESSABLE_CONTENT),
        ],
    )
    async def test_user_registration_fail_validation_error(
        self, app: FastAPI, client: AsyncClient, attr: str, value: str, status_code
    ) -> None:

        new_user = {
            "email": "random@mail.io",
            "username": "randomuser",
            "password": "Thisispassord@123",
        }
        new_user[attr] = value

        res = await client.post(
            app.url_path_for("users:register-new-user"), json={"new_user": new_user}
        )

        assert res.status_code == status_code

    @pytest.mark.parametrize(
        "attr,value,status_code",
        [
            ("email", "shakira@shakira.io", HTTP_400_BAD_REQUEST),
            ("username", "shakirashakira", HTTP_400_BAD_REQUEST),
        ],
    )
    async def test_user_registration_fail_when_credentials_exist(
        self, app: FastAPI, client: AsyncClient, attr: str, value: str, status_code
    ) -> None:

        new_user = {
            "username": "randomname",
            "email": "newmail@mail.io",
            "password": "NewPass@1234",
        }

        new_user[attr] = value

        res = await client.post(
            app.url_path_for("users:register-new-user"), json={"new_user": new_user}
        )

        assert res.status_code == status_code
    
    async def test_saved_password_is_hashed(self,
                                            app:FastAPI,
                                            client:AsyncClient,
                                            db:Database)->None:
        
        user_repository = UsersRepository(db)
        new_user = {"username":"Beyonce","email":"beyonce@gmail.com","password":"Password@123"}

        res = await client.post(app.url_path_for("users:register-new-user"),json={"new_user":new_user})

        assert res.status_code == HTTP_201_CREATED

        user_in_db = await user_repository.get_user_by_email(email=new_user["email"])
        assert user_in_db is not None
        assert user_in_db.username == new_user["username"]
        assert user_in_db.password!=new_user["password"]
        assert auth_service.verify_password(
            password=new_user["password"],
            hashed_pw=user_in_db.password,
        )
