from sqlmodel import Session, delete, select

from app.models import Album, Artist, Genre, Track, Vibe
from app.schemas.album import (
    AlbumCreate,
    AlbumRead,
    AlbumSummary,
    AlbumUpdate,
    TrackRead,
)


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
            release_date=album.release_date,
            grade=album.grade,
            artists=[a.name for a in album.artists],
            genres=[g.name for g in album.genres],
            vibes=[v.name for v in album.vibes],
            tracks=[
                TrackRead(
                    id=t.id,
                    track_order=t.track_order,
                    title=t.title,
                    length_seconds=t.length_seconds,
                    vibes=[v.name for v in t.vibes],
                )
                for t in sorted(album.tracks, key=lambda x: x.track_order)
            ],
        )

    def create_album(self, data: AlbumCreate) -> AlbumRead:
        album = Album(
            title=data.title, release_date=data.release_date, grade=data.grade
        )
        self.session.add(album)
        self.session.flush()

        album.artists = [
            self._get_or_create_named(Artist, name) for name in data.artists
        ]
        album.genres = [self._get_or_create_named(Genre, name) for name in data.genres]
        album.vibes = [self._get_or_create_named(Vibe, name) for name in data.vibes]

        for t in data.tracks:
            self.session.add(
                Track(
                    album_id=album.id,
                    title=t.title,
                    length_seconds=t.length_seconds,
                    track_order=t.track_order,
                    vibes=[self._get_or_create_named(Vibe, name) for name in t.vibes],
                )
            )

        self.session.commit()
        self.session.refresh(album)
        return self._to_read(album)

    def get_album(self, album_id: int):
        album = self.session.get(Album, album_id)
        return self._to_read(album) if album else None

    def list_albums(self):
        albums = self.session.exec(select(Album)).all()
        return [
            AlbumSummary(
                id=a.id,
                title=a.title,
                release_date=a.release_date,
                grade=a.grade,
                artists=[ar.name for ar in a.artists],
            )
            for a in albums
        ]

    def search_albums(self, query: str):
        q = f"%{query.lower()}%"
        statement = (
            select(Album)
            .distinct()
            .join(Album.artists, isouter=True)
            .where(Album.title.ilike(q) | Artist.name.ilike(q))
        )
        albums = self.session.exec(statement).all()
        return [
            AlbumSummary(
                id=a.id,
                title=a.title,
                release_date=a.release_date,
                grade=a.grade,
                artists=[ar.name for ar in a.artists],
            )
            for a in albums
        ]

    def update_album(self, album_id: int, data: AlbumUpdate):
        album = self.session.get(Album, album_id)
        if not album:
            return None

        updates = data.model_dump(exclude_unset=True)
        scalar_fields = ["title", "release_date", "grade"]
        for field in scalar_fields:
            if field in updates:
                setattr(album, field, updates[field])

        for rel, model in [("artists", Artist), ("genres", Genre), ("vibes", Vibe)]:
            if rel in updates:
                setattr(
                    album,
                    rel,
                    [self._get_or_create_named(model, name) for name in updates[rel]],
                )

        if "tracks" in updates:
            self.session.exec(delete(Track).where(Track.album_id == album.id))
            for t in updates["tracks"]:
                self.session.add(
                    Track(
                        album_id=album.id,
                        title=t["title"],
                        length_seconds=t.get("length_seconds"),
                        track_order=t["track_order"],
                        vibes=[
                            self._get_or_create_named(Vibe, name)
                            for name in t.get("vibes", [])
                        ],
                    )
                )

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
