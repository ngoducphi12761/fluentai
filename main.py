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
import json
import utils.action_dispatcher as action_dispatcher
from utils.extract_json import extract_json
from utils.detect_action import is_action_command
from bark import generate_audio

from utils.speak_gtts import speak_gtts

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
        # Debug: Print the context retrieved
        print("[Context]", context)
        # Fallback to general-purpose if context is empty
        # if not context.strip():
        #     # print("No relevant to Fluent Domain.")
        #     # speak("No relevant to Fluent Domain.")
        #     transcribed = f"Answer the following as FluentAi, a voice assistant created by Mr. Bill (Duc Phi Ngo): {transcribed}"
        #     transcribed = clean_text(transcribed)
        #     prompt = transcribed
        # else:
        #     prompt = build_prompt(context, transcribed)
        if context.strip():
    # ✅ Context found
            if is_action_command(transcribed):
                prompt = build_prompt(context, transcribed, mode="action")
                print("[action]: ", prompt)
            else:
                prompt = build_prompt(context, transcribed, mode="question")
                print("[question]: ", prompt)
        else:
            # ✅ No relevant Fluent context found → fallback general polite
            prompt = f"Answer the following naturally as FluentAi: {transcribed}"
            print("[no context found]",prompt)

          # Debug: Print the transcribed input
        # print("[prompt]", prompt)
        llm_response = query_llm(prompt)
        # action_plan = json.loads(llm_response)
        # print("[LLM Response]", llm_response)
        try:
            action_plan = extract_json(llm_response)
            # print("[Action Plan]", action_plan)
            # Proceed to dispatch and execute
            action_dispatcher.execute_action_plan(action_plan)
        
            # if any(phrase in transcribed.lower() for phrase in [
            # "start the automation", "run the automation", "run simulation", 
            # "begin the automation", "launch the solver", "execute simulation", "run the automation",
            # "rerun the automation" , "rerun the simulation"
            # ]):
            #     try:
            #         message = "🚀 Launching Fluent simulation now..."
            #         print(message)
            #         speak_gtts(message)
            #         # audio_array = generate_voice(message)
            #         # play_audio(audio_array)
            #         fluent.run()  # This calls your fluent_automation.py run() function
            #     except Exception as e:
            #         print(f"❌ Failed to run simulation: {e}")
            for action in action_plan:
                if action["action"] == "rerun_simulation":
                    if action["parameters"].get("rerun", False) is True:
                        print("🔁 Rerunning Fluent simulation now...")
                        speak_gtts("Rerunning Fluent simulation now.")
                        fluent.run()
                    elif action["parameters"].get("rerun", False) is False:
                        print("🚀 Launching Fluent simulation now...")
                        speak_gtts("Launching Fluent simulation now")
                        fluent.run()

        except ValueError:
            # If it's a general natural language reply, just print
            # print("[General LLM Response]", llm_response)
            print("[LLM Response]", llm_response)
            speak_gtts(llm_response)
                # ✅ Add Bark to generate human-like voice
            # audio_array = generate_voice(llm_response)
            # play_audio(audio_array)
       
        #Execute the LLM response if it contains Fluent code
        # Trigger execution if matched as a simulation command or Fluent function
        # if "fluent." in llm_response or "fluent.run" in llm_response or any(
        #     phrase in transcribed.lower() for phrase in ["run the tutorial", "run the calculation", "start simulation", 
        #                                                  "start the solver", "run the solver", "start the simulation", 
        #                                                  "run the analysis", "execute the code", "run simulation",
        #                                                  "run the simulaiton", "execute the tutorial", "execute tutorial"]
        # ):
        #     try:
        #         # If LLM didn't generate code, use fallback to run()
        #         if not llm_response.startswith("fluent."):
        #             llm_response = "fluent.run()"
        #         exec("import fluent_automation as fluent\n" + llm_response)
        #     except Exception as e:
        #         print("❌ Execution failed:", e)
        # --- After processing the LLM Response ---


if __name__ == "__main__":
    run_fluent_assistant()
# ------------------------------------------------------
# ✅ Notes:
# - This pipeline follows the diagram: Prompt → Query → Retrieve → Enhance → Generate → Execute
# - Your automation script (fluent_automation.py) is indexed just like documents
# - You can add PDF/Text/Markdown/Notebook files into knowledge/ for enhanced understanding