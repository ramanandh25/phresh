from backend.app.db.repositories.base import BaseRepository
from backend.app.models.cleanings import CleaningCreate, CleaningUpdate, CleaninginDb


CREATE_CLEANING_QUERY = """
INSERT INTO cleanings(name, description, price, cleaning_type)
VALUES (:name, :description, :price, :cleaning_type)
RETURNING "ID", name, description, price, cleaning_type
"""

GET_CLEANING_BY_ID_QUERY = """
SELECT "ID", name, description, price, cleaning_type
FROM cleanings
WHERE "ID" = :id
"""


class CleaningsRepository(BaseRepository):
    async def create_cleaning(self, *, new_cleaning: CleaningCreate) -> CleaninginDb:
        query_values = new_cleaning.model_dump()
        cleaning = await self.db.fetch_one(
            query=CREATE_CLEANING_QUERY, values=query_values
        )
        return CleaninginDb(**cleaning)

    async def get_cleaning_by_id(self, *, id: int) -> CleaninginDb | None:
        cleaning = await self.db.fetch_one(
            query=GET_CLEANING_BY_ID_QUERY, values={"id": id}
        )
        if not cleaning:
            print(f"For id {id} no cleaning found")
            return None
        return CleaninginDb(**cleaning)
