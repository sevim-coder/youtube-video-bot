import os
from dotenv import load_dotenv
from tts import text_to_speech

load_dotenv()

def read_script(filepath="script.txt"):
    if not os.path.exists(filepath):
        raise FileNotFoundError("❌ script.txt not found. Please run writer.py first.")
    
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    if len(lines) < 2:
        raise ValueError("❌ script.txt must contain at least a title and script body.")
    
    title = lines[0].strip()
    script = "".join(lines[1:]).strip()
    return title, script

if __name__ == "__main__":
    try:
        title, script = read_script()
        print("📝 Title:", title)
        print("📜 Script:\n", script)
        mp3 = text_to_speech(script, "output.mp3")
        print(f"🔊 Audio saved to {mp3}")
    except Exception as e:
        print("💥 Error:", e)

