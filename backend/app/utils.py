from pydantic import BaseModel
from typing import List
class Transcript(BaseModel):
    """
    schema for a single Transcript
    """
    start_time: int
    end_time: int
    speaker: str
    text: str

class PreprocessedTranscript(BaseModel):
    """
    schema for Final PreprocessedTranscript
    """
    metadata: dict
    transcript: List[Transcript]
    # not including ''agent interventions'' in audio model.
    #including it here will increase cost by much as audio models are expensive, we can consider addding it using ''Audio models or language models'' depending on cost and performance.
    #For now i am doing it using language model in ''analysis_agent'' because of cost.
    """  
    "agent_interventions": [
    {
      "timestamp": "00:12",
      "type": "Tone_Alert",
      "description": "Consultant tone shifted to 'Instructional'; Candidate engagement is 'High'."
     }]}
    """