import subprocess
import os
import shutil

def clear_vector_store(directory="vector_store"):
    if os.path.exists(directory):
        shutil.rmtree(directory)
        print(f"✅ All contents in '{directory}' have been deleted.")
    else:
        print(f"⚠️ Directory '{directory}' does not exist.")

def run_embedding():
    print("🔁 Running document embedding...")
    try:
        subprocess.run(["py", "./rag/embed_documents.py"], check=True)
        print("✅ Vector store generated.\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during embedding: {e}")

def run_main_assistant():
    print("🚀 Launching Fluent Assistant...")
    try:
        subprocess.run(["py", "main.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Fluent Assistant: {e}")

if __name__ == "__main__":
    clear_vector_store()

    # Re-run embed only if vector store was deleted or missing
    if not os.path.exists("vector_store/index.faiss"):
        run_embedding()
    else:
        print("🧠 Vector store already exists — skipping embedding.\n")

    run_main_assistant()
