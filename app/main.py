from fastapi import FastAPI
from app.database import init_db
from app.clients import router as clients_router
from app.wishlist import router as wishlist_router
from app.middleware import setup_logging
from prometheus_fastapi_instrumentator import Instrumentator
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title="Magalu Wishlist API",
    debug=True,
    lifespan=lifespan
)

setup_logging(app)
Instrumentator().instrument(app).expose(app)

app.include_router(clients_router, prefix="/clients", tags=["clients"])
app.include_router(wishlist_router, prefix="/wishlist", tags=["wishlist"])
