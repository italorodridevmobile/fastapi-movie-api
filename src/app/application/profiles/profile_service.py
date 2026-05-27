from app.domain.interfaces import IProfileRepository
from loguru import logger
from app.api.schemas.profiles_schemas import ProfileCreate

class ProfilesService:
    def __init__(self, repo: IProfileRepository):
        self.repo = repo
    
        
    async def create_profile(self, account_id: str, profile_data: ProfileCreate):
        logger.info(f"Criando o perfil independente {profile_data.name} para a conta: {account_id}")
        try:
            existing_profiles = await self.repo.get_user_profiles(account_id)
            if len(existing_profiles) >= 5:
                logger.warning(f"A conta {account_id} tentou ultrapassar o limite de 5 pessoas")
                raise ValueError("Esta conta ja atingiu o limite maximo de 5 perfis")
            
            data_dict = profile_data.model_dump()
            return await self.repo.save_profile(account_id, data_dict)
        except Exception as e:
            logger.error(f"Erro ao cadastrar perfil na conta {account_id}: {str(e)}")
            raise
        
    async def list_profiles(self, account_id: str):
        logger.info(f"Buscando todos os perfis vinculados a conta: {account_id}")
        return await self.repo.get_user_profiles(account_id)
    
    async def delete_movie(self, profile_id: str):
        logger.info(f"Solicitação de exclusão para perfil ID: {profile_id}")
        try:
            await self.repo.delete(profile_id)
            logger.success(f"Perfil {profile_id} removido com sucesso!")
            return {"message": "Perfil deletado com sucesso", "id": profile_id}
        except Exception as e:
            logger.error(f"Erro ao deletar perfil {profile_id}: {str(e)}")
            raise