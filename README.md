# YouTube Video Bot

This project automates the creation of short narrated videos. It uses OpenAI to generate a script, ElevenLabs for text-to-speech, Unsplash for images and MoviePy to build the final video.

## Setup

1. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and fill in your API keys.

## Usage

1. Generate a script:
   ```bash
   python writer.py
   ```
   This creates `script.txt`.
2. Create the narration audio:
   ```bash
   python main.py
   ```
3. Fetch images for the script:
   ```bash
   python image_fetcher.py
   ```
4. Build the final video:
   ```bash
   python video_creator.py
   ```

Each step requires the previous step's output.
