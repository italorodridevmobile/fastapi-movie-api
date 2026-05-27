import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.core.logger import logger
from app.core.firebase import initialize_firebase
from app.api.routes.router import api_router

# Inicializa o Firebase
try:
    initialize_firebase()
except Exception as e:
    print(f'Aviso: Erro ao inicializar Firebase: {e}')
    
# Instância principal do FastAPI
app = FastAPI(
    title="BackEnd Python Italo Dev.",
    description="BackEnd com FastAPI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/reduc"
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Dominio do site em prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Inclusão das Rotas
app.include_router(api_router, prefix="/api/v1")

# Rota de Healthcheck
@app.get("/", tags=["health"])
async def root():
    return {
        "status": "Online",
        "message": "API operando com sucesso",
        "version": "1.0.0"
    }
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{0:.2f}".format(process_time)
    
    logger.info(
        f"Method: {request.method} | Path: {request.url.path} | "
        f"Status: {response.status_code} | Time: {formatted_process_time}ms"
    )
    
    return response