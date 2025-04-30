from bark import generate_audio

def generate_voice(text: str):
    audio_array = generate_audio(
        text,
        history_prompt="v2/en_speaker_6",  # Calm, confident, professional voice
        text_temp=0.2,                     # Lower = clearer, serious tone
        waveform_temp=0.7                 # Balanced expressiveness
    )
    return audio_array