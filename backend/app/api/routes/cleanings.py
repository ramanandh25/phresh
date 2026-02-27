from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from backend.app.models.cleanings import CleaningCreate, CleaningPublic
from backend.app.api.dependencies.database import get_repository
from backend.app.db.repositories.cleanings import CleaningsRepository


router = APIRouter()


@router.get("/")
async def get_all_cleanings() -> List[dict]:
    cleanings = [
        {
            "id": 1,
            "name": "Cleaning 1",
            "description": "First cleaning",
            "type": "Full cleaning",
            "price_per_hour": 29.99,
        },
        {
            "id": 2,
            "name": "Cleaning 2",
            "description": "Second cleaning",
            "type": "Regular cleaning",
            "price_per_hour": 19.99,
        },
        {
            "id": 3,
            "name": "Cleaning 3",
            "description": "Third cleaning",
            "type": "Deep cleaning",
            "price_per_hour": 39.99,
        },
    ]
    return cleanings


@router.post(
    "/",
    response_model=CleaningPublic,
    name="cleanings:create_cleaning",
    status_code=HTTP_201_CREATED,
)
async def create_cleaning(
    new_cleaning: CleaningCreate = Body(..., embed=True),
    cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository)),
) -> CleaningPublic:
    created_cleaning = await cleanings_repo.create_cleaning(new_cleaning=new_cleaning)
    return created_cleaning


@router.get("/{id}", name="cleanings:get_cleaning_by_id")
async def get_cleaning_by_id(
    id: int,
    cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository)),
):
    cleaning = await cleanings_repo.get_cleaning_by_id(id=id)
    print(f"Cleaning retrieved: {cleaning} for id {id}")  # Debugging statement
    if not cleaning:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Cleaning not found")
    return cleaning
