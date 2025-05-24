from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.document import Document

async def store_documents(session: AsyncSession, texts: list[str], embeddings: list[list[float]]):
    if len(texts) != len(embeddings):
        raise ValueError("Texts and embeddings length mismatch")

    try:
        for text, embedding in zip(texts, embeddings):
            doc = Document(content=text, embedding=embedding)
            session.add(doc)
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise RuntimeError("Failed to store documents") from e
