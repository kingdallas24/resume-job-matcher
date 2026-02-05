import re
from typing import List, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


_WORD_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9+.#-]{1,}")


def _tokens(text: str) -> List[str]:
    """
    Simple tokenizer for keyword lists. Keeps tokens like:
    fastapi, docker, rest, sql, api, c++, c#, node.js (ish)
    """
    text = text.lower()
    return _WORD_RE.findall(text)


def _keywords(resume_text: str, job_text: str) -> Tuple[List[str], List[str]]:
    r = set(_tokens(resume_text))
    j = set(_tokens(job_text))

    # Remove ultra-common filler words that create silly "matches"
    stop = {"and", "or", "the", "a", "an", "to", "for", "of", "in", "on", "with", "is", "are"}
    r -= stop
    j -= stop

    matched = sorted(list(r.intersection(j)))
    missing = sorted(list(j.difference(r)))

    return matched, missing


def score_resume(resume_text: str, job_description: str) -> Tuple[int, List[str], List[str]]:
    """
    Returns: (overall_score 0-100, matched_keywords, missing_keywords)

    Scoring method:
    - TF-IDF vectorize resume + job description
    - cosine similarity between vectors
    - map similarity [0,1] -> [0,100]
    """
    resume_text = resume_text or ""
    job_description = job_description or ""

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",   # built-in english stopwords
        ngram_range=(1, 2),     # unigrams + bigrams helps
        max_features=5000
    )

    tfidf = vectorizer.fit_transform([resume_text, job_description])
    sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]  # float in [0,1]

    overall_score = int(round(sim * 100))

    matched, missing = _keywords(resume_text, job_description)

    return overall_score, matched, missing

