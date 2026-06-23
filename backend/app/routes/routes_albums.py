from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.albums import Album, AlbumCreate, AlbumRead, AlbumUpdate

router = APIRouter(prefix="/albums", tags=["albums"])


def _rollback_and_raise(
    session: Session,
    status_code: int,
    detail: str,
) -> None:
    session.rollback()
    raise HTTPException(status_code=status_code, detail=detail)


@router.get("", response_model=list[AlbumRead])
def list_albums(
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    session: Session = Depends(get_session),
):
    try:
        return session.exec(select(Album).offset(offset).limit(limit)).all()
    except HTTPException:
        raise
    except (IntegrityError, SQLAlchemyError) as exc:
        _rollback_and_raise(session, 400, str(exc))
    except Exception as exc:
        _rollback_and_raise(session, 500, str(exc))


@router.post("", response_model=AlbumRead, status_code=201)
def create_album(
    payload: AlbumCreate,
    session: Session = Depends(get_session),
):
    try:
        record = Album.model_validate(payload)
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


@router.get("/search", response_model=list[AlbumRead])
def search_albums(
    q: str = Query(..., min_length=1),
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    session: Session = Depends(get_session),
):
    try:
        pattern = f"%{q}%"
        return session.exec(
            select(Album).where(Album.title.ilike(pattern)).offset(offset).limit(limit)
        ).all()
    except HTTPException:
        raise
    except (IntegrityError, SQLAlchemyError) as exc:
        _rollback_and_raise(session, 400, str(exc))
    except Exception as exc:
        _rollback_and_raise(session, 500, str(exc))


@router.get("/{record_id}", response_model=AlbumRead)
def get_album(
    record_id: int,
    session: Session = Depends(get_session),
):
    try:
        record = session.get(Album, record_id)
        if not record:
            raise HTTPException(
                status_code=404,
                detail="Album not found",
            )
        return record
    except HTTPException:
        raise
    except (IntegrityError, SQLAlchemyError) as exc:
        _rollback_and_raise(session, 400, str(exc))
    except Exception as exc:
        _rollback_and_raise(session, 500, str(exc))


@router.patch("/{record_id}", response_model=AlbumRead)
def update_album(
    record_id: int,
    payload: AlbumUpdate,
    session: Session = Depends(get_session),
):
    try:
        record = session.get(Album, record_id)
        if not record:
            raise HTTPException(
                status_code=404,
                detail="Album not found",
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


@router.delete("/{record_id}", status_code=204)
def delete_album(record_id: int, session: Session = Depends(get_session)):
    try:
        record = session.get(Album, record_id)
        if not record:
            raise HTTPException(
                status_code=404,
                detail="Album not found",
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
