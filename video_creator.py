from pathlib import Path
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips


def sanitize_filename(title: str) -> str:
    return ''.join(c if c.isalnum() or c in '-_' else '_' for c in title.lower().strip())


def create_video(images_dir: Path, audio_file: Path, output: Path = Path("video.mp4")) -> Path:
    """Build a simple slideshow video using the images and audio."""
    if not audio_file.exists():
        raise FileNotFoundError(f"Audio file '{audio_file}' not found")

    audio = AudioFileClip(str(audio_file))
    img_paths = sorted(images_dir.glob("*.jpg"))
    if not img_paths:
        raise FileNotFoundError(f"No images found in {images_dir}")

    duration = audio.duration / len(img_paths)
    clips = [ImageClip(str(p)).set_duration(duration).resize(height=720) for p in img_paths]
    video = concatenate_videoclips(clips, method="compose").set_audio(audio)
    video.write_videofile(str(output), fps=24, codec="libx264", audio_codec="aac")
    return output


def main():
    script_file = Path("script.txt")
    if not script_file.exists():
        raise FileNotFoundError("script.txt not found. Run writer.py first.")

    title = script_file.read_text(encoding="utf-8").splitlines()[0]
    folder = sanitize_filename(title)
    images_dir = Path("visuals") / folder
    audio_file = Path("output.mp3")
    create_video(images_dir, audio_file)


if __name__ == "__main__":
    main()
