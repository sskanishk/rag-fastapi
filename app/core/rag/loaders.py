from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
import os

def load_pdf_documents_from_directory(directory_path: str):
    if not os.path.exists(directory_path):
        raise FileNotFoundError(f"The directory '{directory_path}' does not exist.")
    
    try:
        pdf_loader = DirectoryLoader(path=directory_path, glob='*.pdf', loader_cls=PyPDFLoader)
        loaded_documents = pdf_loader.load()

        if not loaded_documents:
            raise ValueError(f"No PDF documents found in the directory: {directory_path}")
        
        return loaded_documents

    except Exception as error:
        raise RuntimeError(f"An error occurred while loading PDF files: {error}")