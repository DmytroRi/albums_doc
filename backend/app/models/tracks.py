from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.links import TrackGenreLink, TrackVibeLink

if TYPE_CHECKING:
    from app.models.albums import Album
    from app.models.genres import Genre
    from app.models.vibes import Vibe


class TrackBase(SQLModel):
    """Shared fields for track classes."""

    title: str
    length_seconds: Optional[int] = None
    track_order: int


class Track(TrackBase, table=True):
    """The db table 'tracks'."""

    __tablename__ = "tracks"

    id: Optional[int] = Field(default=None, primary_key=True)
    album_id: int = Field(foreign_key="albums.id")

    album: "Album" = Relationship(back_populates="tracks")
    vibes: list["Vibe"] = Relationship(
        back_populates="tracks",
        link_model=TrackVibeLink,
    )
    genres: list["Genre"] = Relationship(
        back_populates="tracks",
        link_model=TrackGenreLink,
    )


class TrackCreate(TrackBase):
    """Payload for POST /tracks."""

    pass


class TrackUpdate(SQLModel):
    """Payload for PATCH /tracks/{id}."""

    title: Optional[str] = None
    length_seconds: Optional[int] = None
    track_order: Optional[int] = None


class TrackRead(TrackBase):
    """Response model for GET /tracks."""

    id: int
