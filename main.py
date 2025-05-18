"""
Demo: generate a video of ~30 MoviePy‑v2 animations/transitions.
Each segment shows one effect on the same image, lasts PER_CLIP_DURATION
seconds, and has a text overlay naming the effect.
"""

# ───────────────────────── Imports ──────────────────────────
from moviepy import ImageClip, TextClip, AudioFileClip, vfx, afx
from moviepy.video.compositing.CompositeVideoClip import (
    CompositeVideoClip,
    concatenate_videoclips,
)

# ───────────────────────── Paths ────────────────────────────
image_path  = "assets/pic.png"      # still image
audio_path  = "assets/song.mp3"      # background music
output_path = "assets/output.mp4"    # final video

# ───────────────────── Video parameters ─────────────────────
FPS               = 8    # slow feel
PER_CLIP_DURATION = 2    # seconds per effect
FONT              = "Arial"
FONT_SIZE         = 50
TEXT_COLOR        = "white"
TEXT_BG           = "black"

# ─────────────── Helper: wrap effects into list ─────────────
def build_effects(*effects):
    """Return a list of non‑None effect objects."""
    return [e for e in effects if e is not None]

# ─────────────── Catalogue of animation effects ─────────────
ANIMATIONS = [
    ("Fade In / Fade Out", lambda: build_effects(vfx.FadeIn(0.8), vfx.FadeOut(0.8))),
    ("Slide‑In Left",      lambda: build_effects(vfx.SlideIn(0.8, "left"))),
    ("Slide‑In Right",     lambda: build_effects(vfx.SlideIn(0.8, "right"))),
    ("Slide‑In Top",       lambda: build_effects(vfx.SlideIn(0.8, "top"))),
    ("Slide‑In Bottom",    lambda: build_effects(vfx.SlideIn(0.8, "bottom"))),
    ("Slide‑Out Left",     lambda: build_effects(vfx.SlideOut(0.8, "left"))),
    ("Slide‑Out Right",    lambda: build_effects(vfx.SlideOut(0.8, "right"))),
    ("Slide‑Out Top",      lambda: build_effects(vfx.SlideOut(0.8, "top"))),
    ("Slide‑Out Bottom",   lambda: build_effects(vfx.SlideOut(0.8, "bottom"))),
    ("Rotate 360°",        lambda: build_effects(vfx.Rotate(360))),
    ("Rotate 180°",        lambda: build_effects(vfx.Rotate(180))),
    ("Mirror X",           lambda: build_effects(vfx.MirrorX())),
    ("Mirror Y",           lambda: build_effects(vfx.MirrorY())),
    ("Zoom‑In (enlarge)",  lambda: build_effects(vfx.Resize(lambda t: 1 + 0.25 * t))),
    ("Zoom‑Out (shrink)",  lambda: build_effects(vfx.Resize(lambda t: 1.5 - 0.25 * t))),
    ("Black & White",      lambda: build_effects(vfx.BlackAndWhite())),
    ("Invert Colors",      lambda: build_effects(vfx.InvertColors())),
    ("Increase Contrast",  lambda: build_effects(vfx.LumContrast(contrast=40))),
    ("Gamma Brighten",     lambda: build_effects(vfx.GammaCorrection(gamma=1.5))),
    ("Blink",              lambda: build_effects(vfx.Blink(0.2, 0.2))),
    ("Freeze Start",       lambda: build_effects(vfx.Freeze(t=0, freeze_duration=PER_CLIP_DURATION))),
    ("Freeze End",         lambda: build_effects(vfx.Freeze(
                                  t=PER_CLIP_DURATION - 0.1,
                                  freeze_duration=PER_CLIP_DURATION))),
    ("Time Mirror",        lambda: build_effects(vfx.TimeMirror())),
    ("Time Symmetrize",    lambda: build_effects(vfx.TimeSymmetrize())),
    ("SuperSample",        lambda: build_effects(vfx.SuperSample(0.1, 6))),
    ("Accel‑Decel",        lambda: build_effects(vfx.AccelDecel())),
    ("Painting",           lambda: build_effects(vfx.Painting())),
    ("Scroll X",           lambda: build_effects(vfx.Scroll(0, 100))),
    ("Margin Glow",        lambda: build_effects(vfx.Margin(20, color=(255, 215, 0)))),
]

# ─────────────── Build one clip per animation ───────────────
clips = []
for label, effects_builder in ANIMATIONS:
    base_clip = (
        ImageClip(image_path)
        .with_duration(PER_CLIP_DURATION)
        .with_fps(FPS)
        .with_effects(effects_builder())
    )
    text_clip = (
        TextClip(
            text=label,
            font_size=FONT_SIZE,
            color=TEXT_COLOR,
            bg_color=TEXT_BG,
            text_align="center",
            font=FONT,
        )
        .with_duration(PER_CLIP_DURATION)
        .with_position(("center", "bottom"))
    )
    clips.append(CompositeVideoClip([base_clip, text_clip]))

# ─────────────── Concatenate and add audio  ────────────────
video = concatenate_videoclips(clips, method="compose")

total_duration = len(clips) * PER_CLIP_DURATION
audio_clip     = AudioFileClip(audio_path)
audio_looped   = audio_clip.with_effects([afx.AudioLoop(duration=total_duration)])
video          = video.with_audio(audio_looped)

# ───────────────────────── Render ───────────────────────────
video.write_videofile(
    output_path,
    fps=FPS,
    codec="libx264",
    audio_codec="aac",
    preset="medium",
    threads=4,
)