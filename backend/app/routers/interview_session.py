from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..database import get_db
from .. import models, schemas
from typing import List
import uuid
import io


router = APIRouter(
    tags=["Interview-Sessions"]
)

#For now all routes are allowed for everyone just for ease and simplicity
@router.get("/interview-sessions/get-metadata-all/{user_id}", response_model = List[schemas.Return_session_metadata])
async def get_sessions_metadata(user_id: str, db: AsyncSession = Depends(get_db)):


    stmt = select(models.Users).where(models.Users.user_id == user_id)
    user_row = (await db.execute(stmt)).scalar_one_or_none()
    role = user_row.role
    
    if role not in schemas.SESSION_INFO_ALLOWED_ROLES:   
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=schemas.ROLE_BASED_ACCESS_DENIED.model_dump())
    
    stmt = select(models.Sessions)
    try:
        all_sessions = (await db.execute(stmt)).scalars().all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=schemas.INTERNAL_SERVER_ERROR.model_dump())
    return all_sessions


@router.get("/interview-sessions/get-metadata/{user_id}/{session_id}", response_model=schemas.Return_session_metadata)
async def get_session_metadata(user_id: str, session_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    
    stmt = select(models.Users).where(models.Users.user_id == user_id)
    user_row = (await db.execute(stmt)).scalar_one_or_none()
    role = user_row.role
    
    if role not in schemas.SESSION_INFO_ALLOWED_ROLES:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=schemas.ROLE_BASED_ACCESS_DENIED.model_dump())
    
    stmt = select(models.Sessions).where(models.Sessions.id == session_id)
    session = (await db.execute(stmt)).scalar_one_or_none()
    
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=schemas.SESSION_NOT_FOUND.model_dump())
    
    return session


@router.get("/interview-sessions/get-audio/{user_id}/{session_id}")
async def get_session_audio(user_id: str, session_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    
    stmt = select(models.Users).where(models.Users.user_id == user_id)
    user_row = (await db.execute(stmt)).scalar_one_or_none()
    role = user_row.role
    
    if role not in schemas.SESSION_INFO_ALLOWED_ROLES:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=schemas.ROLE_BASED_ACCESS_DENIED.model_dump())
    
    stmt = select(models.SessionAudio).filter(models.SessionAudio.id == session_id)
    session_audio = (await db.execute(stmt)).scalar_one_or_none()
    
    if session_audio is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=schemas.SESSION_NOT_FOUND.model_dump())
    
    return StreamingResponse(
        io.BytesIO(session_audio.audio),
        media_type="audio/mp3"
    )