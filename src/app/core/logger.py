import sys
from loguru import logger

def setup_logging():
    logger.remove() # Remove o log padrão
    
    # Log no console com cor para desenvolvimento
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )
    
    # Log em arquivo JSON para produção (Datadog/ElasticSearch leriam isso)
    logger.add("logs/app.json", serialize=True, rotation="10 MB")

setup_logging()