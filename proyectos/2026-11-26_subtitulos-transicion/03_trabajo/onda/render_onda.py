"""Genera la animación de la onda (estilo DAW rosa/negro) como secuencia PNG con alfa.
Uso: python3 render_onda.py voz.wav salida_dir duracion_s inicio_audio_s [fps]
 - duracion_s: duración total del overlay
 - inicio_audio_s: segundo del overlay en el que empieza a sonar el WAV (t=0 del WAV)
"""
import sys, os, wave, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

wav, out, dur, a0 = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
fps = int(sys.argv[5]) if len(sys.argv) > 5 else 30
os.makedirs(out, exist_ok=True)

W, H = 1080, 250            # tamaño de la barra
HEAD = 64                   # franja del título
PINK = (255, 136, 156); BLACK = (25, 26, 30); GRID = (219, 119, 134); SEP = (135, 63, 76)
PPS = 1080 / 2.6            # píxeles por segundo (ventana visible ≈ 2,6 s)
PLAY_X = int(W * 0.30)      # posición fija del cursor

w = wave.open(wav); sr = w.getframerate(); ch = w.getnchannels(); sw = w.getsampwidth()
raw = w.readframes(w.getnframes())
if sw == 3:
    b = np.frombuffer(raw, np.uint8).reshape(-1, 3)
    x = (b[:, 0].astype(np.int32) | (b[:, 1].astype(np.int32) << 8) | (b[:, 2].astype(np.int32) << 16))
    x = np.where(x >= 1 << 23, x - (1 << 24), x) / float(1 << 23)
else:
    x = np.frombuffer(raw, np.int16) / 32768.0
x = x.reshape(-1, ch)
# envolvente de pico a 4x resolución de píxel
res = PPS * 4; hop = sr / res
nb = int(len(x) / hop)
env = np.zeros((nb, ch))
for i in range(nb):
    s = x[int(i * hop):int((i + 1) * hop) + 1]
    env[i] = np.abs(s).max(axis=0)
# suavizado: máximo móvil (~12 ms) + gaussiana (~10 ms) para un contorno redondeado tipo DAW
k = max(1, int(0.012 * res))
envm = np.stack([np.array([env[max(0, i - k):i + k + 1, c].max() for i in range(nb)]) for c in range(ch)], 1)
gs = 0.010 * res; gx = np.arange(-int(3 * gs), int(3 * gs) + 1); gk = np.exp(-gx**2 / (2 * gs**2)); gk /= gk.sum()
env = np.stack([np.convolve(envm[:, c], gk, mode="same") for c in range(ch)], 1)
env = np.clip(env / max(env.max(), 1e-6) * 0.92, 0, 1)

def amp(tarr, c):
    idx = tarr * res
    v = np.interp(idx, np.arange(nb), env[:, c], left=0, right=0)
    return v

font = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-SemiBold.otf", 40)
lane_h = (H - HEAD) // 2
cols = np.arange(W)
nfr = int(round(dur * fps))
for f in range(nfr):
    t = f / fps
    tw = t - a0                                   # tiempo del WAV bajo el cursor
    im = Image.new("RGBA", (W, H), PINK + (255,))
    d = ImageDraw.Draw(im)
    tcol = tw + (cols - PLAY_X) / PPS             # tiempo de cada columna
    # rejilla vertical cada 0,5 s (se desplaza con la onda)
    g0 = np.ceil((tw - PLAY_X / PPS) / 0.5) * 0.5
    g = g0
    while g < tw + (W - PLAY_X) / PPS:
        gx = PLAY_X + (g - tw) * PPS
        d.line([(gx, HEAD), (gx, H)], fill=GRID, width=2)
        g += 0.5
    d.line([(0, HEAD - 2), (W, HEAD - 2)], fill=SEP, width=3)
    # título que se desplaza con el clip (como en el DAW)
    tx = PLAY_X + (0 - tw) * PPS + 8
    d.text((max(10, tx) if tx < 10 else tx, 9), "Voces Lucho RK - RETRICA", font=font, fill=BLACK)
    # onda L / R
    for c in range(2):
        cy = HEAD + lane_h * c + lane_h // 2
        a = amp(tcol, min(c, env.shape[1] - 1)) * (lane_h / 2 - 6)
        d.line([(0, cy), (W, cy)], fill=BLACK, width=3)
        for xi in range(W):
            if a[xi] > 1:
                d.line([(xi, cy - a[xi]), (xi, cy + a[xi])], fill=BLACK)
    # cursor de reproducción
    d.line([(PLAY_X, 0), (PLAY_X, H)], fill=(255, 255, 255), width=4)
    # sombra inferior suave
    full = Image.new("RGBA", (W, H + 30), (0, 0, 0, 0))
    sh = Image.new("RGBA", (W, H + 30), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle([0, 10, W, H + 6], fill=(0, 0, 0, 120))
    sh = sh.filter(ImageFilter.GaussianBlur(10))
    full.alpha_composite(sh); full.alpha_composite(im, (0, 0))
    full.save(f"{out}/{f:04d}.png")
print("frames", nfr)
