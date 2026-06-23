from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlmodel import Session, SQLModel, select

from app.db.session import get_session
from app.models.links import AlbumArtistLink

router = APIRouter(prefix="/album_artist_links", tags=["album_artist_links"])


class AlbumArtistLinkCreate(SQLModel):
    album_id: int
    artist_id: int


class AlbumArtistLinkUpdate(SQLModel):
    album_id: Optional[int] = None
    artist_id: Optional[int] = None


def _rollback_and_raise(session: Session, status_code: int, detail: str) -> None:
    session.rollback()
    raise HTTPException(status_code=status_code, detail=detail)


def _get_record(session: Session, album_id: int, artist_id: int):
    return session.exec(
        select(AlbumArtistLink).where(AlbumArtistLink.album_id == album_id, AlbumArtistLink.artist_id == artist_id)
    ).first()


@router.get("", response_model=list[AlbumArtistLink])
def list_album_artist_links(
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    session: Session = Depends(get_session),
):
    try:
        return session.exec(select(AlbumArtistLink).offset(offset).limit(limit)).all()
    except HTTPException:
        raise
    except (IntegrityError, SQLAlchemyError) as exc:
        _rollback_and_raise(session, 400, str(exc))
    except Exception as exc:
        _rollback_and_raise(session, 500, str(exc))


@router.post("", response_model=AlbumArtistLink, status_code=201)
def create_album_artist_link(payload: AlbumArtistLinkCreate, session: Session = Depends(get_session)):
    try:
        record = AlbumArtistLink.model_validate(payload)
        session.add(record)
        session.commit()
        session.refresh(record)
        return record
    except HTTPException:
        raise
    except (IntegrityError, SQLAlchemyError) as exc:
        _rollback_and_raise(session, 400, str(exc))
    except Exception as exc:
        _rollback_and_raise(session, 500, str(exc))


@router.get("/{album_id}/{artist_id}", response_model=AlbumArtistLink)
def get_album_artist_link(album_id: int, artist_id: int, session: Session = Depends(get_session)):
    try:
        record = _get_record(session, album_id, artist_id)
        if not record:
            raise HTTPException(status_code=404, detail="AlbumArtistLink not found")
        return record
    except HTTPException:
        raise
    except (IntegrityError, SQLAlchemyError) as exc:
        _rollback_and_raise(session, 400, str(exc))
    except Exception as exc:
        _rollback_and_raise(session, 500, str(exc))


@router.patch("/{album_id}/{artist_id}", response_model=AlbumArtistLink)
def update_album_artist_link(
    album_id: int, artist_id: int, payload: AlbumArtistLinkUpdate, session: Session = Depends(get_session)
):
    try:
        record = _get_record(session, album_id, artist_id)
        if not record:
            raise HTTPException(status_code=404, detail="AlbumArtistLink not found")
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(record, key, value)
        session.add(record)
        session.commit()
        session.refresh(record)
        return record
    except HTTPException:
        raise
    except (IntegrityError, SQLAlchemyError) as exc:
        _rollback_and_raise(session, 400, str(exc))
    except Exception as exc:
        _rollback_and_raise(session, 500, str(exc))


@router.delete("/{album_id}/{artist_id}", status_code=204)
def delete_album_artist_link(album_id: int, artist_id: int, session: Session = Depends(get_session)):
    try:
        record = _get_record(session, album_id, artist_id)
        if not record:
            raise HTTPException(status_code=404, detail="AlbumArtistLink not found")
        session.delete(record)
        session.commit()
        return None
    except HTTPException:
        raise
    except (IntegrityError, SQLAlchemyError) as exc:
        _rollback_and_raise(session, 400, str(exc))
    except Exception as exc:
        _rollback_and_raise(session, 500, str(exc))
