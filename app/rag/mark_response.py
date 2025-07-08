
from app.db.session import AsyncSessionFactory
from app.rag.vectorstore import mark_chat_response_by_id

async def main(payload: dict) -> dict:
    is_helpful = payload['is_helpful']
    id = payload['id']

    async with AsyncSessionFactory() as session:
        resp = await mark_chat_response_by_id(session, id, is_helpful)

    return resp

    