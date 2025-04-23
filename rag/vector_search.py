from langchain.vectorstores import FAISS
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
vector_db = FAISS.load_local("../vector_store", embedding_model)

def retrieve_context(query):
    docs = vector_db.similarity_search(query, k=4)
    return "\n".join([doc.page_content for doc in docs])
