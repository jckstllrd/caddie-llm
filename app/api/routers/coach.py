from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.api.schemas import *
from app.rag import pipeline

router = APIRouter(prefix="/coach", tags=["Coach"])


@router.post("/chat")
async def coach_chat(req: ChatRequest):
    return StreamingResponse(
        pipeline.run_coach(req.messages[0].content),
        media_type="text/event-stream",
    )
