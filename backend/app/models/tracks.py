from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class TrackBase(SQLModel):
    """Shared fields for /tracks' classes."""

    title: str
    length_seconds: Optional[int] = None
    grade: Optional[float] = Field(default=None, ge=0.0, le=5.0)
    track_order: int


class Track(TrackBase, table=True):
    """The db table 'tracks'."""

    __tablename__ = "tracks"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Relationships
    album: Album = Relationship(back_populates="tracks")
    vibes: list[Vibe] = Relationship(
        back_populates="tracks",
        link_model=TrackVibeLink,
    )


class TrackCreate(TrackBase):
    """Payload for POST /tracks."""

    pass


class TrackUpdate(SQLModel):
    """Payload for PATCH /tracks/{id}."""

    title: Optional[str] = None
    length_seconds: Optional[int] = None
    grade: Optional[float] = Field(default=None, ge=0.0, le=5.0)
    track_order: Optional[int] = None


class TrackRead(TrackBase):
    """Response model for GET /tracks"""

    id: int
