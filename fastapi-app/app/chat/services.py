from typing import AsyncGenerator, Any
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from fastapi import HTTPException
from langchain.chat_models import init_chat_model
from app.core.settings import settings
from app.database.database import engine
from app.chat.exceptions import AIChatException
from app.core.logger import logger 

# --- Configuration & Initialization ---
# Initialize the chat model using init_chat_model
chat_model = init_chat_model(
    model=settings.LANGUAGE_MODEL_TYPE,
    model_provider=settings.LANGUAGE_MODEL_PROVIDER,
    google_api_key=settings.LANGUAGE_MODEL_API_KEY,
    temperature=0.7,
)

# 1. Define the Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful and friendly AI assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])

# 2. Build the full chain
chain = prompt | chat_model

# --- Memory Setup ---
def get_session_history(session_id: str):
    """Factory function for SQL-based session history."""
    return SQLChatMessageHistory(
        session_id=session_id,
        connection= engine,
        async_mode=True,  # Use async mode for the history
    )

# 3. Wrap the model with history capability
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

class ChatService:
    @staticmethod
    async def generate_response(session_id: str, message: str) -> AsyncGenerator[str, None]:
        """
        Generates and streams LLM response token-by-token with a structured prompt template and history.
        """
        input = {"input": message}
        config = {"configurable": {"session_id": session_id}}
        try:
            response_stream = chain_with_history.astream(input, config=config)
            async for chunk in response_stream:
                content = ChatService.get_chunk_text(chunk)
                if content:
                    yield content
        except Exception as e:
            logger.error(f"Error generating AI content: {e}", exc_info=True)
            raise AIChatException(str(e))

    @staticmethod
    def get_chunk_text(chunk: Any) -> str:
        """
        Standardizes the extraction of text from LangChain stream chunks.
        Handles BaseMessages, objects with content attributes, and raw strings.
        """
        if isinstance(chunk, BaseMessage):
            # Handle cases where content is a list (e.g., multi-modal)
            if isinstance(chunk.content, list):
                return "".join([str(item.get("text", "")) for item in chunk.content if isinstance(item, dict)])
            return str(chunk.content)
        
        if hasattr(chunk, "content"):
            return str(chunk.content)
        
        if isinstance(chunk, str):
            return chunk
            
        return str(chunk) if chunk is not None else ""