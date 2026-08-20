import os

from dotenv import load_dotenv
from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel
from pypdf import PdfReader

from caddie_llm.scripts.ingest_data import get_connection


class Message(BaseModel):
    conversationId: int
    messageContent: str


app = FastAPI()
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
ORGANISATION_KEY = os.getenv("OPENAI_ORGANISATION_ID")
client = OpenAI(api_key=API_KEY, organization=ORGANISATION_KEY)


def rag(query):
    response = client.embeddings.create(model="text-embedding-3-small", input=query)
    embedding = str(response.data[0].embedding)
    select_query = (
        "SELECT content FROM documents ORDER BY embedding <=> %s::vector LIMIT %s;"
    )
    data = (embedding, 5)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(select_query, data)
            data = cur.fetchall()
            retrieved_chunks = [row[0] for row in data]
    print(retrieved_chunks)


async def call_ai(message):
    response = client.responses.create(
        model="gpt-4.1-nano",
        instructions="You are a golf rules expert, you use your full context to answer queries about golfing rules using the full extent of the rule book. You answer questions in this general format - Quote the related Rule, answer their question, summarise ways they could win by abusing golfing rules.",
        input=message,
    )
    return response.output_text


@app.post("/")
async def send_message(req: Message):
    rag(req.messageContent)
    res = await call_ai(req.messageContent)
    return res


@app.get("/")
def say_hello():
    res = {"conversationId": 0, "content": "Hello World!"}
    return res
