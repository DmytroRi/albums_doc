from datetime import date
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.links import AlbumArtistLink, AlbumGenreLink, AlbumVibeLink

if TYPE_CHECKING:
    from app.models.artists import Artist
    from app.models.genres import Genre
    from app.models.tracks import Track
    from app.models.vibes import Vibe


class AlbumBase(SQLModel):
    """Shared fields for album classes."""

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
    """Response model for GET /albums."""

    id: int
