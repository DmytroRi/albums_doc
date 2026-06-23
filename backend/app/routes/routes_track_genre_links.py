from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlmodel import Session, SQLModel, select

from app.db.session import get_session
from app.models.links import TrackGenreLink

router = APIRouter(prefix="/track_genre_links", tags=["track_genre_links"])


class TrackGenreLinkCreate(SQLModel):
    track_id: int
    genre_id: int


class TrackGenreLinkUpdate(SQLModel):
    track_id: Optional[int] = None
    genre_id: Optional[int] = None


def _rollback_and_raise(session: Session, status_code: int, detail: str) -> None:
    session.rollback()
    raise HTTPException(status_code=status_code, detail=detail)


def _get_record(session: Session, track_id: int, genre_id: int):
    return session.exec(
        select(TrackGenreLink).where(TrackGenreLink.track_id == track_id, TrackGenreLink.genre_id == genre_id)
    ).first()


@router.get("", response_model=list[TrackGenreLink])
def list_track_genre_links(
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    session: Session = Depends(get_session),
):
    try:
        return session.exec(select(TrackGenreLink).offset(offset).limit(limit)).all()
    except HTTPException:
        raise
    except (IntegrityError, SQLAlchemyError) as exc:
        _rollback_and_raise(session, 400, str(exc))
    except Exception as exc:
        _rollback_and_raise(session, 500, str(exc))


@router.post("", response_model=TrackGenreLink, status_code=201)
def create_track_genre_link(payload: TrackGenreLinkCreate, session: Session = Depends(get_session)):
    try:
        record = TrackGenreLink.model_validate(payload)
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


@router.get("/{track_id}/{genre_id}", response_model=TrackGenreLink)
def get_track_genre_link(track_id: int, genre_id: int, session: Session = Depends(get_session)):
    try:
        record = _get_record(session, track_id, genre_id)
        if not record:
            raise HTTPException(status_code=404, detail="TrackGenreLink not found")
        return record
    except HTTPException:
        raise
    except (IntegrityError, SQLAlchemyError) as exc:
        _rollback_and_raise(session, 400, str(exc))
    except Exception as exc:
        _rollback_and_raise(session, 500, str(exc))


@router.patch("/{track_id}/{genre_id}", response_model=TrackGenreLink)
def update_track_genre_link(
    track_id: int, genre_id: int, payload: TrackGenreLinkUpdate, session: Session = Depends(get_session)
):
    try:
        record = _get_record(session, track_id, genre_id)
        if not record:
            raise HTTPException(status_code=404, detail="TrackGenreLink not found")
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


@router.delete("/{track_id}/{genre_id}", status_code=204)
def delete_track_genre_link(track_id: int, genre_id: int, session: Session = Depends(get_session)):
    try:
        record = _get_record(session, track_id, genre_id)
        if not record:
            raise HTTPException(status_code=404, detail="TrackGenreLink not found")
        session.delete(record)
        session.commit()
        return None
    except HTTPException:
        raise
    except (IntegrityError, SQLAlchemyError) as exc:
        _rollback_and_raise(session, 400, str(exc))
    except Exception as exc:
        _rollback_and_raise(session, 500, str(exc))
