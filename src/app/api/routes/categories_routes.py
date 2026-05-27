from typing import List
from app.api.auth.auth import get_current_user
from app.api.schemas.categories_schemas import CategoryCreate, CategoryResponse
from app.application.categories.categories_service import CategoriesService
from app.infrastructure.categories_firestore_repo import FirestoreCategoriesRepository
from fastapi import APIRouter, Depends


router = APIRouter(prefix="/categories", tags=["Categories"])

def get_category_service():
    repo = FirestoreCategoriesRepository()
    return CategoriesService(repo)

# (POST) cadastrar categoria
@router.post('/register', response_model=CategoryResponse)
async def create_category(
    category_data: CategoryCreate,
    service: CategoriesService = Depends(get_category_service),
    #current_user: dict = Depends(get_current_user)
):
    return await service.create_category(category_data)

# (GET) Listar categorias
@router.get('/list', response_model=List[CategoryResponse])
async def list_categories(
    service: CategoriesService = Depends(get_category_service),
    #current_user: dict = Depends(get_current_user)
):
    return await service.get_categories()