from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime
import uuid
from . import utils
from .src.worker_agents import schemas


SESSION_INFO_ALLOWED_ROLES=["ADMIN", "HR_Consultant"]
SESSION_UPLOAD_ALLOWED_ROLES=["HR", "ADMIN"]    #only 'hr' and 'admin' can upload a session

ALLOWED_AUDIO_TYPES = ["audio/mpeg", "audio/mp3"]
ALLOWED_USER_ROLES = ["CANDIDATE", "HR", "ADMIN", "HR_CONSULTANT"]

class UploadInterviewSession(BaseModel):
    hr_id: str
    candidate_id: str
    uploaded_by: str
    role: str
    
class Return_session_metadata(BaseModel):
    session_id: uuid.UUID
    uploaded_by: str
    hr_id: str
    candidate_id: str
    status: Literal["pending", "completed", "failed"]
    transcript_id: uuid.UUID
    created_at: datetime
    is_flagged: bool
    
    
class CreateUser(BaseModel):
    name: str
    role: str
    agency_id: Optional[str] = None

class CreateUserResponse(BaseModel):
    user_id: str  
    
class SpecialRouteResponse(BaseModel):
    transcript: utils.PreprocessedTranscript
    analysis_report: schemas.AnalyzerOutput
    scoring_report: schemas.ScoringAgentOutput
    governance_report: str
    should_flag: bool
    final_report: str
    
    
class ErrorDetail(BaseModel):
    detail: Literal["INTERVAL_SERVER_ERROR", "ROLE_BASED_ACCESS_DENIED", "SESSION_NOT_FOUND", "INVALID_AUDIO_TYPE", "INVALID_USER_ROLE"]
    error_msg: str
    class Config:
        from_attributes = True
        

INTERNAL_SERVER_ERROR = ErrorDetail(
    detail="INTERVAL_SERVER_ERROR", error_msg="There is some internal server problem"
)

ROLE_BASED_ACCESS_DENIED = ErrorDetail(
    detail="ROLE_BASED_ACCESS_DENIED", error_msg="You are not allowed to perform this action"
)

SESSION_NOT_FOUND = ErrorDetail(
    detail="SESSION_NOT_FOUND", error_msg="The session was not found"
)

INVALID_AUDIO_TYPE = ErrorDetail(
    detail="INVALID_AUDIO_TYPE", error_msg=f"This is not allowed audio type.You can only upload these audio types-{ALLOWED_AUDIO_TYPES}"
)

INVALID_USER_ROLE = ErrorDetail(
    detail="INVALID_USER_ROLE" , error_msg=f"This role is not alloweD.You can only take these roles--{ALLOWED_USER_ROLES}"
)