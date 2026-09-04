from app.db.conn import get_connection


def retrieve(embedding, k_chunks):
    select = "SELECT content FROM documents ORDER BY embedding <=> %s::vector LIMIT %s;"
    data = (embedding, k_chunks)
    context = ""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(select, data)
            data = cur.fetchall()
            context = str([row[0] for row in data])
    return context
