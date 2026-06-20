from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.tracks import Track


class VibeBase(SQLModel):
    """Shared fields for /vibes' classes."""

    name: str = Field(index=True, unique=True)


class Vibe(VibeBase, table=True):
    """The db table 'vibes'."""

    __tablename__ = "vibes"

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


class VibeCreate(VibeBase):
    """Payload for POST /vibes."""

    pass


class VibeUpdate(SQLModel):
    """Payload for PATCH /vibes/{id}."""

    name: Optional[str] = Field(index=True, unique=True)


class VibeRead(VibeBase):
    """Response model for GET /vibes"""

    id: int
