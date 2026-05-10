"""init schema

Revision ID: 0001_init_schema
Revises: 
Create Date: 2026-05-10
"""
from alembic import op
import sqlalchemy as sa

revision = '0001_init_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('album', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('title', sa.String(), nullable=False), sa.Column('release_year', sa.Integer(), nullable=False), sa.Column('grade', sa.Float(), nullable=False))
    op.create_index('ix_album_title', 'album', ['title'])
    op.create_index('ix_album_release_year', 'album', ['release_year'])

    for table in ['artist', 'producer', 'genre', 'mood']:
        op.create_table(table, sa.Column('id', sa.Integer(), primary_key=True), sa.Column('name', sa.String(), nullable=False, unique=True))
        op.create_index(f'ix_{table}_name', table, ['name'])

    op.create_table('track', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('album_id', sa.Integer(), sa.ForeignKey('album.id', ondelete='CASCADE')), sa.Column('title', sa.String(), nullable=False), sa.Column('duration_seconds', sa.Integer(), nullable=False), sa.Column('track_order', sa.Integer(), nullable=False))
    op.create_index('ix_track_album_id', 'track', ['album_id'])

    op.create_table('albumartistlink', sa.Column('album_id', sa.Integer(), sa.ForeignKey('album.id', ondelete='CASCADE'), primary_key=True), sa.Column('artist_id', sa.Integer(), sa.ForeignKey('artist.id', ondelete='CASCADE'), primary_key=True))
    op.create_table('albumproducerlink', sa.Column('album_id', sa.Integer(), sa.ForeignKey('album.id', ondelete='CASCADE'), primary_key=True), sa.Column('producer_id', sa.Integer(), sa.ForeignKey('producer.id', ondelete='CASCADE'), primary_key=True))
    op.create_table('albumgenrelink', sa.Column('album_id', sa.Integer(), sa.ForeignKey('album.id', ondelete='CASCADE'), primary_key=True), sa.Column('genre_id', sa.Integer(), sa.ForeignKey('genre.id', ondelete='CASCADE'), primary_key=True))
    op.create_table('albummoodlink', sa.Column('album_id', sa.Integer(), sa.ForeignKey('album.id', ondelete='CASCADE'), primary_key=True), sa.Column('mood_id', sa.Integer(), sa.ForeignKey('mood.id', ondelete='CASCADE'), primary_key=True))


def downgrade() -> None:
    for table in ['albummoodlink', 'albumgenrelink', 'albumproducerlink', 'albumartistlink', 'track', 'mood', 'genre', 'producer', 'artist', 'album']:
        op.drop_table(table)
