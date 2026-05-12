from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class TrackCreate(BaseModel):
    track_number: int = Field(gt=0)
    title: str
    length_seconds: Optional[int] = Field(default=None, gt=0)
    vibes: list[str] = []


class AlbumCreate(BaseModel):
    title: str
    release_date: Optional[date] = None
    grade: Optional[float] = Field(default=None, ge=0, le=5)
    artists: list[str]
    genres: list[str]
    vibes: list[str] = []
    tracks: list[TrackCreate] = []


class AlbumUpdate(BaseModel):
    title: Optional[str] = None
    release_date: Optional[date] = None
    grade: Optional[float] = Field(default=None, ge=0, le=5)
    artists: Optional[list[str]] = None
    genres: Optional[list[str]] = None
    vibes: Optional[list[str]] = None
    tracks: Optional[list[TrackCreate]] = None


class TrackRead(BaseModel):
    id: int
    track_number: int
    title: str
    length_seconds: Optional[int] = None
    vibes: list[str]


class AlbumSummary(BaseModel):
    id: int
    title: str
    release_date: Optional[date] = None
    grade: Optional[float] = None
    artists: list[str]


class AlbumRead(AlbumSummary):
    genres: list[str]
    vibes: list[str]
    tracks: list[TrackRead]