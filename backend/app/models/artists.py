from typing import TYPE_CHECKING, Optional

from app.models.links import AlbumArtistLink
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.albums import Album


class ArtistBase(SQLModel):
    """Shared fields for artist classes."""

    name: str = Field(index=True, unique=True)


class Artist(ArtistBase, table=True):
    """The db table 'artists'."""

    __tablename__ = "artists"

    id: Optional[int] = Field(default=None, primary_key=True)

    albums: list["Album"] = Relationship(
        back_populates="artists",
        link_model=AlbumArtistLink,
    )


class ArtistCreate(ArtistBase):
    """Payload for POST /artists."""

    pass


class ArtistUpdate(SQLModel):
    """Payload for PATCH /artists/{id}."""

    name: Optional[str] = Field(default=None, index=True, unique=True)


class ArtistRead(ArtistBase):
    """Response model for GET /artists."""

    id: int
