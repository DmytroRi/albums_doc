"""init schema

Revision ID: 0001_init_schema
Revises:
Create Date: 2026-05-10
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_init_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "album",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("release_date", sa.Date(), nullable=True),
        sa.Column("grade", sa.Float(), nullable=True),
    )

    for table in ["artist", "genre", "vibe"]:
        op.create_table(
            table,
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("name", sa.String(), nullable=False, unique=True),
        )
        op.create_index(f"ix_{table}_name", table, ["name"])

    op.create_table(
        "track",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("album_id", sa.Integer(), sa.ForeignKey("album.id", ondelete="CASCADE"), nullable=False),
        sa.Column("track_number", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("length_seconds", sa.Integer(), nullable=True),
    )

    op.create_table(
        "album_artist_link",
        sa.Column("album_id", sa.Integer(), sa.ForeignKey("album.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("artist_id", sa.Integer(), sa.ForeignKey("artist.id", ondelete="CASCADE"), primary_key=True),
    )
    op.create_table(
        "album_genre_link",
        sa.Column("album_id", sa.Integer(), sa.ForeignKey("album.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("genre_id", sa.Integer(), sa.ForeignKey("genre.id", ondelete="CASCADE"), primary_key=True),
    )
    op.create_table(
        "album_vibe_link",
        sa.Column("album_id", sa.Integer(), sa.ForeignKey("album.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("vibe_id", sa.Integer(), sa.ForeignKey("vibe.id", ondelete="CASCADE"), primary_key=True),
    )
    op.create_table(
        "track_vibe_link",
        sa.Column("track_id", sa.Integer(), sa.ForeignKey("track.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("vibe_id", sa.Integer(), sa.ForeignKey("vibe.id", ondelete="CASCADE"), primary_key=True),
    )


def downgrade() -> None:
    for table in [
        "track_vibe_link",
        "album_vibe_link",
        "album_genre_link",
        "album_artist_link",
        "track",
        "vibe",
        "genre",
        "artist",
        "album",
    ]:
        op.drop_table(table)