import subprocess
import pyttsx3
from faster_whisper import WhisperModel

# --1. TTS setup--
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# --2. STT setup--

# Load the model (small)
model = WhisperModel("small",  device="cpu")

# Transcribe from file
def transcribe_audio(audio_path):
    segments, _ = model.transcribe(audio_path)
    text = " ".join([seg.text for seg in segments])
    return text

#--3. LLM Query via OLLama
def query_llm(transcribe_text):
    # Call the OLLAMA model using subprocess
    system_prompt = f"""
    You are a smart CFD/FEA assistant for Ansys Fluent. 
    The user is a CFD/FEA engineer giving voice commands.
    Interpret the user's command into a Fluent operation.
    Here is the command: \"{transcribe_text}\" 
    Respond clearly and concisely in one sentence with the correct action,
    then suggest how to execute it in Ansys Fluent.
    """
    process = subprocess.Popen(
        ["ollama", "run", "openchat"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True  # important to return string directly
    )
    try:
        output, _ = process.communicate(input=system_prompt, timeout=15)
    except subprocess.TimeoutExpired:
        process.kill()
        output = "LLM timed out. Please try again."

    return output.strip()

def main():
    speak("Please give me a prompt.")
    audio_path = r"demo_audio/Recording.wav"
    transribed = transcribe_audio(r"demo_audio/Recording.wav")
    print("[your prompt]", transribed)
    speak(f"You said:  {transribed}")

    llm_response = query_llm(transribed)
    print("[LLM Response]", llm_response)
    speak(f"LLM response: {llm_response}")
    
    speak(llm_response)

if __name__ == "__main__":
    main()

