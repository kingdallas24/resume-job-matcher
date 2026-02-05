from fastapi import FastAPI

app = FastAPI(title="Resume ↔ Job Matcher API")

@app.get("/health")
def health():
    return {"status": "ok"}
