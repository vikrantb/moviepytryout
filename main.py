"""
Simple MoviePy demo (single file)
=================================

• Shows a handful of common effects – each labelled on screen.
• Easy to add / tweak effects: just write a tiny function and list it in
  ANIMATIONS.
• Background song will loop automatically to match total runtime.

Tested with MoviePy v2.x and Python 3.12.
"""

# ───────────── Imports ─────────────
from moviepy import ImageClip, TextClip, AudioFileClip, vfx, afx
from moviepy.video.compositing.CompositeVideoClip import (
    CompositeVideoClip,
    concatenate_videoclips,
)

# ─────────── Configuration ─────────
IMAGE_PATH  = "assets/pic.png"
AUDIO_PATH  = "assets/song.mp3"
OUTPUT_PATH = "assets/output.mp4"

FPS               = 8          # frame‑rate
PER_CLIP_DURATION = 2          # seconds each effect is shown
FONT              = "Arial"
FONT_SIZE         = 50
TEXT_COLOR        = "white"
TEXT_BG           = "black"

# ───── Effect helper ─────
def wrap(*items):
    """Return a list of effect objects, removing any Nones."""
    return [e for e in items if e is not None]

# ───── Individual effects (functions that RETURN a list) ─────
def fade():            return wrap(vfx.FadeIn(0.8), vfx.FadeOut(0.8))
def slide_left():      return wrap(vfx.SlideIn(0.8, "left"))
def rotate_180():      return wrap(vfx.Rotate(180))
def zoom_in():         return wrap(vfx.Resize(lambda t: 1 + 0.25 * (t/PER_CLIP_DURATION)))
def bw():              return wrap(vfx.BlackAndWhite())
def blink():           return wrap(vfx.Blink(0.2, 0.2))
def spin():            return wrap(vfx.Rotate(lambda t: 360 * t / PER_CLIP_DURATION))
def pulsate():         return wrap(
                           vfx.Margin(40, color=(255, 255, 0)),
                           vfx.Blink(0.15, 0.15)
                       )

# ───── Playlist (label, effect‑function) ─────
ANIMATIONS = [
    ("Fade In / Out", fade),
    ("Slide‑In Left", slide_left),
    ("Rotate 180°",   rotate_180),
    ("Zoom‑In",       zoom_in),
    ("Black & White", bw),
    ("Blink",         blink),
    ("Spin 360°",     spin),
    ("Pulsate Glow",  pulsate),
]

# ───── Build clips ─────
clips = []
for label, fx_func in ANIMATIONS:
    base = (
        ImageClip(IMAGE_PATH)
        .with_duration(PER_CLIP_DURATION)
        .with_fps(FPS)
        .with_effects(fx_func())
    )
    txt = (
        TextClip(
            text=label,
            font=FONT,
            font_size=FONT_SIZE,
            color=TEXT_COLOR,
            bg_color=TEXT_BG,
            text_align="center"
        )
        .with_duration(PER_CLIP_DURATION)
        .with_position(("center", "bottom"))
    )
    clips.append(CompositeVideoClip([base, txt]))

video = concatenate_videoclips(clips, method="compose")

# ───── Loop background audio ─────
total_dur = len(clips) * PER_CLIP_DURATION
audio = AudioFileClip(AUDIO_PATH).with_effects([afx.AudioLoop(duration=total_dur)])
video = video.with_audio(audio)

# ───── Render ─────
video.write_videofile(
    OUTPUT_PATH,
    fps=FPS,
    codec="libx264",
    audio_codec="aac",
    preset="medium",
    threads=4,
)