
from typing import List, Optional
from app.api.auth.auth import get_current_user
from app.api.schemas.movies_schemas import MovieCreate, MovieResponse, MovieUpdate
from app.application.movies.movie_service import MovieService
from app.infrastructure.movies_firestore_repo import FirestoreMoviesRepository
from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, UploadFile

router = APIRouter(prefix="/movies", tags=["Movies"])

def get_movie_service():
    repo = FirestoreMoviesRepository()
    return MovieService(repo)

# (POST) cadastrar filmes
@router.post('/register', response_model=MovieResponse)
async def add_movie(
    background_tasks: BackgroundTasks,
    title: str = Form(...),
    description: str = Form(...),
    category_ids: str = Form(..., description="IDs separados por virgula Ex: id_1, id_2"),
    price: float = Form(...),
    year: str = Form(...),
    duration: str =  Form(...),
    url_movie: str = Form(..., description="URL do trailer do filme"),
    file: UploadFile = File(...),
    service: MovieService = Depends(get_movie_service),
    #current_user: dict = Depends(get_current_user)
):
    movie_create = MovieCreate(
        title=title, 
        description=description, 
        category_ids=[c.strip() for c in category_ids.split(",") if c.strip()],
        price=price, 
        year=year,
        duration=duration,
        url_movie=url_movie
    )
    
    image_bytes = await file.read()
    
    return await service.create_new_movie(
        movie_data=movie_create, 
        image_file=image_bytes, 
        image_name=file.filename,
        background_tasks=background_tasks
    )
    
# (GET - listar filmes
@router.get('/list', response_model=List[MovieResponse])
async def list_movies(
    page: int = 1, 
    limit: int = 5,
    service: MovieService = Depends(get_movie_service),
    #current_user: dict = Depends(get_current_user)
):
    return await service.get_movies(page=page, limit=limit)

# (GET) listar filmes por categoria
@router.get("/list/{category_id}")
async def get_movies_by_category(
    category_id: str, 
    page: int = 1, 
    limit: int = 5, 
    service: MovieService = Depends(get_movie_service)
):
    return await service.get_movies_by_category(category_id=category_id, page=page, limit=limit)

# (PUT) listar filmes por id
@router.put('/update/{movie_id}', response_model=MovieResponse)
async def update_movie(
    movie_id: str,
    title: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    year: str = Form(...),
    duration: str = Form(...),
    category_ids: str = Form(..., description="IDs separados por virgula Ex: id_1, id_2"),
    file: Optional[UploadFile] = File(None),
    service: MovieService = Depends(get_movie_service),
    #current_user: dict = Depends(get_current_user)
):
    movie_create = MovieCreate(
        title=title,
        description=description,
        price=price,
        category_ids=[c.strip() for c in category_ids.split(",") if c.strip()],
        year=year,
        duration=duration
    )
    
    image_bytes = await file.read() if file else None
    image_name = file.filename if file else ""

    return await service.update_movie(movie_id, movie_create, image_bytes, image_name)

# (DELETE) - deletar filme por id
@router.delete('/delete/{movie_id}', status_code=204)
async def delete_movie(
    movie_id: str,
    service: MovieService = Depends(get_movie_service),
    #current_user: dict = Depends(get_current_user)
):
    await service.delete_movie(movie_id) # Vírgula removida
    return None

# (PATCH) atualizar filme por id
@router.patch('/update-item/{movie_id}', response_model=MovieResponse)
async def patch_movie(
    movie_id: str,
    update_data: MovieUpdate,
    service: MovieService = Depends(get_movie_service),
    #current_user: dict = Depends(get_current_user)
):
    return await service.patch_movie(movie_id, update_data)

# (GET) Pesquisa por nome do filme
@router.get('/search')
async def search_movies_by_title(
    query: str,
    service: MovieService = Depends(get_movie_service),
    #current_user: dict = Depends(get_current_user)
):
    """
    Pesquisa filme pelo titulo
    Ex: /search?query=Italo
    """
    if not query.strip():
        raise HTTPException(status_code=400, detail="Valor vazio, digite algo")
    return await service.search_movies(query_text=query)