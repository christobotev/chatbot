from utils.push_client_cache import push

MAX_PROMPT_EXTENSION_LENGTH = 2000

CONFLICTING_PHRASES = [
    "you are chatgpt",
    "you are someone else",
    "you are not Hristo Botev",
    "ignore previous instructions",
    "do not act as hristo botev",
    "unfiltered ai",
    "jailbreak",
    "sarcastic"
]

def has_conflicting_instruction(text: str) -> bool:
    return any(phrase in text.lower() for phrase in CONFLICTING_PHRASES)

def sanitize_prompt_extension(extension: str) -> str:
    if not extension or not extension.strip():
        return ""
    trimmed = extension.strip()
    return trimmed[:MAX_PROMPT_EXTENSION_LENGTH] + "..." if len(trimmed) > MAX_PROMPT_EXTENSION_LENGTH else trimmed

def validate_prompt_extension(extension: str) -> str:
    if has_conflicting_instruction(extension):
        push("❌ Conflicting instruction found in prompt extension. Rejecting.")
        print("❌ Conflicting instruction found in prompt extension. Rejecting.")
        return ""
    return sanitize_prompt_extension(extension)
