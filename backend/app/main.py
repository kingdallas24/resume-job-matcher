from fastapi import FastAPI
from .schemas import ScoreRequest, ScoreResponse
from .scorer import score_resume

app = FastAPI(
    title="Resume ↔ Job Matcher API",
    version="0.1.0",
    description="API to score how well a resume matches a job description"
)


@app.get("/health")
def health():
    """
    Health check endpoint
    """
    return {"status": "ok"}


@app.post("/score", response_model=ScoreResponse)
def score(payload: ScoreRequest):
    """
    Score a resume against a job description
    """
    overall_score, matched, missing = score_resume(
        payload.resume_text,
        payload.job_description
    )

    return {
        "overall_score": overall_score,
        "matched_keywords": matched,
        "missing_keywords": missing,
    }
