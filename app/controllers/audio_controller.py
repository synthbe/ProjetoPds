from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from schemas.audio_schema import AudioCreate, AudioUpdate, AudioOut
from app.repositories.audio_repository import AudioRepository
from session import get_db

router = APIRouter(prefix="/audios", tags=["Audios"])

@router.post("/", response_model=AudioOut, status_code=status.HTTP_201_CREATED)
def create_audio(data: AudioCreate, db: Session=Depends(get_db)):
    repo = AudioRepository(db)
    return repo.create(data)

@router.get("/{audio_id}", response_model=AudioOut, status_code=status.HTTP_200_OK)
def get_audio(audio_id: int, db: Session=Depends(get_db)):
    repo = AudioRepository(db)
    audio = repo.get_by_id(audio_id)
    if not audio:
        raise HTTPException(status_code=404, detail="Audio not found")
    return audio

@router.put("/{audio_id}", response_model=AudioOut, status_code=status.HTTP_200_OK)
def update_audio(audio_id: int, audio_data: AudioUpdate, db: Session=Depends(get_db)):
    repo = AudioRepository(db)
    success = repo.update(audio_data, audio_id)
    if not success:
        raise HTTPException(status_code=404, detail="Audio not found")
    return success

@router.put("/{audio_id}", response_model=AudioOut, status_code=status.HTTP_200_OK)
def delete_audio(audio_id: int, db: Session=Depends(get_db)):
    repo = AudioRepository(db)
    success = repo.delete(audio_id)
    if not success:
        raise HTTPException(status_code=404, detail="Audio not found")
    return success

@router.put("/{audio_id}", response_model=AudioOut, status_code=status.HTTP_200_OK)
def toggle_audio_pin(audio_id: int, db: Session=Depends(get_db)):
    repo = AudioRepository(db)
    success = repo.toggle_audio_pin(audio_id)
    if not success:
        raise HTTPException(status_code=404, detail="Audio not found")
    return success
