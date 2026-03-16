from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Depends, status, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from .. import models, schemas
import random

router=APIRouter(
    tags = ["Create Simple User(Candidate or HR)"]
)



@router.post("/create-simple-user", response_model=schemas.CreateUserResponse)
async def create_user(info: schemas.CreateUser, db: AsyncSession = Depends(get_db)):
    
    
    '''Generating a user id in basic way'''
    
    
    
    if info.role not in schemas.ALLOWED_USER_ROLES:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=schemas.INVALID_USER_ROLE.model_dump())
    
    x=""
    for i in range(0,5):
        x = x+f"{random.randint(1,9)}"
    
    user_id = info.name+x
    
    new_user=None
    if info.agency_id is not None:
        new_user = models.Users(
            user_id = user_id,
            name = info.name,
            role = info.role,
            agency_id = info.agency_id
        )
    else:
        new_user = models.Users(
            user_id = user_id,
            name = info.name,
            role = info.role
        )
        
    
    db.add(new_user)
    try:
        await db.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=schemas.INTERNAL_SERVER_ERROR.model_dump())
    
    return {"user_id": user_id}


