from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routers.products import router as products_router
from app.configs.db import engine
from app.configs.tables import Base
from app.configs.firebase import check_firebase_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

app.include_router(products_router)

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to fast_api_initializer"}


@app.get("/health/firebase", tags=["health"])
async def firebase_health() -> dict:
    """Check Firebase connection status."""
    return check_firebase_connection()


