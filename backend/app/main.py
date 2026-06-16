import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.session import init_db
from app.routes.albums import router as albums_router
from app.routes.utilities import router as dev_router
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(title="Albums API", version="1.0.0", lifespan=lifespan)
app.include_router(albums_router)
app.include_router(dev_router)

cors_origins = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}