from pathlib import Path

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"

def read(filename: str) -> str:
    return (PROMPTS_DIR / filename).read_text(encoding="utf-8").strip()

def build_system_prompt() -> str:
    return "\n\n".join([
        read("identity.md").format(name="Hristo Botev"),
        read("constraints.md"),
        read("behavior.md"),
        read("tools.md"),
        read("impact_examples.md"),
        read("resume_summary.md"),
        read("work_experience.md"),
        read("style.md"),
    ])