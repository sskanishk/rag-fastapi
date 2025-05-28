import aiohttp
import asyncio
import json
from typing import Dict, List
from app.core.rag.vectorstore import retrieve_relevant_context
from app.core.rag.local_embeddings.ollama import get_ollama_embeddings
from app.db.session import AsyncSessionFactory
from app.core.config import settings

HF_API_URL = f"https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
HEADERS = {
    "Authorization": f"Bearer {settings.HF_TOKEN}"
}

PROMPT_TEMPLATE = """
### Instruction:
Answer the question using ONLY the context below. Follow these rules:
1. Be factual and concise
2. If answer isn't in context, say "I don't have that information"
3. Never invent details

### Context:
{context}

### Question:
{question}

### Response:
"""


async def find_similar_embeddings(query_embedding: list) -> list:
    async with AsyncSessionFactory() as session:
        return await retrieve_relevant_context(
            session=session,
            query_embedding=query_embedding,
            similarity_threshold=0.5,
            top_k=3
        )


def format_context(docs: list) -> str:
    return "\n\n".join(
        f"DOCUMENT {i+1} (Similarity: {doc.get('similarity', 0):.2f}):\n{doc['content']}\n" 
        for i, doc in enumerate(docs)
    )


async def query_hf_api(payload: dict) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            HF_API_URL, 
            headers=HEADERS, 
            json=payload,
            timeout=30
        ) as response:
            if response.status != 200:
                error = await response.text()
                raise Exception(f"HF API error {response.status}: {error}")
                
            result = await response.json()
            return result[0]['generated_text']


async def questionanswer(prompt_data: dict) -> dict:
    question = prompt_data['prompt'][0]
    
    # Create embeddings
    embedder = get_ollama_embeddings()
    embeddings = embedder.embed_query(question)
    
    # Retrieve context
    context_docs = await find_similar_embeddings(embeddings)
    if not context_docs:
        return {"answer": "No relevant context found", "sources": []}
    
    # Prepare prompt
    context_str = format_context(context_docs)
    prompt = PROMPT_TEMPLATE.format(context=context_str, question=question)
    
    # Generate response
    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.3,
            "max_new_tokens": 1024,
            "return_full_text": False
        }
    }
    
    try:
        response = await query_hf_api(payload)
        return {
            "answer": response.strip(),
            "sources": [doc["metadata"] for doc in context_docs]
        }
    except Exception as e:
        return {
            "answer": f"Error generating response: {str(e)}",
            "sources": []
        }