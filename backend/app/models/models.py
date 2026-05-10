from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class AlbumArtistLink(SQLModel, table=True):
    album_id: Optional[int] = Field(default=None, foreign_key="album.id", primary_key=True)
    artist_id: Optional[int] = Field(default=None, foreign_key="artist.id", primary_key=True)


class AlbumProducerLink(SQLModel, table=True):
    album_id: Optional[int] = Field(default=None, foreign_key="album.id", primary_key=True)
    producer_id: Optional[int] = Field(default=None, foreign_key="producer.id", primary_key=True)


class AlbumGenreLink(SQLModel, table=True):
    album_id: Optional[int] = Field(default=None, foreign_key="album.id", primary_key=True)
    genre_id: Optional[int] = Field(default=None, foreign_key="genre.id", primary_key=True)


class AlbumMoodLink(SQLModel, table=True):
    album_id: Optional[int] = Field(default=None, foreign_key="album.id", primary_key=True)
    mood_id: Optional[int] = Field(default=None, foreign_key="mood.id", primary_key=True)


class Artist(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    albums: list["Album"] = Relationship(back_populates="artists", link_model=AlbumArtistLink)


class Producer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    albums: list["Album"] = Relationship(back_populates="producers", link_model=AlbumProducerLink)


class Genre(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    albums: list["Album"] = Relationship(back_populates="genres", link_model=AlbumGenreLink)


class Mood(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    albums: list["Album"] = Relationship(back_populates="moods", link_model=AlbumMoodLink)


class Track(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    album_id: int = Field(foreign_key="album.id", index=True)
    title: str
    duration_seconds: int
    track_order: int
    album: "Album" = Relationship(back_populates="tracks")


class Album(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    release_year: int = Field(index=True)
    grade: float = Field(ge=0, le=10)

    tracks: list[Track] = Relationship(back_populates="album")
    artists: list[Artist] = Relationship(back_populates="albums", link_model=AlbumArtistLink)
    producers: list[Producer] = Relationship(back_populates="albums", link_model=AlbumProducerLink)
    genres: list[Genre] = Relationship(back_populates="albums", link_model=AlbumGenreLink)
    moods: list[Mood] = Relationship(back_populates="albums", link_model=AlbumMoodLink)
