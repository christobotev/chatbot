# from agents import Agent, function_tool
# from agents.extensions.models.litellm_model import LitellmModel
# from db.models import save_feedback
# from tools.feedback_reflection import (
#     tool_is_feedback_reflectable,
#     tool_generate_prompt_reflection
# )
# from pathlib import Path
# import os

# PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"

# def load_instructions(filename: str) -> str:
#     return (PROMPTS_DIR / filename).read_text(encoding="utf-8").strip()

# @function_tool
# def tool_save_feedback(feedback: str, sentiment: str, user: str, is_reflectable: bool | None = None):
#     """Record user feedback."""

#     save_feedback(feedback, sentiment, user, is_reflectable)

#     return {
#         "status": "success",
#         "message": "Recorded successfully",
#         "data": {}
#     }

# agent_feedback_reflection = Agent(
#     name="ReflectOnFeedbackAgent",
#     model=LitellmModel("openai/gpt-4o-mini", api_key=os.environ["OPENAI_API_KEY"]),
#     instructions=load_instructions("../prompts/feedback_reflect.txt"),
#     tools=[
#         tool_is_feedback_reflectable,
#         tool_generate_prompt_reflection,
#         tool_save_feedback
#     ]
# )
