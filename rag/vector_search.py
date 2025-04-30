# ------------------------------------------------------
# 2. vector_search.py (LangChain v0.3)
# ------------------------------------------------------
import json
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os


# VECTOR_PATH = "../vector_store/index.faiss"

# if not os.path.exists(VECTOR_PATH):
#     from rag.embed_documents import run_embedding
#     run_embedding()

embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")
vector_db = FAISS.load_local("vector_store", embedding_model, allow_dangerous_deserialization=True)

# Export documents and metadata
docs = vector_db.docstore._dict  # access internal document store

export_data = []
for doc_id, doc in docs.items():
    export_data.append({
        "id": doc_id,
        "content": doc.page_content,
        "metadata": doc.metadata
    })
# Save to JSON
with open("vector_store/vector_store_export.json", "w", encoding="utf-8") as f:
    json.dump(export_data, f, indent=2, ensure_ascii=False)

print("✅ vector_store_export.json saved.")

def retrieve_context(query):
    docs = vector_db.similarity_search(query, k=4)
    string = "\n".join([doc.page_content for doc in docs])
    return string