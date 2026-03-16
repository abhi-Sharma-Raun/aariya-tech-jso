from langchain_core.messages import HumanMessage
from ..llm_config import llm
from . import prompts
from . import schemas

analyzer_agent_llm=llm.with_structured_output(schemas.ANALYZER_OUTPUT_JSON_SCHEMA, method="json_mode")

def analysis_node(transcript):
    """
    This node takes the preprocessed transcript and performs various analyses to generate observations regarding Tone, professionalism and Engagement and other insights.
    """
    
    transcript_prompt=HumanMessage(content=f"""Timestamped Transcript of the interview: {transcript}""")
    analysis_report_json=analyzer_agent_llm.invoke([prompts.analyzer_system_prompt, transcript_prompt])
    print("Analysis Report JSON:")
    print(analysis_report_json)
    analysis_report=schemas.AnalyzerOutput.model_validate(analysis_report_json)
    return analysis_report