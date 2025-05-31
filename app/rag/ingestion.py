import asyncio
import os
from app.core.logging import setup_logging

from app.rag.local_embeddings.ollama import get_ollama_embeddings
from app.db.models.document import Document
from app.db.base import Base
from app.db.session import engine, AsyncSessionFactory
from app.rag.loaders import load_pdf_documents_from_directory
from app.rag.chunking import split_text_into_chunks
from app.rag.vectorstore import store_documents
from app.rag.local_embeddings.huggingface import get_hf_embedding_model

# Initialize logger
logger = setup_logging()

# Constants
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(CURRENT_DIR, "data")


def load_documents_safely(directory_path: str):
    if not os.path.exists(directory_path):
        logger.error(f"Directory does not exist: {directory_path}")
        return []

    try:
        documents = load_pdf_documents_from_directory(directory_path)
        if not documents:
            logger.warning("No PDF documents found in the directory.")
        return documents
    except Exception as e:
        logger.exception(f"Error while loading documents: {e}")
        return []


def chunk_documents_safely(documents):
    try:
        return split_text_into_chunks(documents)
    except Exception as e:
        logger.exception(f"Error while splitting documents into chunks: {e}")
        return []


async def run_ingestion_pipeline(texts, metadatas):
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database schema created or verified.")

        # Use local embedding model (choose only one)
        embedder = get_ollama_embeddings()
        # embedder = get_hf_embedding_model()

        embeddings = embedder.embed_documents(texts)

        async with AsyncSessionFactory() as session:
            await store_documents(session, texts, embeddings, metadatas)

        logger.info("Documents successfully ingested into the vector store.")
        return {"status": "success", "documents": len(texts)}

    except Exception as e:
        logger.exception(f"Document ingestion failed: {e}")
        raise RuntimeError(f"Document ingestion failed: {e}")


async def main():
    documents = load_documents_safely(DATA_DIR)
    if not documents:
        logger.error("No documents to process. Aborting.")
        return

    chunks = chunk_documents_safely(documents)
    if not chunks:
        logger.error("No text chunks generated. Aborting.")
        return

    texts = [chunk.page_content for chunk in chunks if chunk.page_content.strip()]
    metadatas = [chunk.metadata for chunk in chunks]

    logger.info(f"Starting ingestion of {len(texts)} text chunks...")
    result = await run_ingestion_pipeline(texts, metadatas)
    logger.info(f"Ingestion completed: {result}")
    return result

