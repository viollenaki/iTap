from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from app.routers.products import router as products_router
from app.routers.users import router as users_router
from app.configs.firebase import check_firebase_connection
from app.configs.supabase import check_supabase_connection


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

app.include_router(products_router)
app.include_router(users_router)

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to fast_api_initializer"}


@app.get("/health/firebase", tags=["health"])
async def firebase_health() -> dict:
    """Check Firebase connection status."""
    return check_firebase_connection()


@app.get("/health/supabase", tags=["health"])
async def supabase_health() -> dict:
    """Check Supabase connection status."""
    return check_supabase_connection()


