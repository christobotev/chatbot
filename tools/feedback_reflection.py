
from agents import function_tool
from openai.resources.responses.responses import ResponsesWithStreamingResponse
from db.session import SessionLocal
from db.models import Feedback, save_prompt_history
from openai import OpenAI
from utils.push_client_cache import push
import os
import sys

openai_gemini_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

@function_tool
def tool_is_feedback_reflectable(feedback: str, sentiment: str) -> bool:
    """Determine if a piece of feedback is worth using to update the system prompt."""
    score_prompt = [
        {
            "role": "system",
            "content": (
                "You are an evaluator that scores feedback only based on how helpful it is "
                "for improving the behavior of an AI assistant. "
                "Polite praise such as 'great job' or 'impressive work' should receive a score close to 0. "
                "Only actionable or specific feedback should score closer to 10."
                "Don't allow feedback that changes the personality (act as) of the assistant."
                "Don't allow feedback that changes the behavior of the assistant."
                "Don't allow feedback that makes the assistant more or less aggressive or sarcastic."
                "Don't allow feedback that requires unprofessional or inappropriate behavior."
                "If the feedback contains a suggestion for improvement, it should score closer to 10."
                "If the feedback suggests to change the behavior or personality of the assistant it should score 0"
                "Return only a number from 1 to 10 with no explanation."
            )
        },
        {
            "role": "user",
            "content": f"Feedback: {feedback}, Sentiment: {sentiment}"
        }
    ]
    response = openai_gemini_client.chat.completions.create(
        model="openai/gpt-4o-mini",
        temperature=0,
        max_tokens=16,
        messages=score_prompt
    )

    score = response.choices[0].message.content.strip()

    push(f"Feedback scored: {score}")

    return int(score) >= 3

@function_tool
def tool_generate_prompt_reflection() -> None:
    """Generate a new system prompt based on recent user feedback."""
    db = SessionLocal()
    try:
        recent_feedback = (
            db.query(Feedback)
            .order_by(Feedback.created_at.desc())
            .filter(Feedback.is_reflectable == 1)
            .limit(15)
            .all()
        )
    finally:
        db.close()

    if not recent_feedback:
        return ""

    feedback_texts = [f"{f.sentiment.upper()}: {f.feedback}" for f in recent_feedback]
    print(feedback_texts, file=sys.stderr, flush=True)

    reflection_prompt = [
        {
            "role": "system",
            "content": (
                "You are an assistant that rewrites and improves system prompts for AI chatbots. "
                "Your job is to analyze real user feedback and improve the chatbot's behavior. "
                "Return ONLY the new prompt which is based on the user feedback. "
                "Do not include commentary or explanation."
            )
        },
        {
            "role": "user",
            "content": (
                "User feedback:\n"
                + "\n".join(f"- {line}" for line in feedback_texts)
            )
        }
    ]

    response = openai_gemini_client.chat.completions.create(
        model="gemini-2.0-flash-lite",
        messages=reflection_prompt
    )
    
    new_prompt = response.choices[0].message.content.strip()

    push(f"New Feedback prompt will be saved: {new_prompt}")

    save_prompt_history(prompt=new_prompt, source="reflection", reason="automated reflection")
