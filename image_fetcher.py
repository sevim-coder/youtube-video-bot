import os
import re
import requests
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI


def load_env(path: str | None = None) -> None:
    """Load environment variables from a .env file if present."""
    env_path = Path(path) if path else Path(".env")
    if not load_dotenv(dotenv_path=env_path, override=True):
        print(f"⚠️ .env file not found at {env_path}, relying on existing env vars")


def sanitize_filename(title):
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', title.strip().lower())


def fetch_keywords(prompt: str, n: int = 5):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates keywords for visual content."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50
        )
        keywords = response.choices[0].message.content.split(',')
        return [kw.strip() for kw in keywords][:n]
    except Exception as e:
        raise RuntimeError(f"❌ OpenAI keyword generation failed: {e}")


def get_available_filename(dest_path, base_name):
    counter = 0
    candidate = dest_path / f"{base_name}.jpg"
    while candidate.exists():
        counter += 1
        candidate = dest_path / f"{base_name}({counter}).jpg"
    return candidate


def fetch_images(keywords, title):
    access_key = os.getenv("UNSPLASH_ACCESS_KEY")
    if not access_key:
        raise EnvironmentError("❌ UNSPLASH_ACCESS_KEY not found in environment")

    folder_name = sanitize_filename(title)
    dest_path = Path("visuals") / folder_name
    dest_path.mkdir(parents=True, exist_ok=True)

    for i, kw in enumerate(keywords, start=1):
        try:
            print(f"🔍 Searching for image with keyword: '{kw}'")
            url = f"https://api.unsplash.com/photos/random?query={kw}&client_id={access_key}"
            r = requests.get(url, timeout=30)
            r.raise_for_status()
            data = r.json()
            image_url = data['urls']['regular']
            img_data = requests.get(image_url, timeout=30)
            img_data.raise_for_status()
            filename = get_available_filename(dest_path, f"scene{i}")
            with open(filename, 'wb') as f:
                f.write(img_data.content)
            print(f"✅ Saved: {filename}")
        except Exception as e:
            print(f"⚠️ Failed to fetch image for '{kw}': {e}")


def main():
    try:
        load_env()
        script_file = Path("script.txt")
        if not script_file.exists():
            raise FileNotFoundError("❌ script.txt not found. Please run writer.py first.")

        with open(script_file, "r", encoding="utf-8") as f:
            title = f.readline().strip()
            script = f.read().strip()

        if not title or not script:
            raise ValueError("❌ script.txt must contain a title on the first line and script content below.")

        keywords = fetch_keywords(script)
        print(f"🔑 Keywords: {keywords}")
        fetch_images(keywords, title)

    except Exception as e:
        print(f"💥 Error: {e}")


if __name__ == "__main__":
    main()

