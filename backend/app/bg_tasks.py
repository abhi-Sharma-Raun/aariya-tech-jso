from .src.graph import graph
from . import models
import uuid
from sqlalchemy import select
from .database import AsyncSessionLocal

async def prepare_reports(session_id: uuid.UUID, audio_contents):
    
    
    # For now i am using audio directly without uploading it to a remote cloud.Change it later
    
    async with AsyncSessionLocal() as db_session:
        
        stmt_interview = select(models.Sessions).where(models.Sessions.id == session_id)
        result = await db_session.execute(stmt_interview)
        interview_session = result.scalar_one_or_none()
        '''
        stmt_audio = select(models.SessionAudio).where(models.SessionAudio.id == session_id)
        result = await db_session.execute(stmt_audio)
        interview_audio = result.scalar_one_or_none()
        '''
        if interview_session is None:
            return

        #audio_contents = interview_audio.audio
        audio_contents = audio_contents
        metadata = {
            "session_id": session_id,
            "hr_id": interview_session.hr_id,
            "candidate_id": interview_session.candidate_id
        }
        
        try:
            reports = graph.invoke({
                "raw_audio_url": audio_contents,
                "metadata": metadata
            })

        except Exception as e:
            print(f"Graph Execution failed: {e}")
            interview_session.status = "failed"
            await db_session.commit()
            return
        
        transcript_id = uuid.uuid4()

        transcript = models.Transcripts(
            id=transcript_id,
            session_id=session_id,
            transcript=reports["preprocessed_transcript"].model_dump()
        )

        report_row = models.Reports(
            session_id=session_id,
            analysis_report=reports["analysis_report"].model_dump(),
            governance_report=reports["governance_report"],
            scoring_report=reports["scoring_report"].model_dump(),
            final_report=reports["final_report"]
        )

        db_session.add_all([transcript, report_row])

        interview_session.status = "completed"
        interview_session.transcript_id = transcript_id
        interview_session.is_flagged = True if reports['should_flag'] else False
        try:
            await db_session.commit()
        except Exception as e:
            interview_session.status = "failed"
            await db_session.commit()
            return