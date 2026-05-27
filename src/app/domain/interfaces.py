from abc import ABC, abstractmethod

class IMovieRepository(ABC):
    @abstractmethod
    async def save(self, movie_data: dict):
        pass

    @abstractmethod
    async def get_all(self, page: int = 1, limit: int = 5):
        pass
    
    @abstractmethod
    async def get_by_category(self, category_id: str, page: int = 1, limit: int = 5) -> list:
        """Busca filmes que contenham o ID da categoria no array"""
        pass
    
    @abstractmethod
    async def upload_image(self, file_bytes: bytes, filename: str, content_type: str):
        pass
    
    @abstractmethod
    async def search_by_title(self, query_text: str) -> list:
        """
        Buscar filmes no banco de dados com base no trecho do titulo
        """
        pass
    
class ICategoryRepository(ABC):
    @abstractmethod
    async def create(self, data: dict) -> dict:
        """Cria uma nova categoria re torna o dicionario com id gerado"""
        pass
    
    @abstractmethod
    async def get_all(self) -> list:
        """Retorna uma lista de dicionarios com todas as categorias"""
        pass
    
class IProfileRepository(ABC):
    
    @abstractmethod
    async def save_profile(self, account_id: str, profile_data: dict) -> dict:
        """
        Grava um perfil desacoplado na colecao raiz 'profiles' do firestore,
        vinculando ao ID da conta do titular (account_id)
        """
        pass
    
    @abstractmethod
    async def get_user_profiles(self, account_id: str) -> list:
        """
        Busca e rotorna todos os perfis ativos que pertencem
        a mesma conta titular (account_id)
        """
        pass