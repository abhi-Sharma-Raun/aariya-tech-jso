from pydantic import BaseModel, Field
from typing import List, Literal, Optional


ANALYZER_OUTPUT_JSON_SCHEMA = {
    "name": "analyzer_output",
    "description": "Output the structured analysis of the interview session.",
    "parameters": {
        "type": "object",
        "properties":{
            "Overall Sentiment": {
                "type": "string",
                "enum": ["Cold", "Neutral", "Warm", "Empathetic"],
                "description": "Overall tone of the session."
            },
            "Events": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "timestamp": {
                            "type": "string",
                            "description": "Time of the observed event."
                        },
                        "event": {
                            "type": "string",
                            "description": "Description of the observed behavior."
                        }
                    },
                    "required": ["timestamp", "event"]
                },
            },
            "introduction_completed": {
                "type": "boolean",
                "description": "Whether the consultant completed the introduction protocol."
            },
            "ats_score_explained": {
                "type": "boolean",
                "description": "Whether the consultant explained the ATS score to the candidate."
            },
            "num_interruptions": {
                "type": "integer",
                "description": "Number of times the consultant interrupted the candidate."
            },
            "observation": {
                "type": "string",
                "description": "Additional observations about candidate behavior or session dynamics."
            }
        },
        "required": ["Overall Sentiment", "Events", "introduction_completed", "ats_score_explained", "num_interruptions"]
    }
}


SCORING_AGENT_OUTPUT_JSON_SCHEMA = {
    "name": "scoring_agent_output",
    "description": "Output the final scores and coaching tips based on the analysis report.",
    "parameters": {
        "type": "object",
        "properties": {
            "professionalism_score": {
                "type": "integer",
                "description": "Score for professionalism out of 100."
            },
            "soft_skills_score": {
                "type": "integer",
                "description": "Score for soft skills out of 100."
            },
            "engagement_index": {
                "type": "integer",
                "description": "Engagement index score out of 100."
            },
            "final_grade": {
                "type": "integer",
                "description": "Final grade calculated from the individual scores, out of 100."
            },
            "coaching_tips": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "List of coaching tips for improvement."
            }
        },
        "required": ["professionalism_score", "soft_skills_score", "engagement_index", "final_grade", "coaching_tips"]
    }
}

GOVERNANCE_AGENT_OUTPUT_JSON_SCHEMA = {
    "name": "governance_agent_output",
    "description": "Output a governance report mentioning if rules and policies were followed correctly",
    "parameters": {
        "type": "object",
        "properties": {
            "governance_report": {
                "type": "string",
                "description": "Complete Governance report telling which rules were rightly followed and which were weakly followed and which were not followed"
            },
            "should_flag": {
                "type": "boolean",
                "description": "Should this session be flagged for internal review."
            }       
        }
    }  
}


"""Analyzer Agent Output Schema"""
class Event(BaseModel):
    timestamp: str
    event: str
class AnalyzerOutput(BaseModel):
    overall_sentiment: Literal["Cold", "Neutral", "Warm", "Empathetic"]
    events: List[Event]
    introduction_completed: bool
    ats_score_explained: bool
    num_interruptions: int
    Observation: Optional[str] = None
    
    
    
"""Scoring Agent Output Schema"""
class ScoringAgentOutput(BaseModel):
    professionalism_score: int
    soft_skills_score: int
    engagement_index: int
    final_grade: int
    coaching_tips: List[str]
    
    
"""Governance Agent Output Schema"""
class GovernanceAgentOutput(BaseModel):
    governance_report: str
    should_flag: bool