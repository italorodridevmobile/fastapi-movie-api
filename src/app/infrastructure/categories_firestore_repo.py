import asyncio
from app.core.firebase import get_db
from app.domain.interfaces import ICategoryRepository

class FirestoreCategoriesRepository(ICategoryRepository):
    def __init__(self):
        self.db = get_db()
        self.collection = self.db.collection("categories")
        
    async def create(self, data: dict) -> dict:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._create_sync, data)

    def _create_sync(self, data: dict) -> dict:
        doc_ref = self.collection.document()
        
        data['id'] = doc_ref.id
        doc_ref.set(data)
        return data
    
    async def get_all(self) -> list:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._get_all_sync)

    def _get_all_sync(self) -> list:
        return [{"id": doc.id, **doc.to_dict()} for doc in self.collection.stream()]