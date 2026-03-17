from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Depends, status, HTTPException, Form
from ..src.graph import graph
from .. import schemas
import uuid


router=APIRouter(
    tags = ["Special Route"]
)

MAX_FILE_SIZE = 10485760
@router.post("/upload-recording-get-direct-reports", response_model=schemas.SpecialRouteResponse)
async def get_direct_reports(file: UploadFile = File(...)):
    
    audio_contents=await file.read()
    
    if len(audio_contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Audio file must be smaller than 10 MB"
        )
    try: 
        report = graph.invoke({
                "raw_audio_url": audio_contents
            })
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Error")    
    response_dict={
        "transcript": report['preprocessed_transcript'],
        "analysis_report": report['analysis_report'],
        "scoring_report": report['scoring_report'],
        "governance_report": report['governance_report'],
        "should_flag": report['should_flag'],
        "final_report": report['final_report']
    }
    return response_dict