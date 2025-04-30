from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import tempfile

def speak_gtts(text):
    try:
        tts = gTTS(text=text, lang='en')
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            tts.save(fp.name)
            audio = AudioSegment.from_file(fp.name, format="mp3")
            play(audio)
    except Exception as e:
        print(f"🛑 TTS error: {e}")
