from fastapi import APIRouter
from fastapi.responses import StreamingResponse

import app.rag.pipeline as pipeline
from app.api.schemas import *

router = APIRouter(prefix="/caddie", tags=["Caddie"])


@router.post("/chat")
async def check_caddie(req: ChatRequest):
    return StreamingResponse(
        pipeline.run_coach(req.messages[0].content), media_type="text/event-stream"
    )
