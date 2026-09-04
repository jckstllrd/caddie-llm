from openai import OpenAI

from app.config import *


class AIClient:
    def __init__(self):
        self.client = OpenAI(api_key=API_KEY, organization=ORGANISATION_KEY)

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
