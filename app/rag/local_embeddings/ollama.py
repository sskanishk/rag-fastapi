# from langchain_community.embeddings import OllamaEmbeddings
from langchain_ollama import OllamaEmbeddings

MXBAI_EMBED_LARGE = 'mxbai-embed-large'
NOMIC_EMBED_LARGE = 'nomic-embed-text'

def get_ollama_embeddings(model_name: str = MXBAI_EMBED_LARGE):
    return OllamaEmbeddings(model=model_name)
