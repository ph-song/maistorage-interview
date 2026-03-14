from fastapi import HTTPException


class AIChatException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=500, detail= f"An error occurred while generating the AI response. {detail}")