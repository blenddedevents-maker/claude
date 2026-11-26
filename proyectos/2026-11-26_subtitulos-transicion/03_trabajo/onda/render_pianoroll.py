"""Animación piano roll (estilo DAW verde) a partir de notas detectadas, secuencia PNG con alfa.
Uso: python3 render_pianoroll.py notas.json wav salida_dir duracion_s inicio_audio_s [fps]"""
import sys, os, json, numpy as np, librosa
from PIL import Image, ImageDraw, ImageFilter, ImageFont
notes = json.load(open(sys.argv[1])); wav = sys.argv[2]; out = sys.argv[3]
dur, a0 = float(sys.argv[4]), float(sys.argv[5]); fps = int(sys.argv[6]) if len(sys.argv) > 6 else 30
os.makedirs(out, exist_ok=True)
y, sr = librosa.load(wav, sr=22050, mono=True)
tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units="time")
bp = 60.0 / float(np.atleast_1d(tempo)[0]); b0 = float(beats[0]) if len(beats) else 0.0
wav_len = len(y) / sr
W = 1080; LANE = 74; HEADR = 16; NL = 4; H = LANE * NL
PPS = 1080 / 2.6; PLAY_X = int(W * 0.30)
LANES = [  # (color fondo, color cabecera, rango midi)
    ((54, 187, 1), (44, 160, 0), (0, 47)),
    ((31, 254, 157), (22, 214, 132), (47, 55)),
    ((0, 181, 164), (0, 150, 136), (55, 62)),
    ((123, 254, 92), (100, 220, 72), (62, 128)),
]
NOTE = (21, 35, 38); GRID = (0, 0, 0, 40)
font = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-Bold.otf", 15)
lane_notes = []
for (_, _, (lo, hi)) in LANES:
    ns = [n for n in notes if lo <= n[2] < hi]
    ps = [n[2] for n in ns] or [lo]
    lane_notes.append((ns, min(ps), max(ps)))
for f in range(int(round(dur * fps))):
    t = f / fps; tw = t - a0
    im = Image.new("RGBA", (W, H), (0, 0, 0, 255)); d = ImageDraw.Draw(im, "RGBA")
    clip_x0 = PLAY_X + (0 - tw) * PPS; clip_x1 = PLAY_X + (wav_len - tw) * PPS
    for li, ((bg, hd, _), (ns, pmin, pmax)) in enumerate(zip(LANES, lane_notes)):
        yt = li * LANE
        # fondo de pista (fuera del clip, más oscuro, como en el DAW)
        d.rectangle([0, yt, W, yt + LANE - 3], fill=tuple(int(c * 0.35) for c in bg))
        x0, x1 = max(0, clip_x0), min(W, clip_x1)
        if x1 > x0:
            d.rectangle([x0, yt, x1, yt + LANE - 3], fill=bg)
            d.rectangle([x0, yt, x1, yt + HEADR], fill=hd)
            if clip_x0 > -60: d.text((clip_x0 + 6, yt - 3), "...", font=font, fill=NOTE)
            # rejilla de pulsos
            k0 = int(np.floor((tw - PLAY_X / PPS - b0) / bp)); k1 = int(np.ceil((tw + (W - PLAY_X) / PPS - b0) / bp))
            for k in range(k0, k1 + 1):
                gx = PLAY_X + (b0 + k * bp - tw) * PPS
                if x0 <= gx <= x1: d.line([(gx, yt + HEADR), (gx, yt + LANE - 3)], fill=GRID, width=1)
            # notas
            span = max(pmax - pmin, 1); top, bot = yt + HEADR + 6, yt + LANE - 10
            for (s, e, p, v) in ns:
                nx0 = PLAY_X + (s - tw) * PPS; nx1 = PLAY_X + (e - tw) * PPS
                if nx1 < 0 or nx0 > W: continue
                ny = bot - (p - pmin) / span * (bot - top)
                on = s <= tw <= e
                col = (255, 255, 255, 255) if on else NOTE + (255,)
                d.rounded_rectangle([nx0, ny - 4, max(nx1 - 2, nx0 + 3), ny + 4], radius=3, fill=col,
                                    outline=NOTE if on else None, width=2 if on else 0)
        d.line([(0, yt + LANE - 2), (W, yt + LANE - 2)], fill=(10, 20, 20), width=3)
    d.line([(PLAY_X, 0), (PLAY_X, H)], fill=(255, 255, 255), width=4)
    full = Image.new("RGBA", (W, H + 30), (0, 0, 0, 0)); sh = Image.new("RGBA", (W, H + 30), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle([0, 10, W, H + 6], fill=(0, 0, 0, 120)); sh = sh.filter(ImageFilter.GaussianBlur(10))
    full.alpha_composite(sh); full.alpha_composite(im, (0, 0)); full.save(f"{out}/{f:04d}.png")
print("tempo", tempo, "frames", f + 1)
