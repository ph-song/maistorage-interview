import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.database.database import create_db_and_tables
from app.chat.routes import router as chat_router
from app.core.settings import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the database and tables on startup
    # (Note: SQLChatMessageHistory handles its own table creation, 
    # but other models still need this)
    await create_db_and_tables()
    yield
    # Clean up on shutdown if needed

app = FastAPI(title="LLM Chatbot with Memory", lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)  

# Include the chat controller
app.include_router(chat_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
