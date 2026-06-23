from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlmodel import Session, SQLModel, select

from app.db.session import get_session
from app.models.links import AlbumGenreLink

router = APIRouter(prefix="/album_genre_links", tags=["album_genre_links"])


class AlbumGenreLinkCreate(SQLModel):
    album_id: int
    genre_id: int


class AlbumGenreLinkUpdate(SQLModel):
    album_id: Optional[int] = None
    genre_id: Optional[int] = None


def _rollback_and_raise(
    session: Session,
    status_code: int,
    detail: str,
) -> None:
    session.rollback()
    raise HTTPException(status_code=status_code, detail=detail)


def _get_record(session: Session, album_id: int, genre_id: int):
    return session.exec(
        select(AlbumGenreLink).where(
            AlbumGenreLink.album_id == album_id,
            AlbumGenreLink.genre_id == genre_id,
        )
    ).first()


@router.get("", response_model=list[AlbumGenreLink])
def list_album_genre_links(
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    session: Session = Depends(get_session),
):
    try:
        return session.exec(select(AlbumGenreLink).offset(offset).limit(limit)).all()
    except HTTPException:
        raise
    except (IntegrityError, SQLAlchemyError) as exc:
        _rollback_and_raise(session, 400, str(exc))
    except Exception as exc:
        _rollback_and_raise(session, 500, str(exc))


@router.post("", response_model=AlbumGenreLink, status_code=201)
def create_album_genre_link(
    payload: AlbumGenreLinkCreate,
    session: Session = Depends(get_session),
):
    try:
        record = AlbumGenreLink.model_validate(payload)
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


@router.get("/{album_id}/{genre_id}", response_model=AlbumGenreLink)
def get_album_genre_link(
    album_id: int,
    genre_id: int,
    session: Session = Depends(get_session),
):
    try:
        record = _get_record(session, album_id, genre_id)
        if not record:
            raise HTTPException(
                status_code=404,
                detail="AlbumGenreLink not found",
            )
        return record
    except HTTPException:
        raise
    except (IntegrityError, SQLAlchemyError) as exc:
        _rollback_and_raise(session, 400, str(exc))
    except Exception as exc:
        _rollback_and_raise(session, 500, str(exc))


@router.patch("/{album_id}/{genre_id}", response_model=AlbumGenreLink)
def update_album_genre_link(
    album_id: int,
    genre_id: int,
    payload: AlbumGenreLinkUpdate,
    session: Session = Depends(get_session),
):
    try:
        record = _get_record(session, album_id, genre_id)
        if not record:
            raise HTTPException(
                status_code=404,
                detail="AlbumGenreLink not found",
            )
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


@router.delete("/{album_id}/{genre_id}", status_code=204)
def delete_album_genre_link(
    album_id: int,
    genre_id: int,
    session: Session = Depends(get_session),
):
    try:
        record = _get_record(session, album_id, genre_id)
        if not record:
            raise HTTPException(
                status_code=404,
                detail="AlbumGenreLink not found",
            )
        session.delete(record)
        session.commit()
        return None
    except HTTPException:
        raise
    except (IntegrityError, SQLAlchemyError) as exc:
        _rollback_and_raise(session, 400, str(exc))
    except Exception as exc:
        _rollback_and_raise(session, 500, str(exc))
