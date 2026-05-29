from app.api.auth.auth import get_current_user
from app.api.schemas.profiles_schemas import ProfileCreate
from app.infrastructure.profiles_firestore_repo import FirestoreProfilesRepository
from fastapi import APIRouter, Depends, HTTPException, status
from app.application.profiles.profile_service import ProfilesService

router = APIRouter(prefix="/profiles", tags=["Profiles"])

def get_profile_service():
    repo = FirestoreProfilesRepository()
    return ProfilesService(repo)

@router.post("/create/{account_id}", status_code=status.HTTP_201_CREATED)
async def create_user_profile(
    account_id: str,
    profile_data: ProfileCreate,
    service: ProfilesService = Depends(get_profile_service),
    current_user: dict = Depends(get_current_user)
):
    try:
        return await service.create_profile(account_id=account_id, profile_data=profile_data)
    except ValueError as val_err:
        raise HTTPException(status_code=400, detail=str(val_err))
    except Exception:
        raise HTTPException(status_code=500, detail="Erro interno ao criar o perfil independente")
    
@router.get("/list/{account_id}")
async def list_user_profiles(
    account_id: str,
    service: ProfilesService = Depends(get_profile_service),
    current_user: dict = Depends(get_current_user)
):
    return await service.list_profiles(account_id=account_id)

# (DELETE) - deletar filme por id
@router.delete('/delete/{profile_id}', status_code=204)
async def delete_movie(
    profile_id: str,
    service: ProfilesService = Depends(get_profile_service),
    current_user: dict = Depends(get_current_user)
):
    await service.delete_movie(profile_id)
    return None
