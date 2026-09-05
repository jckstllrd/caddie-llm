from app.ai.client import AIClient
from app.db.embedding import retrieve
from app.rag.prompts import CADDIE_SYSTEM_PROMPT, COACH_SYSTEM_PROMPT

client = AIClient()


def retrieve_context(message):

    embedding = client.create_embedding(message)

    context = retrieve(embedding, 5)

    print(context)
    return context


async def run_caddie(message):
    context_str = retrieve_context(message)

    final_user_content = f"""{context_str}\n\nBased on the Golf context above, anwswer the following question, [DO NOT REFERENCE YOU HAVE BEEN GIVEN THE GOLF CONTEXT]:

    User Question: {message}"""

    async for token in client.stream_text(CADDIE_SYSTEM_PROMPT, final_user_content):
        yield f"data: {token}\n\n"


async def run_coach(message):
    async for token in client.stream_text(COACH_SYSTEM_PROMPT, message):
        yield f"data: {token}\n\n"
