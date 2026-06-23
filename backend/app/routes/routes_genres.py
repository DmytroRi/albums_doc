from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.genres import Genre, GenreCreate, GenreRead, GenreUpdate

router = APIRouter(prefix="/genres", tags=["genres"])


def _rollback_and_raise(
    session: Session,
    status_code: int,
    detail: str,
) -> None:
    session.rollback()
    raise HTTPException(status_code=status_code, detail=detail)


@router.get("", response_model=list[GenreRead])
def list_genres(
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    session: Session = Depends(get_session),
):
    try:
        return session.exec(select(Genre).offset(offset).limit(limit)).all()
    except HTTPException:
        raise
    except (IntegrityError, SQLAlchemyError) as exc:
        _rollback_and_raise(session, 400, str(exc))
    except Exception as exc:
        _rollback_and_raise(session, 500, str(exc))


@router.post("", response_model=GenreRead, status_code=201)
def create_genre(
    payload: GenreCreate,
    session: Session = Depends(get_session),
):
    try:
        record = Genre.model_validate(payload)
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


@router.get("/{record_id}", response_model=GenreRead)
def get_genre(
    record_id: int,
    session: Session = Depends(get_session),
):
    try:
        record = session.get(Genre, record_id)
        if not record:
            raise HTTPException(status_code=404, detail="Genre not found")
        return record
    except HTTPException:
        raise
    except (IntegrityError, SQLAlchemyError) as exc:
        _rollback_and_raise(session, 400, str(exc))
    except Exception as exc:
        _rollback_and_raise(session, 500, str(exc))


@router.patch("/{record_id}", response_model=GenreRead)
def update_genre(
    record_id: int,
    payload: GenreUpdate,
    session: Session = Depends(get_session),
):
    try:
        record = session.get(Genre, record_id)
        if not record:
            raise HTTPException(status_code=404, detail="Genre not found")
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
def delete_genre(
    record_id: int,
    session: Session = Depends(get_session),
):
    try:
        record = session.get(Genre, record_id)
        if not record:
            raise HTTPException(status_code=404, detail="Genre not found")
        session.delete(record)
        session.commit()
        return None
    except HTTPException:
        raise
    except (IntegrityError, SQLAlchemyError) as exc:
        _rollback_and_raise(session, 400, str(exc))
    except Exception as exc:
        _rollback_and_raise(session, 500, str(exc))
