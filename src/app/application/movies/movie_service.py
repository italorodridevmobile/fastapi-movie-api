from typing import Optional
from app.api.schemas.movies_schemas import MovieCreate, MovieUpdate
from loguru import logger
from app.domain.interfaces import IMovieRepository

class MovieService:
    def __init__(self, repo: IMovieRepository):
        self.repo = repo
    
    async def create_new_movie(self, movie_data: MovieCreate, image_file: Optional[bytes], image_name: str, background_tasks):
        # CORREÇÃO: Removido o $ da string
        logger.info(f"Iniciando criacao do filme: {movie_data.title}")
        try:
            data_dict = movie_data.model_dump()

            if image_file:
                url = await self.repo.upload_image(image_file, image_name, "image/jpeg")
                data_dict['image_url'] = url

            movie = await self.repo.save(data_dict)
            
            # CORREÇÃO: Removido o $
            logger.info(f"{movie_data.title} Salvo com sucesso!")
            return movie
        except Exception as e:
            logger.error(f"Falha ao criar filme: {str(e)}")
            raise

    async def get_movies(self, page: int = 1, limit: int = 5):
        logger.info("Buscando lista completa de filmes no Firestore")
        return await self.repo.get_all(page=page, limit=limit)
    
    async def get_movies_by_category(self, category_id: str, page: int = 1, limit: int = 5):
        logger.info(f"Buscando filmes da categoria ID: {category_id} (Página: {page}, Limite: {limit})")
        try:
            movies = await self.repo.get_by_category(category_id, page=page, limit=limit)
            logger.success(f"Retornados {len(movies)} filmes para a categoria {category_id} (Lote: {page})")
            return movies
        except Exception as e:
            logger.error(f"Erro ao buscar filmes da categoria {category_id}: {str(e)}")
            raise
    
    # CORREÇÃO: image_name tipado como Optional[str]
    async def update_movie(self, movie_id: str, movie_data: MovieCreate, image_file: Optional[bytes], image_name: Optional[str] = None):
        logger.info(f"Atualizando filme ID:  {movie_id}")
        try:
            update_data = movie_data.model_dump()
            
            if image_file and image_name:
                url = await self.repo.upload_image(image_file, image_name, "image/jpeg")
                update_data['image_url'] = url
                
            update_movie = await self.repo.update(movie_id, update_data)
            logger.success(f"Filme {movie_id} atualizado com sucesso!")
            return update_movie
        except Exception as e:
            logger.error(f"Erro ao atualizar filme {movie_id}: {str(e)}")
            raise
    
    # CORREÇÃO: patch_data tipado como MovieUpdate e não MonkeyPatch
    async def patch_movie(self, movie_id: str, patch_data: MovieUpdate):
        data_to_update = patch_data.model_dump(exclude_unset=True)
        
        if not data_to_update:
            logger.warning(f"PATCH chamado sem dados para o filme {movie_id}")
            return {"message": "Nada para atualizar"}

        logger.info(f"Fazendo atualização parcial no filme {movie_id}: {list(data_to_update.keys())}")
        return await self.repo.update(movie_id, data_to_update)
    
    async def delete_movie(self, movie_id: str, image_name: Optional[str] = None):
        logger.info(f"Solicitação de exclusão para o filme ID: {movie_id}")
        try:
            await self.repo.delete(movie_id)
            
            if image_name:
                await self.repo.delete_image(image_name)
                
            logger.success(f"Filme {movie_id} removido com sucesso!")
            return {"message": "Filme deletado com sucesso", "id": movie_id}
        except Exception as e:
            logger.error(f"Erro ao deletar filme {movie_id}: {str(e)}")
            raise
    
    async def search_movies(self, query_text: str):
        logger.info(f"Iniciando pesquisa de filmes pelo termo: {query_text}")
        try:
            results = await self.repo.search_by_title(query_text)
            logger.success(f"Pesquisa concluida. Encontrados {len(results)} resultados para {query_text}")
            return results
        except Exception as e:
            logger.error(f"Erro ao pesquisar filmes com o termo {query_text}: {str(e)}")
            raise