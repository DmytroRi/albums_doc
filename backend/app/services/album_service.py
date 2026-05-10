from sqlmodel import Session, delete, select

from app.models.models import Album, Artist, Genre, Mood, Producer, Track
from app.schemas.album import AlbumCreate, AlbumRead, AlbumSummary, AlbumUpdate, TrackRead


class AlbumService:
    def __init__(self, session: Session):
        self.session = session

    def _get_or_create_named(self, model, name: str):
        entity = self.session.exec(select(model).where(model.name == name)).first()
        if entity:
            return entity
        entity = model(name=name)
        self.session.add(entity)
        self.session.flush()
        return entity

    def _to_read(self, album: Album) -> AlbumRead:
        return AlbumRead(
            id=album.id,
            title=album.title,
            release_year=album.release_year,
            grade=album.grade,
            artists=[a.name for a in album.artists],
            producers=[p.name for p in album.producers],
            genres=[g.name for g in album.genres],
            moods=[m.name for m in album.moods],
            tracks=[
                TrackRead(id=t.id, title=t.title, duration_seconds=t.duration_seconds, track_order=t.track_order)
                for t in sorted(album.tracks, key=lambda x: x.track_order)
            ],
        )

    def create_album(self, data: AlbumCreate) -> AlbumRead:
        album = Album(title=data.title, release_year=data.release_year, grade=data.grade)
        self.session.add(album)
        self.session.flush()

        album.artists = [self._get_or_create_named(Artist, name) for name in data.artists]
        album.producers = [self._get_or_create_named(Producer, name) for name in data.producers]
        album.genres = [self._get_or_create_named(Genre, name) for name in data.genres]
        album.moods = [self._get_or_create_named(Mood, name) for name in data.moods]

        for t in data.tracks:
            self.session.add(
                Track(album_id=album.id, title=t.title, duration_seconds=t.duration_seconds, track_order=t.track_order)
            )

        self.session.commit()
        self.session.refresh(album)
        return self._to_read(album)

    def get_album(self, album_id: int):
        album = self.session.get(Album, album_id)
        return self._to_read(album) if album else None

    def list_albums(self):
        albums = self.session.exec(select(Album)).all()
        return [AlbumSummary(id=a.id, title=a.title, release_year=a.release_year, grade=a.grade, artists=[ar.name for ar in a.artists]) for a in albums]

    def search_albums(self, query: str):
        q = f"%{query.lower()}%"
        statement = (
            select(Album)
            .distinct()
            .join(Album.artists, isouter=True)
            .join(Album.producers, isouter=True)
            .where(
                Album.title.ilike(q) | Artist.name.ilike(q) | Producer.name.ilike(q)
            )
        )
        albums = self.session.exec(statement).all()
        return [AlbumSummary(id=a.id, title=a.title, release_year=a.release_year, grade=a.grade, artists=[ar.name for ar in a.artists]) for a in albums]

    def update_album(self, album_id: int, data: AlbumUpdate):
        album = self.session.get(Album, album_id)
        if not album:
            return None

        updates = data.model_dump(exclude_unset=True)
        scalar_fields = ["title", "release_year", "grade"]
        for field in scalar_fields:
            if field in updates:
                setattr(album, field, updates[field])

        for rel, model in [("artists", Artist), ("producers", Producer), ("genres", Genre), ("moods", Mood)]:
            if rel in updates:
                setattr(album, rel, [self._get_or_create_named(model, name) for name in updates[rel]])

        if "tracks" in updates:
            self.session.exec(delete(Track).where(Track.album_id == album.id))
            for t in updates["tracks"]:
                self.session.add(Track(album_id=album.id, title=t["title"], duration_seconds=t["duration_seconds"], track_order=t["track_order"]))

        self.session.add(album)
        self.session.commit()
        self.session.refresh(album)
        return self._to_read(album)

    def delete_album(self, album_id: int) -> bool:
        album = self.session.get(Album, album_id)
        if not album:
            return False
        self.session.delete(album)
        self.session.commit()
        return True
