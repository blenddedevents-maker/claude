"""Visualización de batería estilo DAW (pistas MIDI naranjas + pistas de audio turquesa), PNG con alfa.
Uso: python3 render_bateria.py bateria.wav salida_dir duracion_s inicio_audio_s [fps]"""
import sys, os, numpy as np, librosa, scipy.signal as ss
from PIL import Image, ImageDraw, ImageFilter, ImageFont
wav, out, dur, a0 = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
fps = int(sys.argv[5]) if len(sys.argv) > 5 else 30
os.makedirs(out, exist_ok=True)
y, sr = librosa.load(wav, sr=44100, mono=False)
mono = y.mean(0) if y.ndim > 1 else y
L = len(mono) / sr
def band(lo, hi):
    if lo is None: b = ss.butter(4, hi, "low", fs=sr, output="sos")
    elif hi is None: b = ss.butter(4, lo, "high", fs=sr, output="sos")
    else: b = ss.butter(4, [lo, hi], "band", fs=sr, output="sos")
    return ss.sosfiltfilt(b, mono)
def hits(sig, delta):
    o = librosa.onset.onset_detect(y=sig.astype(np.float32), sr=sr, hop_length=256, units="time", backtrack=False, delta=delta)
    return list(o)
kick = hits(band(None, 140), 0.25); snare = hits(band(180, 2500), 0.35); hat = hits(band(6000, None), 0.25)
print("golpes: bombo", len(kick), "caja", len(snare), "platos", len(hat))
tempo, beats = librosa.beat.beat_track(y=mono, sr=sr, units="time"); bp = 60 / float(np.atleast_1d(tempo)[0]); b0 = float(beats[0]) if len(beats) else 0
# envolventes para las pistas de audio (pico suavizado)
PPS = 1080 / 2.6; res = PPS * 4
def env_of(sig):
    hop = sr / res; nb = int(len(sig) / hop)
    e = np.array([np.abs(sig[int(i * hop):int((i + 1) * hop) + 1]).max() for i in range(nb)])
    k = max(1, int(0.012 * res)); e = np.array([e[max(0, i - k):i + k + 1].max() for i in range(nb)])
    gs = 0.010 * res; gx = np.arange(-int(3 * gs), int(3 * gs) + 1); gk = np.exp(-gx**2 / (2 * gs**2)); gk /= gk.sum()
    e = np.convolve(e, gk, "same"); return np.clip(e / e.max() * 0.92, 0, 1)
chans = [y[0], y[1]] if y.ndim > 1 else [mono, mono]
envs_full = [env_of(c) for c in chans]
envs_low = [env_of(ss.sosfiltfilt(ss.butter(4, 250, "low", fs=sr, output="sos"), c)) for c in chans]
W = 1080; PLAY_X = int(W * 0.30)
OR, ORH = (254, 155, 38), (226, 132, 20); CY, CYH = (82, 253, 228), (60, 222, 200); DK = (17, 32, 35)
font = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-SemiBold.otf", 22)
LAN = [("midi", 62, [(kick, 0.75), (snare, 0.35)], "Bombo / Caja"),
       ("audio", 86, envs_low, "Batería (graves)"),
       ("midi", 62, [(hat, 0.55)], "Platos"),
       ("audio", 86, envs_full, "Batería")]
H = sum(l[1] for l in LAN); HD = 16
for f in range(int(round(dur * fps))):
    t = f / fps; tw = t - a0
    im = Image.new("RGBA", (W, H), (0, 0, 0, 255)); d = ImageDraw.Draw(im, "RGBA")
    cx0 = PLAY_X + (0 - tw) * PPS; cx1 = PLAY_X + (L - tw) * PPS; x0, x1 = max(0, cx0), min(W, cx1)
    yt = 0
    for kind, h, data, label in LAN:
        bg, hd = (OR, ORH) if kind == "midi" else (CY, CYH)
        d.rectangle([0, yt, W, yt + h - 3], fill=tuple(int(c * 0.3) for c in bg))
        if x1 > x0:
            d.rectangle([x0, yt, x1, yt + h - 3], fill=bg)
            if kind == "audio":
                d.rectangle([x0, yt, x1, yt + HD + 8], fill=bg)
                if cx0 > -400: d.text((cx0 + 6, yt - 2), label, font=font, fill=DK)
            k0 = int(np.floor((tw - PLAY_X / PPS - b0) / bp)); k1 = int(np.ceil((tw + (W - PLAY_X) / PPS - b0) / bp))
            for k in range(k0, k1 + 1):
                gx = PLAY_X + (b0 + k * bp - tw) * PPS
                if x0 <= gx <= x1: d.line([(gx, yt + (HD + 8 if kind == "audio" else 4)), (gx, yt + h - 3)], fill=(0, 0, 0, 45), width=1)
            if kind == "midi":
                for (ts_, rel) in data:
                    ny = yt + 6 + (1 - rel) * (h - 18)
                    for s in ts_:
                        nx0 = PLAY_X + (s - tw) * PPS; nx1 = nx0 + 0.11 * PPS
                        if nx1 < 0 or nx0 > W: continue
                        on = s <= tw <= s + 0.11
                        d.rounded_rectangle([nx0, ny - 3, nx1, ny + 3], radius=2, fill=(255, 255, 255) if on else DK, outline=DK if on else None, width=2 if on else 0)
            else:
                top = yt + HD + 10; lh = (yt + h - 6 - top) / 2
                cols = np.arange(W); tc = tw + (cols - PLAY_X) / PPS
                for ci in range(2):
                    cy = top + lh * ci + lh / 2
                    a = np.interp(tc * res, np.arange(len(data[ci])), data[ci], left=0, right=0) * (lh / 2 - 2)
                    d.line([(x0, cy), (x1, cy)], fill=DK, width=2)
                    for xi in range(int(x0), int(x1)):
                        if a[xi] > 1: d.line([(xi, cy - a[xi]), (xi, cy + a[xi])], fill=DK)
        d.line([(0, yt + h - 2), (W, yt + h - 2)], fill=(10, 20, 20), width=3)
        yt += h
    d.line([(PLAY_X, 0), (PLAY_X, H)], fill=(255, 255, 255), width=4)
    full = Image.new("RGBA", (W, H + 30), (0, 0, 0, 0)); sh = Image.new("RGBA", (W, H + 30), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle([0, 10, W, H + 6], fill=(0, 0, 0, 120)); sh = sh.filter(ImageFilter.GaussianBlur(10))
    full.alpha_composite(sh); full.alpha_composite(im, (0, 0)); full.save(f"{out}/{f:04d}.png")
print("tempo", tempo, "frames", f + 1)
