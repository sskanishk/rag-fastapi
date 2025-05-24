from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_text_into_chunks(document_list, chunk_size: int = 500, chunk_overlap: int = 50):
    if not isinstance(document_list, list):
        raise TypeError("Expected document_list to be of type list.")

    if chunk_size <= 0 or chunk_overlap < 0:
        raise ValueError("chunk_size must be > 0 and chunk_overlap must be >= 0.")

    try:
        character_text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap)
        chunked_documents = character_text_splitter.split_documents(document_list)
        return chunked_documents

    except Exception as error:
        raise RuntimeError(f"An error occurred while splitting text into chunks: {error}")
