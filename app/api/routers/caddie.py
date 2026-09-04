from fastapi import APIRouter

from app.api.schemas import *

router = APIRouter(prefix="/caddie", tags=["Caddie"])


@router.post("/chat")
async def check_caddie(req: ChatRequest):
    # caddie_reply = run_caddie_pipeline(ChatRequest.messages)
    caddie_reply = "Caddie: Ok"
    return ChatResponse(conversation_id=str(req.conversation_id), reply=caddie_reply)
