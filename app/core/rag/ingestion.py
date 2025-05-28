import asyncio
import os
from app.core.logging import setup_logging

from app.core.rag.local_embeddings.ollama import get_ollama_embeddings
from app.db.models.document import Document
from app.db.base import Base
from app.db.session import engine, AsyncSessionFactory
from app.core.rag.loaders import load_pdf_documents_from_directory
from app.core.rag.chunking import split_text_into_chunks
from app.core.rag.vectorstore import store_documents
from app.core.rag.local_embeddings.huggingface import get_hf_embedding_model

# Setup logging
logger = setup_logging()

# Setup paths
current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_dir, "data")

def safe_load_documents(directory_path: str):
    if not os.path.exists(directory_path):
        logger.error(f"Directory not found: {directory_path}")
        return []

    try:
        docs = load_pdf_documents_from_directory(directory_path)
        if not docs:
            logger.warning("No documents found.")
        return docs
    except Exception as e:
        logger.exception(f"Failed to load documents: {e}")
        return []


def safe_split_chunks(documents):
    try:
        return split_text_into_chunks(documents)
    except Exception as e:
        logger.exception(f"Failed to split documents into chunks: {e}")
        return []


async def ingest(texts, metadatas):
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database schema ensured.")

        # embedder = get_ollama_embeddings()
        embedder = get_hf_embedding_model()
        embeddings = embedder.embed_documents(texts)

        # Store in DB using vector store logic
        async with AsyncSessionFactory() as session:
            await store_documents(session, texts, embeddings, metadatas)

        logger.info("Data ingestion successful.")
        return {"status": "success", "documents": len(texts)}

    except Exception as e:
        logger.exception(f"Ingestion failed: {e}")
        raise RuntimeError(f"Ingestion failed: {e}")


async def start():
    documents = safe_load_documents(data_dir)
    if not documents:
        logger.error("No documents to ingest. Exiting.")
        return

    text_chunks = safe_split_chunks(documents)
    if not text_chunks:
        logger.error("No text chunks created. Exiting.")
        return

    chunks = [chunk.page_content for chunk in text_chunks if chunk.page_content.strip()]
    metadatas = [chunk.metadata for chunk in text_chunks]
    logger.info(f"Ingesting {len(chunks)} chunks & {len(metadatas)} metadatas...")

    result = await ingest(chunks, metadatas)
    logger.info(f"Ingestion result: {result}")

