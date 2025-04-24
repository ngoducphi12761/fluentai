# ------------------------------------------------------
# 1. embed_documents.py (LangChain v0.3 + upgraded embeddings)
# ------------------------------------------------------
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os


def run_embedding():
    # Ensure the vector store directory exists
    loader = DirectoryLoader(
        path="knowledge",
        glob="*.txt",
        loader_cls=TextLoader,
        show_progress=True
    )
    if not os.path.exists("vector_store"):
        os.makedirs("vector_store")
    
    documents = loader.load()
    if not documents:
        raise ValueError("No documents found in the 'knowledge' directory.")

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = splitter.split_documents(documents)

    embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")
    vector_db = FAISS.from_documents(split_docs, embedding_model)
    try:
        vector_db.save_local("vector_store")
        print("Vector database saved successfully.")
    except Exception as e:
        print(f"Error saving vector database: {e}")

run_embedding()