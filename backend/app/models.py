from .database import Base
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql.sqltypes import TIMESTAMP, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy import Column,String, ForeignKey, LargeBinary, UniqueConstraint
from sqlalchemy.sql.expression import text



class Sessions(Base):
    __tablename__ = "session"
    id = Column(UUID(as_uuid=True),primary_key=True, server_default=text("gen_random_uuid()"))
    uploaded_by = Column(String, ForeignKey("users.user_id"), nullable=False)
    hr_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    candidate_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    status = Column(Enum("pending", "completed", "failed", name="session_status"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    is_flagged = Column(Boolean, nullable=True)
    transcript_id = Column(UUID(as_uuid=True), ForeignKey("transcripts.id"), nullable=True)
    
    transcript = relationship("Transcripts", foreign_keys=[transcript_id])
    hr = relationship("Users", foreign_keys=[hr_id])
    candidate = relationship("Users", foreign_keys=[candidate_id])
    
class SessionAudio(Base):
    __tablename__="session_audio"
    id = Column(UUID(as_uuid=True), ForeignKey("session.id"), primary_key=True)
    audio = Column(LargeBinary, nullable=False)   #if using AWS S3 then store audio bytes there and store url here instead of audio bytes
    
    
class Transcripts(Base):
    __tablename__ = "transcripts"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    session_id = Column(UUID(as_uuid=False), ForeignKey("session.id"), nullable=False)
    transcript = Column(JSONB, nullable=False)     # it is preprocessed and masked transcript          <-------------
    __table_args__=(
        UniqueConstraint("session_id", name="unique_session_transcript"),
    )


class Reports(Base):
    __tablename__ = "reports"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    session_id = Column(UUID(as_uuid=False), ForeignKey("session.id"), nullable=False)
    analysis_report = Column(JSONB, nullable=False)
    scoring_report = Column(JSONB, nullable=False)
    governance_report = Column(String, nullable=False)
    final_report = Column(String, nullable=False)
    __table_args__=(
        UniqueConstraint("session_id", name="unique_session_report"),
    )
    
class Users(Base):
    __tablename__="users"
    user_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    role = Column(Enum("CANDIDATE", "HR", "ADMIN", "HR_CONSULTANT", name="user_role"), nullable=False)
    agency_id = Column(String, nullable=True)    
