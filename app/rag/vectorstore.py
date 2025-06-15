from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.document import Document
from app.db.models.chat import Chat
from typing import Optional, List
from sqlalchemy import select, Float, cast, text
from sqlalchemy.sql.expression import func
from pgvector.sqlalchemy import Vector

async def store_documents(
        session: AsyncSession, 
        texts: list[str], 
        embeddings: list[list[float]], 
        metadatas: Optional[list[dict]] = None
    ):
    if len(texts) != len(embeddings):
        raise ValueError("Texts and embeddings length mismatch")
    
    if metadatas is not None and len(metadatas) != len(texts):
        raise ValueError("Metadata list length must match texts and embeddings")

    try:
        for i, (text, embedding) in enumerate(zip(texts, embeddings)):
            metadata = metadatas[i] if metadatas else None
            doc = Document(content=text, embedding=embedding, metadata=metadata)
            session.add(doc)
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise RuntimeError("Failed to store documents") from e
    

async def store_chats(
        session: AsyncSession, 
        question: str, 
        question_embedding: list[float], 
        response: str, 
        response_embedding: list[float],
        created_by: str
    ):
    if len(question) == 0:
        raise ValueError("Invalid question")

    try:
        chat = Chat(question=question, question_embedding=question_embedding, response=response, response_embedding=response_embedding, created_by=created_by)
        session.add(chat)        
        await session.commit()
    except Exception as e:
        print("store chat ", e)
        await session.rollback()
        raise RuntimeError("Failed to store chats") from e


async def retrieve_relevant_context_old(
    session: AsyncSession,
    query_embedding: List[float],
    similarity_threshold: float = 0.7,
    top_k: int = 5,
    metadata_filter: Optional[dict] = None
) -> List[dict]:
    try:
        # Base query
        # print("query_embedding>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", query_embedding)
        query = select(
            Document.content,
            Document.metadata,
            func.cosine_similarity(Document.embedding, query_embedding).label("similarity")
        ).where(
            func.cosine_similarity(Document.embedding, query_embedding) > similarity_threshold
        ).order_by(
            func.cosine_similarity(Document.embedding, query_embedding).desc()
        ).limit(top_k)

        print("query =>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>...", query)

        # Add metadata filters if provided
        if metadata_filter:
            for key, value in metadata_filter.items():
                query = query.where(Document.metadata[key].astext == str(value))

        # Execute query
        result = await session.execute(query)
        documents = result.fetchall()

        print("Heree =>>>>>>>>>>>>>>>>>>>> ")

        # Format results
        return [{
            "content": doc.content,
            "metadata": doc.metadata,
            "similarity": doc.similarity
        } for doc in documents]

    except Exception as e:
        raise RuntimeError(f"Failed to retrieve documents: {str(e)}") from e


async def retrieve_relevant_context(
        session: AsyncSession, 
        query_embedding: list[float], 
        similarity_threshold: float = 0.75, 
        top_k: int = 3
    ):
    # Convert to PostgreSQL vector format
    pg_vector = "[" + ",".join(map(str, query_embedding)) + "]"

    stmt = text("""
        SELECT content, metadata, 1 - (embedding <=> :embedding) as similarity
        FROM documents
        WHERE 1 - (embedding <=> :embedding) > :threshold
        ORDER BY embedding <=> :embedding
        LIMIT :limit
    """)
    
    result = await session.execute(
        stmt,
        {
            "embedding": pg_vector,
            "threshold": similarity_threshold,
            "limit": top_k
        }
    )
    return result.mappings().all()


async def retrieve_relevant_context_from_cache(
        session: AsyncSession, 
        question_embedding: list[float], 
        similarity_threshold: float = 0.75, 
        top_k: int = 3
    ):
    # Convert to PostgreSQL vector format
    pg_vector = "[" + ",".join(map(str, question_embedding)) + "]"

    print("pg_vector ====> ", pg_vector)

    stmt = text("""
        SELECT question, response, 1 - (question_embedding <=> :embedding) as similarity
        FROM chats
        WHERE 1 - (question_embedding <=> :embedding) > :threshold
        ORDER BY question_embedding <=> :embedding
        LIMIT :limit
    """)
    
    result = await session.execute(
        stmt,
        {
            "embedding": pg_vector,
            "threshold": similarity_threshold,
            "limit": top_k
        }
    )
    return result.mappings().all()

