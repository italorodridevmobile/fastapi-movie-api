from app.api.schemas.categories_schemas import CategoryCreate
from loguru import logger
from app.domain.interfaces import ICategoryRepository

class CategoriesService:
    def __init__(self, repo: ICategoryRepository):
        self.repo = repo
    
    async def create_category(self, category_data: CategoryCreate):
        logger.info(f"Iniciando criacao da categoria: {category_data.title}")
        try:
            data_dict = category_data.model_dump()
            
            category = await self.repo.create(data_dict)
            
            logger.success(f"Categoria: '{category_data.title}' salva com sucesso (ID: {category.get('id')}!)")
            return category
        except Exception as e:
            logger.error(f"Falha ao criar categoria {category_data.title}: {str(e)}")
            raise
        
    async def get_categories(self):
        logger.info("Buscando lista completa de categorias")
        try:
            categories = await self.repo.get_all()
            logger.success(f"Retornadas {len(categories)} categorias com sucesso.")
            return categories
        except Exception as e:
            logger.error(f"Erro ao buscar categories: {str(e)}")
            raise