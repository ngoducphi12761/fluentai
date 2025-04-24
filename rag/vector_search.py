# ------------------------------------------------------
# 2. vector_search.py (LangChain v0.3)
# ------------------------------------------------------
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os


# VECTOR_PATH = "../vector_store/index.faiss"

# if not os.path.exists(VECTOR_PATH):
#     from rag.embed_documents import run_embedding
#     run_embedding()

embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")
vector_db = FAISS.load_local("vector_store", embedding_model, allow_dangerous_deserialization=True)

def retrieve_context(query):
    docs = vector_db.similarity_search(query, k=4)
    return "\n".join([doc.page_content for doc in docs])