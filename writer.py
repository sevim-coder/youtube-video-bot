import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_script(title, summary=None):
    topic_style = os.getenv("TOPIC_STYLE", "general")

    prompt = f"""
You are a scriptwriter for a women's interest YouTube channel with a focus on "{topic_style}".
Create a natural, engaging 90-second narration for the video titled: "{title}"
{f"Context: {summary}" if summary else ""}

- Speak directly to the audience using a calm, inspiring tone
- Avoid jargon
- Emphasize emotion, self-reflection, and relatable examples
- Use short paragraphs, suitable for voice narration
- Keep it under 200 words
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert scriptwriter for voice-based YouTube videos."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print("❌ OpenAI Error:", e)
        return None


def save_script(title, script):
    try:
        with open("script.txt", "w", encoding="utf-8") as f:
            f.write(f"{title.strip()}\n{script.strip()}\n")
        print("\n💾 Script saved to script.txt")
    except Exception as e:
        print(f"❌ Failed to save script.txt: {e}")


if __name__ == "__main__":
    video_title = "Mercury Retrograde and Your Emotions"
    summary = "How this cosmic event influences your mental clarity, mood, and focus."
    script = generate_script(video_title, summary)
    if script:
        print("\n🎤 Script:\n", script)
        save_script(video_title, script)

