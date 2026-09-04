from fastapi import APIRouter

from app.api.schemas import *

router = APIRouter(prefix="/caddie", tags=["Caddie"])


@router.post("/chat")
async def check_caddie(req: ChatRequest):
    # caddie_reply = run_caddie_pipeline(ChatRequest.messages)
    caddie_reply = ChatResponse(conversation_id="None", reply="Caddie: Ok")
    return caddie_reply
