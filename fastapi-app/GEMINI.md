# FastAPI LLM Chat Interface

This project implements a simple REST API using FastAPI that provides an LLM chat interface with streaming capabilities and session management.

## Project Vision & Mandates

- **Streaming:** The `/chat` endpoint MUST stream LLM responses token-by-token using Server-Sent Events (SSE).
- **Session Management:** Support for chat sessions stored in a database to maintain conversational context.
- **Simplicity:** No authentication/authorization is required for this phase.
- **Quality Assurance:** Every core feature should be accompanied by clear test cases and a testing methodology.

## Tech Stack

- **Framework:** FastAPI
- **Web Server:** Uvicorn
- **LLM SDK:** LangChain (Gemini Model)
- **Validation/Schema:** Pydantic
- **Deployment:** Docker
- **Frontend:** Streamlit

## Architecture

The project follows a layered architecture to ensure maintainability:

1.  **Models (`pydantic`):** Define the schema for chat history (message, timestamp, session_id, sender).
2.  **Routers (`APIRouter`):** Handle HTTP requests, specifically the streaming `/chat` endpoint.
3.  **Service Layer:** Business logic for LLM interaction and streaming response generation.

## Conventions

- **Naming:** Follow standard Python (PEP 8) naming conventions.
- **Documentation:** Maintain up-to-date docstrings for all core functions and endpoints.
- **Testing:** Use `pytest` for unit and integration testing.
