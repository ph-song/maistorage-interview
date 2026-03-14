import uuid
from typing import AsyncGenerator
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
from app.chat.services import ChatService
from app.core.settings import settings
from langchain_core.exceptions import LangChainException
from sse_starlette.sse import EventSourceResponse
from app.core.logger import logger
import json

router = APIRouter()

@router.post("/chat")
async def chat_endpoint(message: str, request: Request):
    """
    Main endpoint for the chatbot. Uses session management to identify chat history.
    Streams the LLM response token-by-token.
    """
    # 1. Get or create session_id from the signed cookie
    session_id = request.session.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
        request.session["session_id"] = session_id

    # 2. Define the generator for streaming
    async def event_generator() -> AsyncGenerator[dict, None]: # Changed return type hint to dict
        yield {"event": "metadata", "data": json.dumps({"session_id": session_id})}

        try:
            # 3. Use ChatService to stream the response
            async for token in ChatService.generate_response(session_id, message):
                yield {"event": "message", "data": json.dumps({"text": f"{token}"})} # Added event: message
        except Exception as e:
            logger.error(f"Error in chat endpoint: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=str(e))
        
    return EventSourceResponse(event_generator(), media_type="text/event-stream")

