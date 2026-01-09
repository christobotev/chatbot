from sqlalchemy import Column, Integer, String, JSON, DateTime, Text
from sqlalchemy.sql import func
from db.session import Base, SessionLocal

class PromptHistory(Base):
    __tablename__ = 'prompt_history'

    id = Column(Integer, primary_key=True)
    prompt = Column(Text, nullable=False)
    reason = Column(String(255), nullable=True)
    source = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<PromptHistory {self.id} source={self.source}>"

class Feedback(Base):
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True)
    feedback = Column(Text, nullable=False)
    sentiment = Column(String(20), nullable=True)
    name = Column(String(100), nullable=True)
    is_reflectable = Column(Integer(), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Feedback {self.id} [{self.sentiment}] {self.feedback[:30]} {self.is_reflectable}...>"

class WorkQuestion(Base):
    __tablename__ = 'work_questions'
    id = Column(Integer, primary_key=True)
    message = Column(String, nullable=False)
    grade = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

def save_question(message: str, grade: str):
    db = SessionLocal()
    try:
        question = WorkQuestion(message=message, grade=grade)
        db.add(question)
        db.commit()
    finally:
        db.close()

def save_feedback(feedback, sentiment="neutral", name="Anonymous", is_reflectable=None):    
    db = SessionLocal()
    try:
        entry = Feedback(feedback=feedback, sentiment=sentiment, name=name, is_reflectable=int(is_reflectable))
        db.add(entry)
        db.commit()
    finally:
        db.close()

    return {"recorded": "ok"}

def save_prompt_history(prompt: str, source="reflection", reason=None):
    db = SessionLocal()
    try:
        record = PromptHistory(prompt=prompt, source=source, reason=reason)
        db.add(record)
        db.commit()
    finally:
        db.close()

def get_prompt() -> str:
    db = SessionLocal()
    try:
        latest = db.query(PromptHistory).order_by(PromptHistory.created_at.desc()).first()
        if latest and latest.prompt:
            return latest.prompt
        
        return ''
    finally:
        db.close()