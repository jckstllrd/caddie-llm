from fastapi import APIRouter

from app.api.schemas import *

router = APIRouter(prefix="/coach", tags=["Coach"])


@router.post("/chat")
async def coach_chat(req: ChatRequest):
    # coach_reply = run_coach_pipeline(ChatRequest.messages)
    coach_reply = "Coach: Ok"
    return ChatResponse(conversation_id=str(req.conversation_id), reply=coach_reply)
