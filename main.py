"""
Demo: generate a video showcasing ~30 MoviePy‑v2 animations & transitions.

• Each segment lasts PER_CLIP_DURATION seconds and is labelled in‑frame.
• Low FPS (slow‑motion feel) + background song that auto‑loops to fit.
• Effects catalogue is easy to extend—just append to ANIMATIONS.

Useful docs / references:
- MoviePy effect reference: https://zulko.github.io/moviepy/index.html
- FadeIn / FadeOut classes: https://zulko.github.io/moviepy/reference/moviepy.video.fx.FadeIn.html
- SlideIn / SlideOut: https://zulko.github.io/moviepy/reference/moviepy.video.fx.SlideIn.html
- Resize with a λ‑function (for smooth zoom): https://zulko.github.io/moviepy/reference/moviepy.video.fx.Resize.html
- Freeze effect parameters: https://zulko.github.io/moviepy/reference/moviepy.video.fx.Freeze.html
- New “complex” demos: continuous 360° spin, orbit‑zoom, and pulsating glow.
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
# (Swap these paths to try different inputs)

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
    # Composite: mirror horizontally then rotate a bit
    ("Mirror X + Rotate 45°", lambda: build_effects(vfx.MirrorX(), vfx.Rotate(45))),
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
    ("Gamma Boost (1.8)",    lambda: build_effects(vfx.GammaCorrection(gamma=1.8))),
    ("Lum Contrast ↓",        lambda: build_effects(vfx.LumContrast(contrast=-40))),

    # Continuous rotation over the whole clip (smooth spin)
    ("Spin 360°", lambda: build_effects(
        vfx.Rotate(lambda t: 360 * t / PER_CLIP_DURATION)
    )),

    # Orbit effect: simultaneous slow spin + slight zoom‑in
    ("Orbit Zoom", lambda: build_effects(
        vfx.Rotate(lambda t: 45 * t / PER_CLIP_DURATION),
        vfx.Resize(lambda t: 1 + 0.15 * t)
    )),

    # Pulsating glow: margin halo + rapid gamma pulse
    ("Pulsate Glow", lambda: build_effects(
        vfx.Margin(40, color=(255, 255, 0)),
        vfx.Blink(0.15, 0.15),  # Blink expects positional on/off times
    )),

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

# --- Audio ---
# afx.AudioLoop repeats the song so it exactly matches total_duration
# (handy for short background tracks).
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
"""
MoviePy demo – modular effect library + simple sequencing helpers
=================================================================

• All basic/advanced effects are exposed as *functions* that take only the
  parameters you’ll most often tweak (duration, side, zoom factor, etc.).
• Compose multiple effects with `seq()` – sugar for chaining.
• Build a whole video by listing `(label, clip_fx)` tuples in `ANIMATIONS`.
• Background audio is auto‑looped to fill the runtime.

Docs worth bookmarking:
- MoviePy API     : https://zulko.github.io/moviepy/index.html
- Effect reference: https://zulko.github.io/moviepy/ref/videofx.html
"""

# ───────────────────────── Imports ──────────────────────────
from typing import Callable, List

from moviepy import ImageClip, TextClip, AudioFileClip, vfx, afx
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip, concatenate_videoclips

# ───────────────────────── Paths ────────────────────────────
image_path  = "assets/pic.png"   # ← swap to taste
audio_path  = "assets/song.mp3"
output_path = "assets/output.mp4"

# ───────────────────── Video parameters ─────────────────────
FPS               = 8
PER_CLIP_DURATION = 2
FONT              = "Arial"
FONT_SIZE         = 50
TEXT_COLOR        = "white"
TEXT_BG           = "black"

# ──────────────────── Effect primitives ─────────────────────
def fade(d: float = 0.8):
    """Cross‑fade in then out."""
    return [vfx.FadeIn(d), vfx.FadeOut(d)]

def slide_in(side: str = "left", d: float = 0.8):
    return [vfx.SlideIn(d, side)]

def slide_out(side: str = "left", d: float = 0.8):
    return [vfx.SlideOut(d, side)]

def rotate(deg: float = 90):
    return [vfx.Rotate(deg)]

def mirror(axis: str = "x"):
    return [vfx.MirrorX()] if axis.lower() == "x" else [vfx.MirrorY()]

def zoom(factor: float = 0.25, mode: str = "in"):
    sign = 1 if mode == "in" else -1
    return [vfx.Resize(lambda t: 1 + sign * factor * (t / PER_CLIP_DURATION))]

def bw():           return [vfx.BlackAndWhite()]
def invert():       return [vfx.InvertColors()]
def contrast(delta=40): return [vfx.LumContrast(contrast=delta)]
def gamma(val=1.5): return [vfx.GammaCorrection(gamma=val)]
def margin(size=20, color=(255,215,0)): return [vfx.Margin(size, color=color)]
def blink(on=0.2, off=0.2): return [vfx.Blink(on, off)]
def freeze(at="end"): return [vfx.Freeze(t=at, freeze_duration=PER_CLIP_DURATION)]
def time_mirror():   return [vfx.TimeMirror()]
def time_sym():      return [vfx.TimeSymmetrize()]
def supersample():   return [vfx.SuperSample(0.1, 6)]
def accel_decel():   return [vfx.AccelDecel()]
def painting():      return [vfx.Painting()]
def scroll_x(px=100):return [vfx.Scroll(0, px)]

# Complex combos
def spin360():       return [vfx.Rotate(lambda t: 360 * t / PER_CLIP_DURATION)]
def orbit_zoom():    return rotate(45) + zoom(0.15, "in")
def pulsate_glow():  return margin(40, (255,255,0)) + blink(0.15,0.15)

# ─────────────── Composition helpers ──────────────
def seq(*effect_funcs: List[Callable[[], List[Callable]]]):
    """Return a single list of effects executed in order."""
    effects = []
    for f in effect_funcs:
        effects.extend(f())
    return effects

def make_clip(label: str, effects: List[Callable]):
    """Create a CompositeVideoClip( base + overlay text )"""
    base = (
        ImageClip(image_path)
        .with_duration(PER_CLIP_DURATION)
        .with_fps(FPS)
        .with_effects(effects)
    )
    txt = (
        TextClip(label, fontsize=FONT_SIZE, color=TEXT_COLOR,
                 bg_color=TEXT_BG, font=FONT, text_align="center")
        .with_duration(PER_CLIP_DURATION)
        .with_position(("center", "bottom"))
    )
    return CompositeVideoClip([base, txt])

# ─────────────── Playlist of demo segments ───────────────
ANIMATIONS = [
    ("Fade In / Out",         seq(fade)),
    ("Slide In‑Left",         seq(slide_in)),
    ("Slide Out‑Right",       seq(slide_out)),
    ("Rotate 180°",           seq(rotate)),
    ("Mirror X",              seq(mirror)),
    ("Zoom‑In",               seq(zoom)),
    ("Black & White",         seq(bw)),
    ("Invert Colors",         seq(invert)),
    ("High Contrast",         seq(contrast)),
    ("Gamma Boost",           seq(gamma)),
    ("Blink",                 seq(blink)),
    ("Freeze End",            seq(freeze)),
    ("Time Mirror",           seq(time_mirror)),
    ("SuperSample",           seq(supersample)),
    ("Accel‑Decel",           seq(accel_decel)),
    ("Painting",              seq(painting)),
    ("Scroll X",              seq(scroll_x)),
    # composites
    ("Mirror + Rotate 45°",   seq(mirror, lambda: rotate(45))),
    ("Spin 360°",             seq(spin360)),
    ("Orbit Zoom",            seq(orbit_zoom)),
    ("Pulsate Glow",          seq(pulsate_glow)),
    ("Margin Glow",           seq(margin)),
]

# ─────────────── Build & render video ──────────────
clips = [make_clip(label, fx) for label, fx in ANIMATIONS]
video  = concatenate_videoclips(clips, method="compose")

# Loop music
audio_clip   = AudioFileClip(audio_path)
audio_looped = audio_clip.with_effects([afx.AudioLoop(duration=len(clips)*PER_CLIP_DURATION)])
video        = video.with_audio(audio_looped)

video.write_videofile(
    output_path,
    fps=FPS,
    codec="libx264",
    audio_codec="aac",
    preset="medium",
    threads=4,
)