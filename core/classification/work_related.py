WORK_KEYWORDS = {
    "code", "bug", "error", "exception",
    "api", "docker", "aws", "database",
    "sql", "backend", "frontend",
    "architecture", "ddd", "cqrs", "php", "react", "js",
    "javascript", "work", "job", "algorithm", "experience"
}

def is_work_related(message: str) -> bool:
    text = message.lower()
    return any(k in text for k in WORK_KEYWORDS)