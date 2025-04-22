import subprocess
import pyttsx3
from faster_whisper import WhisperModel
import fluent_automation as fluent
import speech_recognition as sr

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
# Transcribe from microphone in real-time
def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    try:
        # Use the microphone as the audio source
        with sr.AudioFile(audio_path) as source:
            print("Listening... Speak your prompt.")
            audio = recognizer.listen(source)
            # Save the audio to a file
            with open("temp_input.wav", "wb") as f:
                f.write(audio.get_wav_data())
                with sr.Microphone() as source:
                    print("Listening... Speak your prompt.")
                    audio = recognizer.listen(source)
                    #Save the audio to a file
                    with open("temp_input.wav", "wb") as f:
                        f.write(audio.get_wav_data())
                
                    # Transcribe with Whisper
                    segments, _ = model.transcribe("temp_input.wav")
                    text = " ".join([seg.text for seg in segments])
                    return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
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
    while True:
        audio_path = r"demo_audio/Recording.wav"
        transribed = transcribe_audio(r"demo_audio/Recording.wav")
        print("[your prompt]", transribed)
        speak(f"You said:  {transribed}")

        # Exit keywords
        if any(word in transcribed.lower() for word in ["stop", "exit", "quit", "shutdown"]):
            speak("Stopping simulation. Goodbye!")
            print("🛑 Exiting FluentAi.")
            break

        llm_response = query_llm(transribed)
        print("[LLM Response]", llm_response)
        speak(f"LLM response: {llm_response}")
        
        speak(llm_response)

if __name__ == "__main__":
    main()

