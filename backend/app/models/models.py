from datetime import date
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class AlbumArtistLink(SQLModel, table=True):
    __tablename__ = "album_artist_link"

    album_id: Optional[int] = Field(
        default=None, foreign_key="album.id", primary_key=True
    )
    artist_id: Optional[int] = Field(
        default=None, foreign_key="artist.id", primary_key=True
    )


class AlbumGenreLink(SQLModel, table=True):
    __tablename__ = "album_genre_link"
    
    album_id: Optional[int] = Field(
        default=None, foreign_key="album.id", primary_key=True
    )
    genre_id: Optional[int] = Field(
        default=None, foreign_key="genre.id", primary_key=True
    )


class AlbumVibeLink(SQLModel, table=True):
    __tablename__ = "album_vibe_link"

    album_id: Optional[int] = Field(
        default=None, foreign_key="album.id", primary_key=True
    )
    vibe_id: Optional[int] = Field(
        default=None, foreign_key="vibe.id", primary_key=True
    )


class TrackVibeLink(SQLModel, table=True):
    __tablename__ = "track_vibe_link"

    track_id: Optional[int] = Field(
        default=None, foreign_key="track.id", primary_key=True
    )
    vibe_id: Optional[int] = Field(
        default=None, foreign_key="vibe.id", primary_key=True
    )


class Album(SQLModel, table=True):
    __tablename__ = "album"

    id: Optional[int] = Field(default=None, primary_key=True)

    title: str
    release_date: Optional[date] = None
    grade: Optional[float] = Field(default=None, ge=0.0, le=5.0)

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


class Artist(SQLModel, table=True):
    __tablename__ = "artist"

    id: Optional[int] = Field(default=None, primary_key=True)

    name: str = Field(index=True, unique=True)

    albums: list[Album] = Relationship(
        back_populates="artists",
        link_model=AlbumArtistLink,
    )


class Genre(SQLModel, table=True):
    __tablename__ = "genre"

    id: Optional[int] = Field(default=None, primary_key=True)

    name: str = Field(index=True, unique=True)

    albums: list[Album] = Relationship(
        back_populates="genres",
        link_model=AlbumGenreLink,
    )


class Vibe(SQLModel, table=True):
    __tablename__ = "vibe"

    id: Optional[int] = Field(default=None, primary_key=True)

    name: str = Field(index=True, unique=True)

    albums: list[Album] = Relationship(
        back_populates="vibes",
        link_model=AlbumVibeLink,
    )

    tracks: list["Track"] = Relationship(
        back_populates="vibes",
        link_model=TrackVibeLink,
    )


class Track(SQLModel, table=True):
    __tablename__ = "track"

    id: Optional[int] = Field(default=None, primary_key=True)

    album_id: int = Field(foreign_key="album.id")

    track_number: int
    title: str
    length_seconds: Optional[int] = None
    grade: Optional[float] = Field(default=None, ge=0.0, le=5.0)

    album: Album = Relationship(back_populates="tracks")

    vibes: list[Vibe] = Relationship(
        back_populates="tracks",
        link_model=TrackVibeLink,
    )