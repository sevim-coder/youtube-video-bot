import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()

client = ElevenLabs(
    api_key=os.getenv("ELEVEN_API_KEY")
)

VOICE_ID = os.getenv("VOICE_ID")

def text_to_speech(text, filename="output.mp3"):
    stream = client.text_to_speech.convert(
        voice_id=VOICE_ID,
        model_id="eleven_multilingual_v2",
        text=text,
        output_format="mp3_44100_128"
    )

    with open(filename, "wb") as f:
        for chunk in stream:
            f.write(chunk)


if __name__ == "__main__":
    from writer import generate_script
    sample_script = generate_script(
        "Mercury Retrograde and Emotions",
        "How does Mercury Retrograde affect your mood, memory, and confidence?"
    )
    print("Narration:", sample_script)
    text_to_speech(sample_script, "output.mp3")

