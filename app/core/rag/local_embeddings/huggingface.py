from langchain_huggingface import HuggingFaceEmbeddings

ST_1024_DIM = "sentence-transformers/all-roberta-large-v1"
ST_384_DIM = "sentence-transformers/all-MiniLM-L6-v2"

def get_hf_embedding_model():
    embedding_model=HuggingFaceEmbeddings(model_name=ST_1024_DIM)
    return embedding_model