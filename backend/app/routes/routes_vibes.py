from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.vibes import Vibe, VibeCreate, VibeRead, VibeUpdate

router = APIRouter(prefix="/vibes", tags=["vibes"])


def _rollback_and_raise(
    session: Session,
    status_code: int,
    detail: str,
) -> None:
    session.rollback()
    raise HTTPException(status_code=status_code, detail=detail)


@router.get("", response_model=list[VibeRead])
def list_vibes(
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    session: Session = Depends(get_session),
):
    try:
        return session.exec(select(Vibe).offset(offset).limit(limit)).all()
    except HTTPException:
        raise
    except (IntegrityError, SQLAlchemyError) as exc:
        _rollback_and_raise(session, 400, str(exc))
    except Exception as exc:
        _rollback_and_raise(session, 500, str(exc))


@router.post("", response_model=VibeRead, status_code=201)
def create_vibe(
    payload: VibeCreate,
    session: Session = Depends(get_session),
):
    try:
        record = Vibe.model_validate(payload)
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


@router.get("/{record_id}", response_model=VibeRead)
def get_vibe(
    record_id: int,
    session: Session = Depends(get_session),
):
    try:
        record = session.get(Vibe, record_id)
        if not record:
            raise HTTPException(
                status_code=404,
                detail="Vibe not found",
            )
        return record
    except HTTPException:
        raise
    except (IntegrityError, SQLAlchemyError) as exc:
        _rollback_and_raise(session, 400, str(exc))
    except Exception as exc:
        _rollback_and_raise(session, 500, str(exc))


@router.patch("/{record_id}", response_model=VibeRead)
def update_vibe(
    record_id: int,
    payload: VibeUpdate,
    session: Session = Depends(get_session),
):
    try:
        record = session.get(Vibe, record_id)
        if not record:
            raise HTTPException(
                status_code=404,
                detail="Vibe not found",
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
def delete_vibe(
    record_id: int,
    session: Session = Depends(get_session),
):
    try:
        record = session.get(Vibe, record_id)
        if not record:
            raise HTTPException(
                status_code=404,
                detail="Vibe not found",
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
