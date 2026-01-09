⚡ This chatbot is more than just Q&A — it’s a **personal brand ambassador** designed to represent Hristo Botev as a software engineer, while remaining modular, extensible, and cost-aware.

It answers career-related questions, shares resume information, captures user feedback, logs unknown questions, sends push notifications, and is structured for future self-improvement — with guardrails to ensure professional and relevant interactions only.

🌐 **Live demo**  
https://hristo.botevllc.com

---

## ✨ Key Features

### 🧑 Persona-based responses

- Speaks in the first person as **Hristo Botev**
- Focused strictly on software engineering, career, and project-related topics
- Politely refuses irrelevant or out-of-scope requests

---

### 📄 Resume integration

- Summarizes background from `resume_summary.txt`
- Can share a **downloadable resume link**
- ⚠️ **PDF parsing has been intentionally removed** to reduce complexity and cost

---

### 🏗️ Modular prompt & instruction system

Behavior is defined through **multiple focused instruction files**, allowing changes without touching application code:

- `identity`
- `style`
- `behavior_constraints`
- `work_experience`
- `impact_examples`
- `resume_summary`
- `tools`
- `feedback_handoff`
- `feedback_reflect`

This structure supports controlled evolution while maintaining predictable behavior.

---

### 📝 Feedback handling (cost-aware)

- User feedback is still **captured and stored**
- Reflection and prompt self-mutation are **temporarily disabled**
- This was a deliberate decision to limit LLM costs
- The feedback loop will be **refactored and re-enabled** in a more efficient form

---

### 🧠 Question classification (lightweight)

- Removed synchronous **GraderAgent**
- Replaced with a **fast keyword-based work relevance check**
- Enables:
  - Immediate filtering
  - Optional **asynchronous grading** in the future
- Keeps the main interaction path fast and inexpensive

---

### 🛠️ Custom tools

The following tools remain unchanged:

- `tool_save_feedback` → log user feedback
- `tool_send_resume` → send a resume download link
- `tool_record_user_details` → capture email / company
- `tool_record_unknown_question` → log unanswered questions
- `tool_record_user_interest_in_chatbots` → track product interest

---

### 📬 Professional handoff

- Politely directs interested users to email contact
- Requests email/company before sending resume
- Encourages feedback at the end of conversations

📧 **Contact**: hristo.s.botev@gmail.com

---

### ⚖️ Guardrails

- Responds **only** to software-engineering-related topics
- Declines unrelated roles or requests
- Ignores malicious or manipulative feedback
- Does not self-modify behavior based on hostile input

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone git@github.com:YOUR_HANDLE/chatbot-project.git
cd chatbot-project
```

### 2. Setup environment

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Environment variables

Create a .env file:

```bash
OPENAI_API_KEY=sk-proj-1234
PUSHOVER_TOKEN=IfYouWantToUsePushover
PUSHOVER_USER=IfYouWantToUsePushover
AGENTS_DB_PATH=agents_sessions.db
DATABASE_URL=sqlite:///data/app.db
```

###4. Run with Docker

```bash
docker-compose up --build
```

Then open http://localhost:5005/

🧩 Agents Overview

ChatbotAgent → main user-facing agent.
ReflectOnFeedbackAgent → captures feedback & refines prompts.

📈 Roadmap

Full calendar integration for scheduling
Upload job descriptions for automated fit assessment
Analytics & insights dashboard
Multi-persona support
Frontend chat widget for websites

📬 Contact

📧 hristo.s.botev@gmail.com
🌐 https://hristo.botevllc.com
