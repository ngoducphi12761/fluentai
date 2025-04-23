from langchain.document_loaders import TextLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from sentence_transformers import SentenceTransformer
import os

loader = DirectoryLoader(
    "../knowledge",
    glob="*.py",  # Load Python automation script too
    loader_cls=TextLoader,
    show_progress=True
)

documents = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
split_docs = splitter.split_documents(documents)

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
vector_db = FAISS.from_documents(split_docs, embedding_model)
vector_db.save_local("../vector_store")