from datetime import date
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.tracks import Track


class AlbumBase(SQLModel):
    """Shared fields for /albums' classes."""

    title: str
    release_date: Optional[date] = None
    grade: Optional[float] = Field(default=None, ge=0.0, le=5.0)


class Album(AlbumBase, table=True):
    """The db table 'albums'."""

    __tablename__ = "albums"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Relationships
    artists: list["Artist"] = Relationship(
        back_populates="albums",
        link_model=AlbumArtistLink,
    )
    genres: list["Genre"] = Relationship(
        back_populates="albums",
        link_model=AlbumGenreLink,
    )
    vibes: list["Vibe"] = Relationship(
        back_populates="albums",
        link_model=AlbumVibeLink,
    )
    tracks: list["Track"] = Relationship(back_populates="album")


class AlbumCreate(AlbumBase):
    """Payload for POST /albums."""

    pass


class AlbumUpdate(SQLModel):
    """Payload for PATCH /albums/{id}."""

    title: str
    release_date: Optional[date] = None
    grade: Optional[float] = Field(default=None, ge=0.0, le=5.0)


class AlbumRead(AlbumBase):
    """Response model for GET /albums"""

    id: int
