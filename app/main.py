from fastapi import FastAPI, Depends
from app.database import init_db
from app.clients import router as clients_router
from app.wishlist import router as wishlist_router
from app.middleware import setup_logging
from app.auth import verify_token
from prometheus_fastapi_instrumentator import Instrumentator
from contextlib import asynccontextmanager
from fastapi import Depends
from app.token import router as token_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title="Magalu Wishlist API",
    debug=True,
    lifespan=lifespan,
    openapi_tags=[
        {"name": "auth", "description": "Operações de autenticação"},
        {"name": "clients", "description": "Gestão de clientes"},
        {"name": "wishlist", "description": "Gestão de listas de desejos"}
    ]
)
setup_logging(app)
Instrumentator().instrument(app).expose(app)

app.include_router(token_router, prefix="/auth", tags=["auth"])
app.include_router(clients_router, prefix="/clients", tags=["clients"], dependencies=[Depends(verify_token)])
app.include_router(wishlist_router, prefix="/wishlist", tags=["wishlist"], dependencies=[Depends(verify_token)])

