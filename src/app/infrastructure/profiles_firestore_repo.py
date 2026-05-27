import asyncio
from datetime import datetime, timezone
from app.core.firebase import get_db, get_bucket
from app.domain.interfaces import IProfileRepository

class FirestoreProfilesRepository(IProfileRepository):
    def __init__(self):
        self.db = get_db()
        self.bucket = get_bucket()
        self.collection = self.db.collection('profiles')

    async def save_profile(self, account_id: str, profile_data: dict) -> dict:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._save_profile_sync, account_id, profile_data)

    async def get_user_profiles(self, account_id: str) -> list:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._get_user_profiles_sync, account_id)

    def _save_profile_sync(self, account_id: str, profile_data: dict) -> dict:
        profile_ref = self.collection.document()
        
        profile_data['id'] = profile_ref.id
        profile_data['account_id'] = account_id
        
        profile_data['active_devices'] = [
            {
                "device_id": profile_data.pop("device_id"),
                "device_name": profile_data.pop("device_name"),
                "last_login": datetime.now(timezone.utc).isoformat()
            }
        ]
        
        profile_ref.set(profile_data)
        return profile_data
    
    def _get_user_profiles_sync(self, account_id: str) -> list:
        profile_docs = self.collection.where("account_id", "==", account_id).stream()
        return [{"id": doc.id, **doc.to_dict()} for doc in profile_docs]
    
    async def delete(self, profile_id: str):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._delete_sync, profile_id)
    
    def _delete_sync(self, profile_id: str):
        doc_ref = self.collection.document(profile_id)
        doc_ref.delete()
        return True