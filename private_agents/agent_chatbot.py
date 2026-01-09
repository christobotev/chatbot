from agents import Agent, function_tool, set_tracing_disabled
from core.system_prompt import build_system_prompt
from core.prompt_utils import validate_prompt_extension
from db.models import get_prompt
from agents.extensions.models.litellm_model import LitellmModel
# from private_agents.agent_feedback_reflection import agent_feedback_reflection
from utils.push_client_cache import push
import os

RESUME_LINK = "https://chat.botevllc.com/downloads/hristo_botev_resume_placeholder.pdf"

@function_tool
def tool_record_user_details(name="Name not provided", email="not provided"):
    """Record user's name and email when they voluntarily provide it or is related to requesting my resume."""
    push(f"Recording {name} with email {email}")
    return {
        "status": "success",
        "message": "Recorded successfully",
        "data": {}
    }

@function_tool
def tool_record_user_interest_in_chatbots(name="Name not provided", email="not provided"):
    """Record user's name and email when they inquire about help building a chatbot for them"""
    push(f"Recording {name} with email {email} is interested in building a Chatbot for them.")
    return {
        "status": "success",
        "message": "Chatbot inquary successfully",
        "data": {}
    }

@function_tool
def tool_record_unknown_question(question: str, from_user: str):
    """Record work related questions the agent couldn't answer."""
    push(f"Recording unknown question from {from_user}: {question}")
    return {
        "status": "success",
        "message": "Recorded successfully",
        "data": {}
    }

@function_tool
def tool_send_resume(companyName: str = "Guest"):
    """
    Provide a downloadable resume link or payload.
    Optionally include the company name of the requester.
    """
    push(f"Resume sent to {companyName}")
    return {
        "status": "success",
        "message": "Resume sent successfully",
        "data": {
            "link": RESUME_LINK,
            "company": companyName
        }
    }

def build_instructions() -> str:
    base = build_system_prompt()
    extended = validate_prompt_extension(get_prompt() or "")
    return base + "\n\n" + extended

set_tracing_disabled(True)  # avoid OpenAI tracing 401s (not using chatgpt)

ChatbotAgent = Agent(
    name="ChatbotAgent",
    model=LitellmModel("openai/gpt-4o-mini", api_key=os.environ["OPENAI_API_KEY"]),
    instructions=build_instructions(),
    tools=[
        tool_record_user_details,
        tool_record_unknown_question,
        tool_send_resume,
        tool_record_user_interest_in_chatbots,
    ],
    # handoffs=[agent_feedback_reflection] make it async
)
