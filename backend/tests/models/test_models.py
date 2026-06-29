from datetime import date

import pytest
from pydantic import ValidationError
from sqlmodel import Session, select

from app.models.albums import Album, AlbumCreate, AlbumUpdate
from app.models.artists import Artist, ArtistCreate
from app.models.genres import Genre, GenreCreate
from app.models.links import (
    AlbumArtistLink,
    AlbumGenreLink,
    AlbumVibeLink,
    TrackGenreLink,
    TrackVibeLink,
)
from app.models.tracks import Track, TrackCreate
from app.models.vibes import Vibe, VibeCreate


def test_album_grade_validation_accepts_boundaries_and_rejects_out_of_range():
    assert AlbumCreate(title="Low", grade=0).grade == 0
    assert AlbumCreate(title="High", grade=5).grade == 5

    with pytest.raises(ValidationError):
        AlbumCreate(title="Too low", grade=-0.1)

    with pytest.raises(ValidationError):
        AlbumCreate(title="Too high", grade=5.1)


def test_album_update_allows_partial_payload_and_validates_grade():
    assert AlbumUpdate().model_dump(exclude_unset=True) == {}
    assert AlbumUpdate(grade=None).grade is None

    with pytest.raises(ValidationError):
        AlbumUpdate(grade=6)


def test_named_create_models_require_name():
    for model in (ArtistCreate, GenreCreate, VibeCreate):
        with pytest.raises(ValidationError):
            model.model_validate({})
        assert model(name="name").name == "name"


def test_track_create_requires_title_order_and_album_id():
    payload = TrackCreate(title="Intro", track_order=1, length_seconds=90)
    assert payload.title == "Intro"
    assert payload.track_order == 1
    assert payload.length_seconds == 90

    with pytest.raises(ValidationError):
        TrackCreate.model_validate({"title": "Missing order"})


def test_model_relationships_persist_through_sqlmodel(session: Session):
    artist = Artist(name="Björk")
    genre = Genre(name="Art Pop")
    vibe = Vibe(name="Ethereal")
    album = Album(title="Homogenic", release_date=date(1997, 9, 22), grade=5)
    track = Track(title="Jóga", track_order=1, length_seconds=301, album=album)

    album.artists.append(artist)
    album.genres.append(genre)
    album.vibes.append(vibe)
    track.genres.append(genre)
    track.vibes.append(vibe)

    session.add(album)
    session.add(track)
    session.commit()

    stored_album = session.exec(select(Album).where(Album.title == "Homogenic")).one()
    assert [artist.name for artist in stored_album.artists] == ["Björk"]
    assert [genre.name for genre in stored_album.genres] == ["Art Pop"]
    assert [vibe.name for vibe in stored_album.vibes] == ["Ethereal"]
    assert stored_album.tracks[0].title == "Jóga"
    assert stored_album.tracks[0].genres[0].name == "Art Pop"
    assert stored_album.tracks[0].vibes[0].name == "Ethereal"


def test_link_models_expose_expected_composite_keys():
    cases = (
        (AlbumArtistLink(album_id=1, artist_id=2), {"album_id": 1, "artist_id": 2}),
        (AlbumGenreLink(album_id=1, genre_id=3), {"album_id": 1, "genre_id": 3}),
        (AlbumVibeLink(album_id=1, vibe_id=4), {"album_id": 1, "vibe_id": 4}),
        (TrackGenreLink(track_id=5, genre_id=3), {"track_id": 5, "genre_id": 3}),
        (TrackVibeLink(track_id=5, vibe_id=4), {"track_id": 5, "vibe_id": 4}),
    )

    for instance, expected in cases:
        assert instance.model_dump() == expected
