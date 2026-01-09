from agents import Runner, RunConfig
from private_agents.agent_chatbot import ChatbotAgent
from core.classification.work_related import is_work_related
from core.classification.grading import grade
from db.models import save_question

async def run_chatbot(message, session):
    result = await Runner.run(
        starting_agent=ChatbotAgent,
        input=message,
        session=session,
        run_config=RunConfig(tracing_disabled=True),
    )
    return result.final_output or ""

async def grade_if_needed(message):
    print(">>> grade_if_needed called")

    if not is_work_related(message):
        print(">>> not work related")
        return

    result = grade(message)
    print(">>> saving question", result)
    save_question(message, result)