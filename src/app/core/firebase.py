import firebase_admin
from firebase_admin import credentials, firestore, storage
from pydantic_settings import BaseSettings
import os

# Config variaveis de ambiente
class Settings(BaseSettings):
    # Buscando chaves do .env com pydantic
    firebase_bucket_name: str = "curriculo-italodev.firebasestorage.app"

    class Config:
        env_file = ".env"
        extra = 'ignore'
        
settings = Settings()

def initialize_firebase():
    """
    Inicializa o SDK do Firebase
    Add serviceAccountKey.json na raiz
    """
    
    # Verifica se ja foi inicializado para evitar erros em hot-reload
    if not firebase_admin._apps:
        cred_path = os.path.join(os.getcwd(), "serviceAccountKey.json")
        
        if not os.path.exists(cred_path):
            raise FileNotFoundError(
                f"Arquivo de credenciais nao encontrado em: {cred_path}."
                "Baixe-o no console do Firebase > Configuraçoes do projeto > Contas e serviços"
            )
            
        cred = credentials.Certificate(cert=cred_path)
        firebase_admin.initialize_app(cred, {
            'storageBucket': settings.firebase_bucket_name
        })
        print('Firebase inicializado com sucesso.')
        
def get_db():
    return firestore.client()

def get_bucket():
    return storage.bucket()