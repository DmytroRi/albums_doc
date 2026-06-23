from sqlmodel import Field, SQLModel


class AlbumArtistLink(SQLModel, table=True):
    __tablename__ = "album_artist_link"

    album_id: int | None = Field(
        default=None,
        foreign_key="albums.id",
        primary_key=True,
    )
    artist_id: int | None = Field(
        default=None, foreign_key="artists.id", primary_key=True
    )


class AlbumGenreLink(SQLModel, table=True):
    __tablename__ = "album_genre_link"

    album_id: int | None = Field(
        default=None,
        foreign_key="albums.id",
        primary_key=True,
    )
    genre_id: int | None = Field(
        default=None,
        foreign_key="genres.id",
        primary_key=True,
    )


class AlbumVibeLink(SQLModel, table=True):
    __tablename__ = "album_vibe_link"

    album_id: int | None = Field(
        default=None,
        foreign_key="albums.id",
        primary_key=True,
    )
    vibe_id: int | None = Field(
        default=None,
        foreign_key="vibes.id",
        primary_key=True,
    )


class TrackVibeLink(SQLModel, table=True):
    __tablename__ = "track_vibe_link"

    track_id: int | None = Field(
        default=None,
        foreign_key="tracks.id",
        primary_key=True,
    )
    vibe_id: int | None = Field(
        default=None,
        foreign_key="vibes.id",
        primary_key=True,
    )


class TrackGenreLink(SQLModel, table=True):
    __tablename__ = "track_genre_link"

    track_id: int | None = Field(
        default=None,
        foreign_key="tracks.id",
        primary_key=True,
    )
    genre_id: int | None = Field(
        default=None,
        foreign_key="genres.id",
        primary_key=True,
    )
