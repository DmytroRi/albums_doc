from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlmodel import Session, SQLModel, select

from app.db.session import get_session
from app.models.links import AlbumVibeLink

router = APIRouter(prefix="/album_vibe_links", tags=["album_vibe_links"])


class AlbumVibeLinkCreate(SQLModel):
    album_id: int
    vibe_id: int


class AlbumVibeLinkUpdate(SQLModel):
    album_id: Optional[int] = None
    vibe_id: Optional[int] = None


def _rollback_and_raise(session: Session, status_code: int, detail: str) -> None:
    session.rollback()
    raise HTTPException(status_code=status_code, detail=detail)


def _get_record(session: Session, album_id: int, vibe_id: int):
    return session.exec(
        select(AlbumVibeLink).where(AlbumVibeLink.album_id == album_id, AlbumVibeLink.vibe_id == vibe_id)
    ).first()


@router.get("", response_model=list[AlbumVibeLink])
def list_album_vibe_links(
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    session: Session = Depends(get_session),
):
    try:
        return session.exec(select(AlbumVibeLink).offset(offset).limit(limit)).all()
    except HTTPException:
        raise
    except (IntegrityError, SQLAlchemyError) as exc:
        _rollback_and_raise(session, 400, str(exc))
    except Exception as exc:
        _rollback_and_raise(session, 500, str(exc))


@router.post("", response_model=AlbumVibeLink, status_code=201)
def create_album_vibe_link(payload: AlbumVibeLinkCreate, session: Session = Depends(get_session)):
    try:
        record = AlbumVibeLink.model_validate(payload)
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


@router.get("/{album_id}/{vibe_id}", response_model=AlbumVibeLink)
def get_album_vibe_link(album_id: int, vibe_id: int, session: Session = Depends(get_session)):
    try:
        record = _get_record(session, album_id, vibe_id)
        if not record:
            raise HTTPException(status_code=404, detail="AlbumVibeLink not found")
        return record
    except HTTPException:
        raise
    except (IntegrityError, SQLAlchemyError) as exc:
        _rollback_and_raise(session, 400, str(exc))
    except Exception as exc:
        _rollback_and_raise(session, 500, str(exc))


@router.patch("/{album_id}/{vibe_id}", response_model=AlbumVibeLink)
def update_album_vibe_link(
    album_id: int, vibe_id: int, payload: AlbumVibeLinkUpdate, session: Session = Depends(get_session)
):
    try:
        record = _get_record(session, album_id, vibe_id)
        if not record:
            raise HTTPException(status_code=404, detail="AlbumVibeLink not found")
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


@router.delete("/{album_id}/{vibe_id}", status_code=204)
def delete_album_vibe_link(album_id: int, vibe_id: int, session: Session = Depends(get_session)):
    try:
        record = _get_record(session, album_id, vibe_id)
        if not record:
            raise HTTPException(status_code=404, detail="AlbumVibeLink not found")
        session.delete(record)
        session.commit()
        return None
    except HTTPException:
        raise
    except (IntegrityError, SQLAlchemyError) as exc:
        _rollback_and_raise(session, 400, str(exc))
    except Exception as exc:
        _rollback_and_raise(session, 500, str(exc))
