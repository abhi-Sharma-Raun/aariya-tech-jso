from langchain_core.messages import HumanMessage
from typing import List
from ..llm_config import llm
from . import prompts
from . import schemas
from ...utils import Transcript


governance_agent_llm = llm.with_structured_output(schemas.GOVERNANCE_AGENT_OUTPUT_JSON_SCHEMA, method="json_mode")

def governance_node(transcript: List[Transcript]):
    
    human_prompt=HumanMessage(content=f"""
        The transcript of the interview is: 
        {transcript}
    """)
    
    governance_report_json=governance_agent_llm.invoke([prompts.governance_system_prompt, human_prompt])
    print("Governance Report JSON:")
    print(governance_report_json)
    governance_report=schemas.GovernanceAgentOutput.model_validate(governance_report_json)
    return governance_report
    