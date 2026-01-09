import os
from dotenv import load_dotenv

load_dotenv(override=True)

from db import models #import models before creating tables
from db.session import Base, engine
Base.metadata.create_all(bind=engine)

# Import things that query the DB
import gradio as gr
from agents import SQLiteSession
from orchestration.chat_flow import run_chatbot, grade_if_needed

DB_PATH = os.getenv("AGENTS_DB_PATH", "/data/agents_sessions.db")

class Me:
    def __init__(self):
        self.db_path = DB_PATH
        self.sessions = {}

    def get_session(self, request: gr.Request):
        sid = getattr(request, "session_hash", "anon")
        if sid not in self.sessions:
            self.sessions[sid] = SQLiteSession(session_id=sid, db_path=self.db_path)
        return self.sessions[sid]

    async def chat(self, message, history, request):
        session = self.get_session(request)

        response = await run_chatbot(message, session)

        try:
            await grade_if_needed(message)
        except Exception as e:
            print(f"⚠️ grading failed: {e}")

        return response

me = Me()

if __name__ == "__main__":
    gr.ChatInterface(fn=me.chat).launch(server_name="0.0.0.0", server_port=5005)
