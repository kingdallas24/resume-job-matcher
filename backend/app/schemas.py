from pydantic import BaseModel
from typing import List

class ScoreRequest(BaseModel):
    resume_text: str
    job_description: str

class ScoreResponse(BaseModel):
    overall_score: float
    matched_keywords: List[str]
    missing_keywords: List[str]
