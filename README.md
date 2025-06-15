# YouTube Video Bot

This repository contains scripts to generate a YouTube video from a text script.

## Prerequisites

The scripts expect the `moviepy` package to be available. If you see an error like:

```
ModuleNotFoundError: No module named 'moviepy.editor'
```

install `moviepy` using pip:

```bash
pip install moviepy
```

You'll also need FFmpeg installed for video generation.

## Usage

The `video_creator.py` script combines images and audio into a single video. Make sure `output.mp3` and your images are ready in the `visuals/` folder before running it.

```bash
python video_creator.py
```

