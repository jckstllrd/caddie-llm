import os

import numpy as np
import psycopg as pg
import spacy
from dotenv import load_dotenv
from openai import OpenAI
from psycopg import connection
from pypdf import PdfReader

load_dotenv()
PSQL_CONNECTION_STRING = os.getenv("PSQL_CONNECTION_STRING")
client = OpenAI()


def get_connection():
    return pg.connect(str(PSQL_CONNECTION_STRING))


def add_embeddings_to_db(chunks, embeddings):
    insert_query = """INSERT INTO documents (content, embedding) VALUES (%s, %s) RETURNING id, content;"""

    conn = get_connection()
    print(len(chunks))
    for i in range(len(chunks)):
        data = (chunks[i], embeddings[i])
        try:
            print("trying")
            print(conn)
            with conn.cursor() as cur:
                print(cur)
                cur.execute(insert_query, data)
                data = cur.fetchone()
                print("Message ID for latest entry: ", data)

        except (pg.DatabaseError, Exception) as error:
            print(error)
    conn.commit()


def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


def load_rag_documents():
    reader = PdfReader("./data/2023-Rules-Of-Golf.pdf")
    nlp = spacy.load("en_core_web_sm")

    full_text = ""
    print("here")
    for page in reader.pages:
        full_text += page.extract_text()
    doc = nlp(full_text)
    sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
    chunks = []
    current_chunk_sentences = [sentences[0]]
    print(len(sentences))
    BATCH = 500
    sentence_embeddings = []
    for i in range(0, len(sentences), BATCH):
        batch = sentences[i : i + BATCH]
        responses = client.embeddings.create(
            model="text-embedding-3-small", input=batch
        )
        batch_embeddings = [data.embedding for data in responses.data]

        sentence_embeddings.extend(batch_embeddings)
    MIN_THRESHOLD = 0.6
    for i in range(len(sentences) - 1):
        cmp = cosine_similarity(sentence_embeddings[i], sentence_embeddings[i + 1])
        if cmp > MIN_THRESHOLD:
            chunks.append(" ".join(current_chunk_sentences))
            current_chunk_sentences = [sentences[i + 1]]
        else:
            current_chunk_sentences.append(sentences[i + 1])

    if current_chunk_sentences:
        chunks.append(" ".join(current_chunk_sentences))

    responses = client.embeddings.create(model="text-embedding-3-small", input=chunks)

    final_embeddings = [data.embedding for data in responses.data]
    add_embeddings_to_db(chunks, final_embeddings)


if __name__ == "__main__":
    load_rag_documents()
