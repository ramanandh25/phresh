from backend.app.db.repositories.base import BaseRepository
from backend.app.models.cleanings import CleaningCreate, CleaningUpdate, CleaninginDb


CREATE_CLEANING_QUERY = """
INSERT INTO cleanings(name, description, price, cleaning_type)
VALUES (:name, :description, :price, :cleaning_type)
RETURNING "ID", name, description, price, cleaning_type
"""

class CleaningsRepository(BaseRepository):  
    
    async def create_cleaning(self, *, new_cleaning: CleaningCreate) -> CleaninginDb:
        query_values = new_cleaning.model_dump()
        cleaning = await self.db.fetch_one(query=CREATE_CLEANING_QUERY, values=query_values)
        return CleaninginDb(**cleaning)

