from langchain_core.messages import HumanMessage
from typing import List
from ..llm_config import llm
from . import prompts
from . import schemas
from ...utils import Transcript



analyzer_agent_llm=llm.with_structured_output(schemas.ANALYZER_OUTPUT_JSON_SCHEMA, method="json_mode")

def analysis_node(transcript: List[Transcript]):
    """
    This node takes the preprocessed transcript and performs various analyses to generate observations regarding Tone, professionalism and Engagement and other insights.
    """
    
    human_prompt=HumanMessage(content=f"""
        Timestamped Transcript of the interview: 
        {transcript}
    """)
    analysis_report_json=analyzer_agent_llm.invoke([prompts.analyzer_system_prompt, human_prompt])
    
    analysis_report=schemas.AnalyzerOutput.model_validate(analysis_report_json)
    return analysis_report