import subprocess
import pyttsx3
from faster_whisper import WhisperModel
import fluent_automation as fluent
import speech_recognition as sr
import unicodedata
# --1. TTS setup--
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def clean_text(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')

# --2. STT setup--
# Load the model (small)
model = WhisperModel("small",  device="cpu", compute_type="float32")

# # Transcribe from file
# def transcribe_audio_from_files(audio_path):
#     segments, _ = model.transcribe(audio_path)
#     text = " ".join([seg.text for seg in segments])
#     return text
# Transcribe from microphone in real-time
def transcribe_audio():
    recognizer = sr.Recognizer()
    try:
        # Use the microphone as the audio source
        with sr.Microphone() as source:
            print("Listening... Speak your prompt.")
            recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
            audio = recognizer.listen(source)
            # Save the audio to a file (optional, for debugging or reuse)
            with open("temp_input.wav", "wb") as f:
                f.write(audio.get_wav_data())
                # Transcribe with Whisper
                segments, _ = model.transcribe("temp_input.wav")
                text = " ".join([seg.text for seg in segments])
                return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return ""
    except sr.RequestError as e:
        print(f"Could not access microphone; {e}")
        return ""
def query_llm(transcribe_text):
    # Call the OLLAMA model using subprocess
    # system_prompt = clean_text(f"""
    # You are a smart CFD/FEA assistant for Ansys Fluent. 
    # The user is a CFD/FEA engineer giving voice commands.
    # Interpret the user's command into a Fluent operation.
    # Here is the command: \"{transcribe_text}\" 
    # Respond clearly and concisely in one sentence with the correct action,
    # then suggest how to execute it in Ansys Fluent.
    # """)

    system_prompt = clean_text(f"""
    You are Fluent Assistant — a voice-based CFD/FEA assistant for Ansys Fluent.
    You were created by Bill, a top 1% CFD/FEA and Machine Learning engineer.
    Your mission is to interpret spoken or typed commands and translate them into correct Fluent operations.
    Always introduce yourself proudly if the user asks about your name or creator.
    Here is the command: \"{transcribe_text}\" 
    Respond clearly and concisely in one sentence with the correct action,
    then suggest how to execute it in Ansys Fluent.
    """)

    process = subprocess.Popen(
        ["ollama", "run", "openchat"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True  # important to return string directly
    )
    try:
        output, _ = process.communicate(input=system_prompt, timeout=15)
        return output.strip()
    except subprocess.TimeoutExpired:
        process.kill()
        output = "LLM timed out. Please try again."

    return output.strip()


# --6. Suggestion helper
def print_example_prompts():
    suggestions = [
        "🧠 Try saying:",
        "- Initialize the solution using hybrid initialization.",
        "- Create a velocity inlet boundary at inlet with 5 m/s.",
        "- Start steady-state simulation with 500 iterations.",
        "- Export the temperature contour to a PNG file.",
        "- Set turbulence model to k-epsilon.",
        "- Mesh the geometry using automatic settings.",
        "- Save the case and data files.",
    ]
    print("\n".join(suggestions))
    speak("Please try one of the suggested commands.")

def main():
    # mode = input("Choose input mode [voice/text]: ").strip().lower()

    # if mode == "text":
    #     transcribed = input("⌨️ Type your Fluent command: ")
    # else:
    #     transcribed = transcribe_audio()

    while True:
        # audio_path = r"demo_audio/Recording.wav"
        # transribed = transcribe_audio(r"demo_audio/Recording.wav")
       
        # #Here is model is audio 
        # transcribed = transcribe_audio()
        # print("[your prompt]", transcribed)

        transcribed = input("⌨️ Type your Fluent command: ")
        print("[your prompt]", transcribed)
        # Exit keywords
        if any(word in transcribed.lower() for word in ["stop", "exit", "quit", "shutdown"]):
            speak("Stopping simulation. Goodbye!")
            print("🛑 Exiting FluentAi.")
            break

        llm_response = query_llm(transcribed)
        print("[LLM Response]", llm_response)
        speak(f"LLM response: {llm_response}")
        
        # speak(llm_response)
         # Suggest example prompts if input was vague
                # Suggest example prompts if input was unclear
        if any(keyword in llm_response.lower() for keyword in ["specific", "unclear", "incomplete", "does not provide", "not provide"]):
            print_example_prompts()

        # write the code 

if __name__ == "__main__":
    main()

