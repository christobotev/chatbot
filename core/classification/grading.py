"""
IMPORTANT:
Do NOT add LLM calls here.

Grading is intentionally deterministic and synchronous.
LLM-based enrichment must be done asynchronously.
"""
RULES = {
    "core_dev": {
        "weight": 4,
        "keywords": ["code", "bug", "refactor", "algorithm"]
    },
    "infra": {
        "weight": 3,
        "keywords": ["docker", "aws", "deploy", "ci", "ci/di"]
    },
    "data": {
        "weight": 3,
        "keywords": ["sql", "database", "model"]
    },
    "career": {
        "weight": 1,
        "keywords": ["resume", "interview", "job"]
    }
}

def grade(message: str) -> dict:
    text = message.lower()
    score = 0
    categories = {}

    for name, rule in RULES.items():
        hits = [k for k in rule["keywords"] if k in text]
        if hits:
            score += rule["weight"]
            categories[name] = hits

    return {
        "score": min(score, 10),
        "categories": categories,
        "is_work_related": score >= 3
    }