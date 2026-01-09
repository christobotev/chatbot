# Changelog

## [Unreleased]

- Planning calendar / scheduling integration
- Refactoring feedback reflection to reduce LLM cost
- UI theming improvements

---

## [0.2.0] – 2026-01

### Changed

- Reworked instruction system into multiple focused prompt files
- Replaced GraderAgent with lightweight keyword-based relevance checks
- Moved from Google API keys to OpenAI API only
- Changed default port from 5002 → 5005

### Removed

- PDF resume parsing and extraction
- Synchronous question grading
- Automated feedback-driven prompt mutation (temporarily)
- Gradio theme (UI will be revisited later)

### Notes

These changes were made intentionally to:

- Reduce LLM usage and cost
- Improve maintainability
- Make future async processing easier to introduce

---

## [0.1.0] – Initial Release

### Added

- Persona-based chatbot
- Resume sharing and career Q&A
- Feedback capture and reflection
- Custom tools for logging, notifications, and contact capture
