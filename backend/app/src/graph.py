from langgraph.graph import StateGraph
from typing import TypedDict, List, Annotated, Any, Optional
from pydantic import BaseModel, Field
from langgraph.constants import END
from .llm_config import transcribe_audio_file
from .worker_agents import analyzer_agent, scoring_agent, governance_agent, schemas
from . import utils
from ..utils import PreprocessedTranscript, Transcript

    

class State(TypedDict):
    raw_audio_url: Annotated[Any, Field(description="This stores url of the raw audio pulled from the source during ingestion")]
    unprocessed_transcript: Annotated[Any, Field(description="This stores the raw transcript generated from the audio")] = None
    preprocessed_transcript: Annotated[PreprocessedTranscript, Field(description="This stores the preprocessed transcript")] = None
    analysis_report: Annotated[Any, Field(description="This stores the analysis report")] = None
    scoring_report: Annotated[Any, Field(description="This stores the scoring report")] = None
    governance_report: Annotated[Any, Field(description="stores the governance report")] = None
    should_flag: Annotated[bool, Field(description="stores the governance report")]=False
    final_report: Annotated[Any, Field(description="stores the final report")] = None
    metadata: Annotated[dict, Field(description="This stores the metadata associated with the interview audio")]
    

def ingestion_node(state: State):
    """
    This node pulls the raw audio and metadata from the source and stores it in the state for preprocessing and further analysis.
    """
    # For now we are just simulating the ingestion by adding placeholder for raw audio and metadata in the state.
    #Otherwise we may have 2 options: 1. Store audio in state(Pull it here) 2. Don't store it in state(Pull it in process_audio_node) use directly
    # I prefer Option 2 as Option 1 is difficult to trace.
    pass


def process_audio_node(state: State):
    """
    takes the raw audio as input and processes it to generate a raw transcript.
    """
    audio_url=state['raw_audio_url']
    transcript=transcribe_audio_file(audio_url)
    return {
        "unprocessed_transcript": transcript
    }
    
def preprocessing_node(state: State):
    """
    takes the unprocessed/raw transcript and preprocesses it to generate a structured transcript.
    """
    
    unprocessed_transcript=state['unprocessed_transcript']
    preprocessed_transcripts=[]
    for ut in unprocessed_transcript:
        ts=Transcript(
            start_time=ut.start, end_time=ut.end, speaker=ut.speaker, text=utils.mask_sensitive_data(ut.text)    #storing masked text
        )
        preprocessed_transcripts.append(ts)
    
    final_preprocessed_transcript=PreprocessedTranscript(
        metadata={"total_duration_milliseconds": unprocessed_transcript[-1].end},
        transcript=preprocessed_transcripts
    )
    return {
        "preprocessed_transcript": final_preprocessed_transcript
    }
    

def analysis_node(state: State):
    """
    This node takes the preprocessed transcript and performs various analyses to generate observations regarding Tone, professionalism and Engagement and other insights.
    """
    analysis_report=analyzer_agent.analysis_node(state['preprocessed_transcript'].transcript)
    return {
        "analysis_report": analysis_report
    }
   

def governance_node(state: State):
    """
    This node takes the transcript and checks for compliance with predefined governance rules and policies.
    """
    governance_agent_out=governance_agent.governance_node(state['preprocessed_transcript'].transcript)
    return {
        "governance_report": governance_agent_out.governance_report,
        "should_flag": governance_agent_out.should_flag
    }


def scoring_node(state: State):
    """
    Finalaizes the grade and sends the notifications to the HR dashboard and Super Admin Dashboard.
    """
    scoring_report = scoring_agent.scoring_node(state['analysis_report'])
    return {
        "scoring_report": scoring_report
    }
    

def final_report_node(state: State):
    """
    This node compiles all the previous outputs and generates a final report that can be sent to the HR dashboard and Super Admin Dashboard.
    """
    final_report="Not implemented yet"
    return {
        "final_report": final_report
    }
    


builder=StateGraph(State)
builder.add_node("ingestion_node", ingestion_node)
builder.add_node("process_audio_node", process_audio_node)  
builder.add_node("preprocessing_node", preprocessing_node)
builder.add_node("analysis_node", analysis_node)
builder.add_node("governance_node", governance_node)
builder.add_node("scoring_node", scoring_node)
builder.add_node("final_report_node", final_report_node)
builder.add_edge("ingestion_node", "process_audio_node")
builder.add_edge("process_audio_node", "preprocessing_node")
builder.add_edge("preprocessing_node", "analysis_node")
builder.add_edge("preprocessing_node", "governance_node")
builder.add_edge("analysis_node", "scoring_node")
builder.add_edge("governance_node", "final_report_node")
builder.add_edge("scoring_node", "final_report_node")
builder .add_edge("final_report_node", END)
builder.set_entry_point("ingestion_node")

graph=builder.compile()

'''
png = graph.get_graph().draw_mermaid_png()
with open("graph.png", "wb") as f:
    f.write(png)
'''


