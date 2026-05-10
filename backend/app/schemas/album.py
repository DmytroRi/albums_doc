from typing import Optional

from pydantic import BaseModel, Field


class TrackCreate(BaseModel):
    title: str
    duration_seconds: int = Field(gt=0)
    track_order: int = Field(gt=0)


class AlbumCreate(BaseModel):
    title: str
    release_year: int
    grade: float = Field(ge=0, le=10)
    artists: list[str]
    producers: list[str]
    genres: list[str]
    moods: list[str]
    tracks: list[TrackCreate]


class AlbumUpdate(BaseModel):
    title: Optional[str] = None
    release_year: Optional[int] = None
    grade: Optional[float] = Field(default=None, ge=0, le=10)
    artists: Optional[list[str]] = None
    producers: Optional[list[str]] = None
    genres: Optional[list[str]] = None
    moods: Optional[list[str]] = None
    tracks: Optional[list[TrackCreate]] = None


class TrackRead(BaseModel):
    id: int
    title: str
    duration_seconds: int
    track_order: int


class AlbumSummary(BaseModel):
    id: int
    title: str
    release_year: int
    grade: float
    artists: list[str]


class AlbumRead(AlbumSummary):
    producers: list[str]
    genres: list[str]
    moods: list[str]
    tracks: list[TrackRead]
