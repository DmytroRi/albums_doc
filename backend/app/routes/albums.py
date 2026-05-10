from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.db.session import get_session
from app.schemas.album import AlbumCreate, AlbumRead, AlbumSummary, AlbumUpdate
from app.services.album_service import AlbumService

router = APIRouter(prefix="/albums", tags=["albums"])


@router.post("", response_model=AlbumRead, status_code=201)
def create_album(payload: AlbumCreate, session: Session = Depends(get_session)):
    return AlbumService(session).create_album(payload)


@router.get("", response_model=list[AlbumSummary])
def list_albums(session: Session = Depends(get_session)):
    return AlbumService(session).list_albums()


@router.get("/search", response_model=list[AlbumSummary])
def search_albums(q: str = Query(..., min_length=1), session: Session = Depends(get_session)):
    return AlbumService(session).search_albums(q)


@router.get("/{album_id}", response_model=AlbumRead)
def get_album(album_id: int, session: Session = Depends(get_session)):
    album = AlbumService(session).get_album(album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    return album


@router.put("/{album_id}", response_model=AlbumRead)
def update_album(album_id: int, payload: AlbumUpdate, session: Session = Depends(get_session)):
    album = AlbumService(session).update_album(album_id, payload)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    return album


@router.delete("/{album_id}", status_code=204)
def delete_album(album_id: int, session: Session = Depends(get_session)):
    success = AlbumService(session).delete_album(album_id)
    if not success:
        raise HTTPException(status_code=404, detail="Album not found")
    return None
