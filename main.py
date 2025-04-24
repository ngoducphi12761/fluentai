# === RAG + LLM Enhanced Architecture for FluentAi (Latest LangChain & LLM) ===
# ------------------------------------------------------
# 📁 Project Structure 
# ------------------------------------------------------
# FluentAi/
# ├── main.py                  # Main CLI/voice app loop
# ├── fluent_automation.py     # All Fluent meshing/solver/post logic
# ├── rag/
# │   ├── embed_documents.py   # Step 1: Preprocess docs and build vector DB
# │   ├── vector_search.py     # Step 2: Query vector DB for relevant context
# │   ├── prompt_template.py   # Step 3: Build prompt using enhanced context + user query
# │   └── llm_gateway.py       # Step 4: Call LLM and return response
# ├── knowledge/               # Fluent docs, code, PDFs, Markdown, etc.
# └── vector_store/            # FAISS/Chroma vector DB output

# Mr. Bill — Duc Phi Ngo is architecting and developing this project. 

from rag.embed_documents import run_embedding
from rag.vector_search import retrieve_context
from rag.prompt_template import build_prompt
from rag.llm_gateway import query_llm
import fluent_automation as fluent
import unicodedata

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def clean_text(text):
    return unicodedata.normalize('NFKD', text).encode('utf-8', 'ignore').decode('utf-8')

def run_fluent_assistant():
    
    while True:
        transcribed = input("Ask anything about Fluent: ")
        
        if any(word in transcribed.lower() for word in ["exit", "quit", "shutdown"]):
            break
        transcribed = clean_text(transcribed)
        context = retrieve_context(transcribed)
        # Fallback to general-purpose if context is empty
        if not context.strip():
            # print("No relevant to Fluent Domain.")
            # speak("No relevant to Fluent Domain.")
            transcribed = f"Answer the following as FluentAi, a voice assistant created by Mr. Bill (Duc Phi Ngo): {transcribed}"
            transcribed = clean_text(transcribed)
            prompt = transcribed
        else:
            prompt = build_prompt(context, transcribed)

          # Debug: Print the transcribed input
        print("[prompt]", prompt)
        llm_response = query_llm(prompt)
        print("[LLM Response]", llm_response)
        #Execute the LLM response if it contains Fluent code
        if "fluent." in llm_response or "fluent.run" in llm_response:
            try:
                exec("import fluent_automation as fluent\n" + llm_response)
            except Exception as e:
                print("Execution failed:", e)

if __name__ == "__main__":
    run_fluent_assistant()
# ------------------------------------------------------
# ✅ Notes:
# - This pipeline follows the diagram: Prompt → Query → Retrieve → Enhance → Generate → Execute
# - Your automation script (fluent_automation.py) is indexed just like documents
# - You can add PDF/Text/Markdown/Notebook files into knowledge/ for enhanced understanding