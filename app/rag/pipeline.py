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

    # create embedding of message content

    # retrieve / index content from the database

    # create the augmented input context

    # generate model response
    context_str = retrieve_context(message)

    final_user_content = f"""{context_str}\n\nBased on the Golf context above, anwswer the following question:

    User Question: {message}"""

    response = client.generate_text(CADDIE_SYSTEM_PROMPT, final_user_content)

    print("were good to go")
    # return model response
    return response


async def run_coach(message):
    response = client.generate_text(COACH_SYSTEM_PROMPT, message)
    return response
