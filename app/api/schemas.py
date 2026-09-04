from typing import Optional

from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    messages: list[Message]


class ChatResponse(BaseModel):
    conversation_id: str
    reply: str
