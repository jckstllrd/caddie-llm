from fastapi import APIRouter

import app.rag.pipeline as pipeline
from app.api.schemas import *

router = APIRouter(prefix="/caddie", tags=["Caddie"])


@router.post("/chat")
async def check_caddie(req: ChatRequest):
    caddie_reply = await pipeline.run_caddie(req.messages[0].content)
    return ChatResponse(
        conversation_id=str(req.conversation_id), reply=str(caddie_reply)
    )
