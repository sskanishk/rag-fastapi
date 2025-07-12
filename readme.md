# FastApi RAG Application

A minimal RAG backend using Python, FastAPI, and vector similarity search. The application supports user authentication, document ingestion, querying, and response feedback.

## Features

- User registration and login (JWT-based auth)
- Ask questions and get answers based on ingested documents
- Provide feedback on helpfulness of responses
- Ingest documents for RAG
- Choose between Ollama or Hugging Face embedding models
- Built with FastAPI, PostgreSQL, pgvector, and LangChain

---

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd <repo-folder>
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**
   Create a `.env` file in the root directory:

   ```env
   DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/yourdb
   JWT_SECRET=your_jwt_secret
   MODEL_FLOW=ollama  # or hf for Hugging Face
   ```

5. **Run migrations (if using Alembic)**
   ```bash
   alembic upgrade head
   ```

6. **Start the application**
   ```bash
   uvicorn app.main:app --reload
   ```

---

## Embedding Options

You can switch between embedding models by setting the `MODEL_FLOW` in the `.env` file:

Ref: [.env.sample](https://github.com/sskanishk/rag-fastapi/blob/master/.env.sample)

### Ollama
Uses [langchain_ollama](https://python.langchain.com/docs/integrations/text_embedding/ollama/):
```python
from langchain_ollama import OllamaEmbeddings

def get_ollama_embeddings(model_name: str = "mxbai-embed-large"):
    return OllamaEmbeddings(model=model_name)
```

Supported models:
- `mxbai-embed-large`
- `nomic-embed-text`

### Hugging Face
Uses [langchain_huggingface](https://python.langchain.com/docs/integrations/text_embedding/huggingface/):
```python
from langchain_huggingface import HuggingFaceEmbeddings

def get_hf_embedding_model():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-roberta-large-v1")
```

Supported models:
- `sentence-transformers/all-roberta-large-v1` (1024 dims)
- `sentence-transformers/all-MiniLM-L6-v2` (384 dims)

---

## API Endpoints

### Register
```bash
curl --location 'http://127.0.0.1:8000/api/v1/auth/register' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "test2@example.com",
    "password": "exX$ampd1sfgsdfle",
    "name": "asdf"
}'
```

### Login
```bash
curl --location 'http://127.0.0.1:8000/api/v1/auth/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "test2@example.com",
    "password": "exX$ampd1sfgsdfle"
}'
```

### Ask a Question
```bash
curl --location --request GET 'http://localhost:8000/api/v1/ask' \
--header 'accept: application/json' \
--header 'Authorization: Bearer <JWT_TOKEN>' \
--header 'Content-Type: application/json' \
--data '{
    "prompt": "what do you mean by Gen AI?"
}'
```

### Mark Response as Helpful
```bash
curl --location --request GET 'http://localhost:8000/api/v1/mark_response' \
--header 'accept: application/json' \
--header 'Authorization: Bearer <JWT_TOKEN>' \
--header 'Content-Type: application/json' \
--data '{
    "is_helpful": true,
    "id": "28cc8a02-7e74-4af9-882f-3a363bd9580e"
}'
```

### Ingest Documents
```bash
curl --location 'http://localhost:8000/api/v1/ingest' \
--header 'accept: application/json' \
--header 'Authorization: Bearer <JWT_TOKEN>'
```

---

## Notes

- Replace `<JWT_TOKEN>` with the token received from the login API.
- You can switch embedding models using `MODEL_FLOW` = `ollama` or `hf`.
- Ensure PostgreSQL and `pgvector` extension are installed and configured.

---

## Tech Stack

- **Backend**: FastAPI
- **Auth**: JWT
- **Database**: PostgreSQL + pgvector
- **Embeddings**: Ollama / Hugging Face via LangChain
- **Vector Store**: FAISS / pgvector

---

## MIT License

This project is licensed under the MIT License.

