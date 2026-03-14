# maistorage-interview

A technical assessment project for the **MAIStorage** interview process, featuring a containerized LLM-powered application built with LangChain.

---

## Quick Start

### Prerequisites
Ensure you have the following installed on your local machine:
* **Docker**
* **Docker Compose**

### 1. Environment Configuration
Create a `.env` file in `fastapi-app/` directory and configure the following variables. 

| Variable | Description | Default |
| :--- | :--- | :--- |
| `LANGUAGE_MODEL_API_KEY` | **(Mandatory)** Your API key for the LLM provider. | — |
| `LANGUAGE_MODEL_PROVIDER` | The LangChain `init_chat_model()` provider. | `google_genai` |
| `LANGUAGE_MODEL_TYPE` | The specific model version/type. | `gemini-2.5-flash` |
| `SECRET_KEY` | Key used for security/session signing. | `supersecretkey` |

**Example `.env` file:**
```bash
# Required
LANGUAGE_MODEL_API_KEY=your_api_key_here

# Optional (Defaults shown)
LANGUAGE_MODEL_PROVIDER=google_genai
LANGUAGE_MODEL_TYPE=gemini-2.5-flash
SECRET_KEY=supersecretkey