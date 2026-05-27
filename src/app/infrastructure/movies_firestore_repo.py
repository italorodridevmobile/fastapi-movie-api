import asyncio
import datetime
from app.core.firebase import get_db, get_bucket
from app.domain.interfaces import IMovieRepository

class FirestoreMoviesRepository(IMovieRepository):
    def __init__(self):
        self.db = get_db()
        self.bucket = get_bucket()
        self.collection = self.db.collection('movies')

    async def save(self, movie_data: dict):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._save_sync, movie_data)

    def _save_sync(self, movie_data: dict):
        doc_ref = self.collection.document()
        movie_data['id'] = doc_ref.id
        doc_ref.set(movie_data)
        return movie_data

    async def upload_image(self, file_bytes: bytes, filename: str, content_type: str) -> str:
        loop = asyncio.get_event_loop()
        # Passamos o content_type para o método síncrono também
        return await loop.run_in_executor(None, self._upload_sync, file_bytes, filename, content_type)

    def _upload_sync(self, file_bytes: bytes, filename: str, content_type: str) -> str:
        blob = self.bucket.blob(f"movies/{filename}")
        # Usando o content_type aqui
        blob.upload_from_string(file_bytes, content_type=content_type)
        blob.make_public()
        return blob.public_url

    async def get_all(self, page: int = 1, limit: int = 5) -> list:
        loop = asyncio.get_event_loop()
        
        return await loop.run_in_executor(
            None, 
            self._get_all_sync, 
            page, 
            limit
        )

    def _get_all_sync(self, page: int, limit: int) -> list:
        skip = (page - 1) * limit
        
        all_movies = [{"id": doc.id, **doc.to_dict()} for doc in self.collection.stream()]
        
        return all_movies[skip : skip + limit]
    
    async def update(self, movie_id: str, data: dict):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._update_sync, movie_id, data)
    
    def _update_sync(self, movie_id: str, data: dict):
        doc_ref = self.collection.document(movie_id)
        doc_ref.update(data)
        updated_doc = doc_ref.get()
        if updated_doc.exists:
            return {**updated_doc.to_dict(), "id": movie_id}
        return None
    
    async def delete(self, movie_id: str):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._delete_sync, movie_id)
    
    def _delete_sync(self, movie_id: str):
        doc_ref = self.collection.document(movie_id)
        doc_ref.delete()
        return True
    
    async def delete_image(self, filename: str):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._delete_image_sync, filename)
        
    def _delete_image_sync(self, filename: str):
        blob = self.bucket.blob(f"movies/{filename}")
        if blob.exists():
            blob.delete()
    
    async def get_by_category(self, category_id: str, page: int = 1, limit: int = 5) -> list:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self._get_by_category_sync,
            category_id,
            page,
            limit
        )

    def _get_by_category_sync(self, category_id: str, page: int, limit: int) -> list:
        skip = (page - 1) * limit
        
        query = self.collection.where("category_ids", "array_contains", category_id)
        
        all_movies = [{"id": doc.id, **doc.to_dict()} for doc in query.stream()]

        return all_movies[skip : skip + limit]
    
    async def search_by_title(self, query_text: str) -> list:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._search_by_title_sync, query_text)

    def _search_by_title_sync(self, query_text: str) -> list:
        search_term = query_text.lower().strip()
        
        if not search_term:
            return []

        all_docs = self.collection.stream()
        results = []
        
        for doc in all_docs:
            movie_data = doc.to_dict()
            title = movie_data.get("title", "").lower()
            
            if search_term in title:
                movie_data["id"] = doc.id
                results.append(movie_data)
                
        return results
    
    
    
    
    