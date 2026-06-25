from collections.abc import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from app.db.session import get_session
import app.models  # noqa: F401 - register SQLModel tables
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


@pytest.fixture(name="session")
def session_fixture() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="test_app")
def test_app_fixture(session: Session) -> FastAPI:
    app = FastAPI(title="Albums API Test App")
    for router in (
        albums_router,
        artists_router,
        genres_router,
        vibes_router,
        tracks_router,
        album_artist_links_router,
        album_genre_links_router,
        album_vibe_links_router,
        track_genre_links_router,
        track_vibe_links_router,
        dev_router,
    ):
        app.include_router(router)

    def get_test_session() -> Generator[Session, None, None]:
        yield session

    app.dependency_overrides[get_session] = get_test_session
    return app


@pytest.fixture(name="client")
def client_fixture(test_app: FastAPI) -> Generator[TestClient, None, None]:
    with TestClient(test_app) as client:
        yield client
