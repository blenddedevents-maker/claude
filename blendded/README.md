# BLENDDED — Premium Festival Visual

A seamless 15-second loop for giant LED screens, rendered procedurally with a GPU shader.
It is not a stock template: every frame is computed from the brand's own logo.

## Deliverables

| File | Use |
|---|---|
| `output/BLENDDED_LED_4K60_loop.mp4` | **Master**: 3840×2160, 60 fps, 15 s (900 frames), H.264 High, no audio |
| `output/BLENDDED_LED_1080p60_loop.mp4` | Lightweight copy for previews and phones |
| `output/stills/` | Key frames (normal and at the drop) |
| `visual.html` | Real-time version (WebGL2). Opens in any browser; click for full screen |
| `assets/blendded_logo.svg` | Logo vectorised from the original artwork (letterforms only) |

## Musical structure (sync with the DJ)

The loop lasts exactly **32 beats at 128 BPM** (8 bars of 4/4), so it locks to the tempo:

| Time | Beat | Event |
|---|---|---|
| 0.00 s | 1 | Start of the loop (calm point, no impact) |
| every 0.469 s | each beat | Pulse of light in the logo and the flares |
| 2.81 s → 3.75 s | 7–8 | Build-up: energy and lasers intensify |
| **3.75 s** | **9** | **IMPACT 1**: white/violet flash, double shockwave, anamorphic sweep, burst of particles |
| every 2 bars | — | Chrome glint sweeps across the letters |
| 10.31 s → 11.25 s | 23–24 | Build-up |
| **11.25 s** | **25** | **IMPACT 2** |

To hit a drop, fire the clip (or set its cue point) so that second 3.75 or 11.25 lands on the drop.
At 120/126/130 BPM, adjust the clip speed in the media server (e.g. Resolume: BPM Sync → 128).

## Visual layers

1. **Energy currents**: bundles of fine ultraviolet strands following a domain-warped noise field (half-resolution HDR pass).
2. **3D orbital currents**: two tilted elliptical rings. The back arc passes behind the logo and the front arc runs below it.
3. **Lasers**: 6 beams from the stage plus 2 crossed beams that come in during impacts.
4. **Particles**: 5 layers with seamless infinite depth and a surge on each drop.
5. **Chrome logo**: rounded bevel computed from a signed distance field, white-chrome reflection with a horizon line, reflections of the energy field, moving speculars and a short extrusion for depth.
6. **Signature flares**: the six star sparkles from the original artwork, in the same positions.
7. **Grading**: ACES tonemapping, vignette, and dither so 8-bit LED walls show no banding.

**Seamless loop:** every movement is a periodic function with integer multiples of the period.
Measured: the jump from frame 899 → 0 equals any other beat transition (9.07 vs 9.08 mean difference), so the restart can't be seen.

## Playback recommendations

- Resolume / Arena: convert to **DXV3** (or HAP) for smooth 4K60 playback: `File → Convert`.
- Disvoice/Watchout/Millumin: HAP Q or ProRes 422 HQ if the server prefers it (`ffmpeg -i master.mp4 -c:v prores_ks -profile:v 3 out.mov`).
- Ultra-wide screens: the logo takes up 66% of the width with negative space around it. Scale "fit height" and fill the sides with black, or render a custom resolution (see below).

## Re-render (any resolution)

```bash
python3 src/prep_logo.py assets/blendded_logo.svg src/logo_tex.png   # logo texture
python3 src/build.py visual.html                                       # self-contained HTML
node src/render.mjs 3840 2160 60 15 out                                # W H FPS SECONDS OUT
```
Requires: Node + Playwright (Chromium), ffmpeg, Python with numpy/opencv/cairosvg/Pillow.
For LED panels with a non-standard resolution (e.g. 7680×1080), change `W H`: the composition adapts.
