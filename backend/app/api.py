from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from app.routers.products import router as products_router

app = FastAPI()
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


