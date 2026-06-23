import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.session import init_db
from app.routes.routes_album_artist_links import router as album_artist_links_router
from app.routes.routes_album_genre_links import router as album_genre_links_router
from app.routes.routes_album_vibe_links import router as album_vibe_links_router
from app.routes.routes_albums import router as albums_router
from app.routes.routes_artists import router as artists_router
from app.routes.routes_genres import router as genres_router
from app.routes.routes_track_genre_links import router as track_genre_links_router
from app.routes.routes_track_vibe_links import router as track_vibe_links_router
from app.routes.routes_tracks import router as tracks_router
from app.routes.routes_vibes import router as vibes_router
from app.routes.utilities import router as dev_router
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(title="Albums API", version="1.0.0", lifespan=lifespan)
app.include_router(albums_router)
app.include_router(artists_router)
app.include_router(genres_router)
app.include_router(vibes_router)
app.include_router(tracks_router)
app.include_router(album_artist_links_router)
app.include_router(album_genre_links_router)
app.include_router(album_vibe_links_router)
app.include_router(track_genre_links_router)
app.include_router(track_vibe_links_router)
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