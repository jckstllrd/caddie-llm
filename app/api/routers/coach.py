from fastapi import APIRouter

from app.api.schemas import *
from app.rag import pipeline

router = APIRouter(prefix="/coach", tags=["Coach"])


@router.post("/chat")
async def coach_chat(req: ChatRequest):
    coach_reply = await pipeline.run_caddie(req.messages[0].content)
    return ChatResponse(
        conversation_id=str(req.conversation_id), reply=str(coach_reply)
    )
