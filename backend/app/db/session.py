import os

from sqlmodel import SQLModel, Session, create_engine

from app.models import models  # noqa: F401

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg://albums:albums@localhost:5432/albums"
)

engine = create_engine(DATABASE_URL, echo=False)


def get_session():
    with Session(engine) as session:
        yield session

def init_db() -> None:
    SQLModel.metadata.create_all(engine)