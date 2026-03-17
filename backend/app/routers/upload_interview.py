from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Depends, status, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..database import get_db
from ..bg_tasks import prepare_reports
from .. import models, schemas
import uuid


router=APIRouter(
    tags = ["Upload Interview"]
)

MAX_FILE_SIZE = 10485760

@router.post("/upload-interview-session")
async def upload_interview_session(
    bg_tasks: BackgroundTasks,
    hr_id: str = Form(...), candidate_id: str = Form(...), uploaded_by: str = Form(...),
    file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    
    
    #Not adding verification for hr_id, candidate_id, etc. So make sure to enter correct info 
    
    stmt = select(models.Users).where(models.Users.user_id == uploaded_by)
    user_row = (await db.execute(stmt)).scalar_one_or_none()
    role = user_row.role
    
    if role not in schemas.SESSION_UPLOAD_ALLOWED_ROLES:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=schemas.ROLE_BASED_ACCESS_DENIED.model_dump())
    
    
    if file.content_type not in schemas.ALLOWED_AUDIO_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=schemas.INVALID_AUDIO_TYPE.model_dump())

    
    audio_contents=await file.read()
    # Upload the file to a storage service and get the URL (Here we are skipping this step and directly sending the file contents to the background task)
    
    if len(audio_contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Audio file must be smaller than 10 MB"
        )
    
    session_id = uuid.uuid4()
    new_interview_session = models.Sessions(
        id = session_id,
        uploaded_by=uploaded_by,
        hr_id=hr_id,
        candidate_id=candidate_id,
        status="pending"
    )
    '''
    interview_audio_row = models.SessionAudio(
        id = session_id,
        audio = audio_contents
    )
    '''
    try:
        db.add(new_interview_session)
        '''
        await db.flush()
        db.add(interview_audio_row)
        '''
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=schemas.INTERNAL_SERVER_ERROR.model_dump())
    bg_tasks.add_task(prepare_reports, session_id=session_id, audio_contents=audio_contents)

    return {"msg": "Interview has been uploaded successully. You can use the session id to check the status of the upload", "Session_id": session_id}
