from langchain_core.messages import HumanMessage
from ..llm_config import llm
from . import prompts
from . import schemas

scoring_agent_llm=llm.with_structured_output(schemas.SCORING_AGENT_OUTPUT_JSON_SCHEMA, method="json_mode")

def scoring_node(analysis_report):
    
    human_prompt=HumanMessage(content=f"""Analysis Report: {analysis_report}""")
    scoring_report_json=scoring_agent_llm.invoke([prompts.scoring_system_prompt, human_prompt])
    print("Scoring Report JSON:")
    print(scoring_report_json)
    scoring_report=schemas.ScoringAgentOutput.model_validate(scoring_report_json)
    return scoring_report