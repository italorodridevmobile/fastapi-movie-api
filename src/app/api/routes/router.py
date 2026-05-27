from fastapi import APIRouter
from app.api.routes.movies_routes import router as movies_router
from app.api.routes.categories_routes import router as categories_router
from app.api.routes.profiles_routes import router as profiles_router

api_router = APIRouter()

api_router.include_router(movies_router)
api_router.include_router(categories_router)
api_router.include_router(profiles_router)