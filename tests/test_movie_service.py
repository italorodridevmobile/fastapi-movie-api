import pytest
from unittest.mock import AsyncMock, MagicMock
from app.application.movies.movie_service import MovieService
from app.api.schemas.schemas import MovieCreate, MovieUpdate

@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def service(mock_repo):
    return MovieService(mock_repo)

@pytest.mark.asyncio
async def test_create_movie_successfully(service, mock_repo):
    # Arrange
    mock_repo.upload_image = AsyncMock(return_value="http://link.com/foto.jpg")
    mock_repo.save = AsyncMock(return_value={"id": "123", "title": "Batman"})
    movie_in = MovieCreate(title="Batman Teste", description="Descricao longa", genres=["Ação"], price=10.0)
    
    # Act
    result = await service.create_new_movie(movie_in, b"bytes", "foto.jpg", MagicMock())

    # Assert
    assert result["id"] == "123"
    mock_repo.upload_image.assert_called_once()
    mock_repo.save.assert_called_once()

@pytest.mark.asyncio
async def test_get_all_movies(service, mock_repo):
    # Arrange
    mock_repo.get_all = AsyncMock(return_value=[{"id": "1", "title": "Filme 1"}])

    # Act
    result = await service.get_movies()

    # Assert
    assert len(result) == 1
    assert result[0]["title"] == "Filme 1"
    mock_repo.get_all.assert_called_once()

@pytest.mark.asyncio
async def test_update_movie_full(service, mock_repo):
    # Arrange
    mock_repo.upload_image = AsyncMock(return_value="http://new.com/foto.jpg")
    mock_repo.update = AsyncMock(return_value={"id": "123", "title": "Novo Titulo"})
    movie_up = MovieCreate(title="Novo Titulo", description="Nova descricao longa", genres=["Drama"], price=20.0)

    # Act
    result = await service.update_movie("123", movie_up, b"bytes", "nova_foto.jpg")

    # Assert
    assert result["title"] == "Novo Titulo"
    mock_repo.upload_image.assert_called_once()
    mock_repo.update.assert_called_once()

@pytest.mark.asyncio
async def test_patch_movie_partial(service, mock_repo):
    # Arrange
    # Simulando o retorno completo do banco apos o patch
    mock_repo.update = AsyncMock(return_value={"id": "123", "title": "Batman", "price": 50.0})
    patch_data = MovieUpdate(price=50.0)

    # Act
    result = await service.patch_movie("123", patch_data)

    # Assert
    assert result["price"] == 50.0
    # Verifica se o service passou apenas o que foi enviado para o repo
    args, _ = mock_repo.update.call_args
    assert args[1] == {"price": 50.0} 

@pytest.mark.asyncio
async def test_delete_movie_with_cleanup(service, mock_repo):
    # Arrange
    mock_repo.delete = AsyncMock()
    mock_repo.delete_image = AsyncMock()

    # Act
    result = await service.delete_movie("123", image_name="capa.jpg")

    # Assert
    assert result["message"] == "Filme deletado com sucesso"
    mock_repo.delete.assert_called_once_with("123")
    mock_repo.delete_image.assert_called_once_with("capa.jpg")