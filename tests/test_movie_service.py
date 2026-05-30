import pytest
from unittest.mock import AsyncMock, MagicMock

from app.api.schemas.movies_schemas import MovieCreate, MovieUpdate
from app.application.movies.movie_service import MovieService


@pytest.fixture
def repository():
    return MagicMock()


@pytest.fixture
def service(repository):
    return MovieService(repository)


@pytest.mark.asyncio
async def test_create_movie(service, repository):
    repository.upload_image = AsyncMock(
        return_value="http://link.com/capa.jpg"
    )

    repository.save = AsyncMock(
        return_value={
            "id": "123",
            "title": "Batman Teste",
        }
    )

    movie = MovieCreate(
        title="Batman Teste",
        description="Filme do Batman",
        category_ids=["cat-1"],
        price=19.90,
        year="2024",
        duration="2h 10min",
        url_movie="https://youtube.com/watch?v=test",
    )

    result = await service.create_new_movie(
        movie,
        b"image-bytes",
        "capa.jpg",
        MagicMock(),
    )

    assert result["id"] == "123"
    repository.upload_image.assert_called_once()
    repository.save.assert_called_once()


@pytest.mark.asyncio
async def test_get_movies(service, repository):
    repository.get_all = AsyncMock(
        return_value=[
            {
                "id": "1",
                "title": "Filme 1",
            }
        ]
    )

    result = await service.get_movies()

    assert len(result) == 1
    assert result[0]["title"] == "Filme 1"


@pytest.mark.asyncio
async def test_update_movie(service, repository):
    repository.upload_image = AsyncMock(
        return_value="http://new.com/capa.jpg"
    )

    repository.update = AsyncMock(
        return_value={
            "id": "123",
            "title": "Novo Titulo",
        }
    )

    movie = MovieCreate(
        title="Novo Titulo",
        description="Nova descrição",
        category_ids=["cat-1"],
        price=29.90,
        year="2025",
        duration="1h 50min",
        url_movie="https://youtube.com/watch?v=novo",
    )

    result = await service.update_movie(
        "123",
        movie,
        b"image-bytes",
        "nova_capa.jpg",
    )

    assert result["title"] == "Novo Titulo"
    repository.upload_image.assert_called_once()
    repository.update.assert_called_once()


@pytest.mark.asyncio
async def test_patch_movie(service, repository):
    repository.update = AsyncMock(
        return_value={
            "id": "123",
            "title": "Batman",
            "price": 50.0,
        }
    )

    patch = MovieUpdate(price=50.0)

    result = await service.patch_movie("123", patch)

    assert result["price"] == 50.0

    args, _ = repository.update.call_args
    assert args[1] == {"price": 50.0}


@pytest.mark.asyncio
async def test_delete_movie(service, repository):
    repository.delete = AsyncMock()
    repository.delete_image = AsyncMock()

    result = await service.delete_movie(
        "123",
        image_name="capa.jpg",
    )

    assert result["message"] == "Filme deletado com sucesso"

    repository.delete.assert_called_once_with("123")
    repository.delete_image.assert_called_once_with("capa.jpg")