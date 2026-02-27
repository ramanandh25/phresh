from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, Path
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_200_OK

from backend.app.models.cleanings import CleaningCreate, CleaningPublic, CleaningUpdate
from backend.app.api.dependencies.database import get_repository
from backend.app.db.repositories.cleanings import CleaningsRepository


router = APIRouter()


@router.get(
    "/", response_model=List[CleaningPublic], name="cleanings:get-all-cleanings"
)
async def get_all_cleanings(
    cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository)),
) -> List[CleaningPublic]:
    return await cleanings_repo.get_all_cleanings()


@router.post(
    "/",
    response_model=CleaningPublic,
    name="cleanings:create-cleaning",
    status_code=HTTP_201_CREATED,
)
async def create_cleaning(
    new_cleaning: CleaningCreate = Body(..., embed=True),
    cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository)),
) -> CleaningPublic:
    created_cleaning = await cleanings_repo.create_cleaning(new_cleaning=new_cleaning)
    return created_cleaning


@router.get("/{id}", name="cleanings:get-cleaning-by-id")
async def get_cleaning_by_id(
    id: int = Path(..., title="The ID of the cleaning to retrieve"),
    cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository)),
):
    cleaning = await cleanings_repo.get_cleaning_by_id(id=id)
    print(f"Cleaning retrieved: {cleaning} for id {id}")  # Debugging statement
    if not cleaning:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Cleaning not found")
    return cleaning


@router.put("/{id}", name="cleanings:update-cleaning")
async def update_cleaning(
    id: int = Path(..., ge=1, title="The ID of the cleaning to update"),
    cleaning_update: CleaningUpdate = Body(..., embed=True),
    cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository)),
) -> CleaningPublic:
    updated_cleaning = await cleanings_repo.update_cleaning(
        id=id, cleaning_update=cleaning_update
    )
    if not updated_cleaning:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Cleaning not found")

    return updated_cleaning


@router.delete(
    "/{id}",
    name="cleanings:delete-cleaning-by-id",
    status_code=HTTP_200_OK,
)
async def delete_cleaning_by_id(
    id: int = Path(..., ge=1, title="The id of the cleaning to be deleted"),
    cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository)),
) -> int:

    deleted_id = await cleanings_repo.delete_cleaning_by_id(id=id)

    if not deleted_id:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"No cleaning with the id {id} is found for deleting",
        )
    return deleted_id
