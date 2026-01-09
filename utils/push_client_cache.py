import os
import sys
import requests
from cachetools import TTLCache
import hashlib

recent_pushes = TTLCache(maxsize=100, ttl=60)

def push(message: str, level: str = "info"):
    message = message.strip().lower()
    key = stable_hash(message)

    if key in recent_pushes:
        print(f"Skipping push (duplicate) {message}", file=sys.stderr, flush=True)

        return

    recent_pushes[key] = True
    try:
        send_to_pushover_or_logger(message, level)
    except Exception as e:
        print(f"Pushover failed: {e}", file=sys.stderr, flush=True)

def stable_hash(message: str) -> str:
    """Return a consistent hash for a string."""
    return hashlib.sha256(message.encode("utf-8")).hexdigest()

def send_to_pushover_or_logger(message: str, level: str = "info"):
    # I might use level later
    try:
        requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": message,
        }
    )
    except Exception as e:
        print(f"Pushover failed: {e}")