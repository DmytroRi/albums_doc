from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.links import AlbumGenreLink, TrackGenreLink
from app.models.tracks import Track

if TYPE_CHECKING:
    from app.models.albums import Album


class GenreBase(SQLModel):
    """Shared fields for genre classes."""

    name: str = Field(index=True, unique=True)


class Genre(GenreBase, table=True):
    """The db table 'genre'."""

    __tablename__ = "genres"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Relationships
    albums: list["Album"] = Relationship(
        back_populates="genres",
        link_model=AlbumGenreLink,
    )

    tracks: list["Track"] = Relationship(
        back_populates="vibes",
        link_model=TrackGenreLink,
    )


class GenreCreate(GenreBase):
    """Payload for POST /genres."""

    pass


class GenreUpdate(SQLModel):
    """Payload for PATCH /genres/{id}."""

    name: Optional[str] = Field(default=None, index=True, unique=True)


class GenreRead(GenreBase):
    """Response model for GET /genres."""

    id: int
