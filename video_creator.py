from pathlib import Path
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips


def create_video(image_folder: str, audio_file: str, output_file: str = "final.mp4", image_duration: int = 3) -> None:
    """Combine images and an audio narration into a simple slideshow video."""
    folder = Path(image_folder)
    images = sorted(folder.glob("*.jpg"))
    if not images:
        raise FileNotFoundError(f"No images found in {folder}")

    audio = AudioFileClip(audio_file)

    clips = [ImageClip(str(img)).set_duration(image_duration) for img in images]
    slideshow = concatenate_videoclips(clips, method="compose")
    slideshow = slideshow.set_audio(audio).set_duration(audio.duration)
    slideshow.write_videofile(output_file, fps=24)


def main():
    title_dir = Path("visuals") / "mercury_retrograde_and_your_emotions"
    create_video(title_dir, "output.mp3")


if __name__ == "__main__":
    main()
