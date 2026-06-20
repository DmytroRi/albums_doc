from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.tracks import Track


class GenreBase(SQLModel):
    """Shared fields for /genre' classes."""

    name: str = Field(index=True, unique=True)


class Genre(GenreBase, table=True):
    """The db table 'genre'."""

    __tablename__ = "genre"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Relationships
    albums: list[Album] = Relationship(
        back_populates="vibes",
        link_model=AlbumVibeLink,
    )

    tracks: list["Track"] = Relationship(
        back_populates="vibes",
        link_model=TrackVibeLink,
    )


class GenreCreate(GenreBase):
    """Payload for POST /genre."""

    pass


class GenreUpdate(SQLModel):
    """Payload for PATCH /genre/{id}."""

    name: Optional[str] = Field(index=True, unique=True)


class GenreRead(GenreBase):
    """Response model for GET /genre"""

    id: int
