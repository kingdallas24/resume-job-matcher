import re
from typing import List, Tuple

def extract_keywords(text: str) -> List[str]:
    tokens = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    return list(set(tokens))

def score_resume(resume_text: str, job_description: str) -> Tuple[float, List[str], List[str]]:
    resume_keywords = set(extract_keywords(resume_text))
    job_keywords = set(extract_keywords(job_description))

    matched = sorted(resume_keywords & job_keywords)
    missing = sorted(job_keywords - resume_keywords)

    if not job_keywords:
        score = 0.0
    else:
        score = round(len(matched) / len(job_keywords) * 100, 2)

    return score, matched, missing
