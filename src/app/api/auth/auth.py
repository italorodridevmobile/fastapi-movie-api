from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import firebase_admin
from firebase_admin import auth
from app.core.logger import logger

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        # Validando integridade e expiracao do token
        decoded_token = auth.verify_id_token(token)
        return decoded_token # retorna uid
    except firebase_admin.auth.ExpiredIdTokenError:
        logger.warning("Tentativa de acesso com Token expirado.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticacao expirado",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except Exception as e:
        logger.error(f"Erro na validacao do token Firebase: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticacao invalido ou ausente",
            headers={"WWW-Authenticate": "Bearer"}
        )