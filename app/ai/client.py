from openai import AsyncOpenAI, OpenAI
from openai.types.responses import ResponseTextDeltaEvent

from app.config import *


class AIClient:
    def __init__(self):
        self.client = OpenAI(api_key=API_KEY, organization=ORGANISATION_KEY)
        self.async_client = AsyncOpenAI(
            api_key=API_KEY, organization=ORGANISATION_KEY
        )

    def generate_text(self, instructions, content, model="gpt-4.1"):
        response = self.client.responses.create(
            model=model,
            input=[
                {"role": "developer", "content": instructions},
                {"role": "user", "content": content},
            ],
        )
        output_text = response.output_text
        return output_text

    def create_embedding(self, message):
        response = self.client.embeddings.create(
            model="text-embedding-3-small", input=message
        )
        embedding = str(response.data[0].embedding)
        return embedding

    async def stream_text(self, instructions, content, model="gpt-4.1"):
        stream = await self.async_client.responses.create(
            model=model,
            input=[
                {"role": "developer", "content": instructions},
                {"role": "user", "content": content},
            ],
            stream=True,
        )
        async for event in stream:
            if event.type == "response.output_text.delta":
                output_token = event.delta
                yield output_token
