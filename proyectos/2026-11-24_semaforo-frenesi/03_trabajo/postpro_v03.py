"""v03 — Prepara las capas para componer con el título DETRÁS del semáforo.
Entrada: <base>.png (render) y <base>_mask.png (alfa del semáforo).
Salida en <dir_salida>/:
  capa_fondo.png   render graduado + atmósfera (bruma violeta y bokeh)  → debajo del texto
  capa_frente.png  semáforo recortado (RGBA)                            → encima del texto
  capa_brillo.png  halo de las luces (fondo negro, mezclar en 'screen') → encima de todo
  capa_grano.png   grano de película (gris 50 %, mezclar en 'overlay')  → encima de todo
Uso: python3 postpro_v03.py <base> <dir_salida>
"""
import sys, os
import numpy as np
from PIL import Image, ImageFilter

base, outdir = sys.argv[1], sys.argv[2]
os.makedirs(outdir, exist_ok=True)
rgb = Image.open(base + ".png").convert("RGB")
W, H = rgb.size
a = np.asarray(rgb).astype(np.float32) / 255
mask_im = Image.open(base + "_mask.png").convert("RGBA").split()[3].resize((W, H))
m = np.asarray(mask_im).astype(np.float32) / 255

def save(arr, name, mode="RGB"):
    Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8), mode).save(os.path.join(outdir, name))

# ---------- gradación común (look flash nocturno)
def grade(x):
    x = np.clip((x - 0.012) / 0.988, 0, 1) ** 1.06
    lum = x.mean(axis=2, keepdims=True)
    x = x + np.clip(1 - lum * 3, 0, 1) * np.array([0.006, -0.002, 0.018])   # sombras hacia violeta
    g = x.mean(axis=2, keepdims=True)
    return np.clip(g + (x - g) * 1.12, 0, 1)

a = grade(a)

# ---------- halo de las luces
lum = a.max(axis=2); sat = lum - a.min(axis=2)
hm = np.clip((lum - 0.55) / 0.45, 0, 1) * np.clip(sat * 2.5, 0, 1)
hi = Image.fromarray((a * hm[..., None] * 255).astype(np.uint8))
glow = np.zeros_like(a)
for r, w in ((W * .004, .55), (W * .018, .65), (W * .05, .55), (W * .12, .35)):
    glow += np.asarray(hi.filter(ImageFilter.GaussianBlur(r))).astype(np.float32) / 255 * w
save(np.clip(glow, 0, 1), "capa_brillo.png")

# ---------- atmósfera del fondo: bruma violeta + bokeh desenfocado
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
haze = np.exp(-(((xx - W * .18) / (W * .55)) ** 2 + ((yy - H * .2) / (H * .45)) ** 2))[..., None] * np.array([.10, .035, .20])
haze += np.exp(-(((xx - W * .9) / (W * .45)) ** 2 + ((yy - H * .85) / (H * .35)) ** 2))[..., None] * np.array([.05, .02, .12])
bok = Image.new("RGB", (W, H), (0, 0, 0))
from PIL import ImageDraw
d = ImageDraw.Draw(bok)
rng = np.random.default_rng(12)
pal = [(150, 70, 255), (90, 110, 255), (255, 150, 60), (230, 60, 220), (255, 220, 170)]
for _ in range(24):
    x, y = rng.uniform(0, W), rng.uniform(0, H)
    r = rng.uniform(W * .012, W * .05)
    c = pal[rng.integers(len(pal))]; k = rng.uniform(.12, .38)
    d.ellipse([x - r, y - r, x + r, y + r], fill=tuple(int(v * k) for v in c))
bok = np.asarray(bok.filter(ImageFilter.GaussianBlur(W * .006))).astype(np.float32) / 255
bg = a + (haze + bok * .8) * (1 - m[..., None])
# viñeta
d2 = np.sqrt(((xx - W * .5) / (W * .68)) ** 2 + ((yy - H * .48) / (H * .62)) ** 2)
vig = np.clip(1 - (d2 - .5) * .95, .2, 1)[..., None]
save(bg * vig, "capa_fondo.png")

# ---------- semáforo recortado (con la misma viñeta)
fg = np.dstack([np.clip(a * vig, 0, 1), m])
save(fg, "capa_frente.png", "RGBA")

# ---------- grano
g = np.clip(.5 + np.random.default_rng(21).normal(0, .07, (H, W)), 0, 1)
Image.fromarray((g * 255).astype(np.uint8), "L").convert("RGB").save(os.path.join(outdir, "capa_grano.png"))
print("OK", outdir)
