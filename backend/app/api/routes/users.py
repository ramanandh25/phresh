from fastapi import Depends, APIRouter, HTTPException, Path, Body
from backend.app.models.users import UserCreate, UserInDB, UserPublic
from backend.app.db.repositories.users import UsersRepository
from backend.app.api.dependencies.database import get_repository
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND


router = APIRouter()


@router.post(
    "/",
    response_model=UserPublic,
    name="users:register-new-user",
    status_code=HTTP_201_CREATED,
)
async def register_new_user(
    new_user: UserCreate = Body(..., embed=True),
    user_repo: UsersRepository = Depends(get_repository(UsersRepository)),
):
    created_user = await user_repo.register_new_user(new_user=new_user)
    created_user = created_user.model_dump(exclude={"password","salt"})
    return UserPublic(**created_user)
