import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()

API_KEY = os.getenv("ELEVEN_API_KEY")
VOICE_ID = os.getenv("VOICE_ID")

if not API_KEY:
    raise EnvironmentError("ELEVEN_API_KEY not set in environment")

client = ElevenLabs(api_key=API_KEY)


def text_to_speech(text: str, filename: str = "output.mp3") -> str:
    """Convert text to speech and save it to ``filename``."""
    if not VOICE_ID:
        raise EnvironmentError("VOICE_ID not set in environment")

    stream = client.text_to_speech.convert(
        voice_id=VOICE_ID,
        model_id="eleven_multilingual_v2",
        text=text,
        output_format="mp3_44100_128",
    )

    with open(filename, "wb") as f:
        for chunk in stream:
            f.write(chunk)

    return filename


if __name__ == "__main__":
    from writer import generate_script
    sample_script = generate_script(
        "Mercury Retrograde and Emotions",
        "How does Mercury Retrograde affect your mood, memory, and confidence?"
    )
    print("Narration:", sample_script)
    text_to_speech(sample_script, "output.mp3")

