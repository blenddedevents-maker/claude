"""Retoque del render: halo de luces (bloom), gradación tipo flash nocturno, viñeta y grano.
Uso: python3 postpro.py <entrada.png> <salida.png>
"""
import sys
import numpy as np
from PIL import Image, ImageFilter

src, dst = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(np.float32) / 255.0

# --- bloom: solo zonas muy brillantes y saturadas (las luces)
lum = a.max(axis=2)
sat = lum - a.min(axis=2)
mask = np.clip((lum - 0.72) / 0.28, 0, 1) * np.clip(sat * 2.2, 0, 1)
hi = (a * mask[..., None] * 255).astype(np.uint8)
hi_im = Image.fromarray(hi)
bloom = np.zeros_like(a)
for r, w in ((W * 0.006, 0.9), (W * 0.025, 0.75), (W * 0.07, 0.55)):
    bloom += np.asarray(hi_im.filter(ImageFilter.GaussianBlur(r))).astype(np.float32) / 255.0 * w
a = 1 - (1 - a) * (1 - np.clip(bloom, 0, 1))  # screen

# --- gradación: negros profundos, sombras hacia azul/violeta, contraste
def curve(x, lift=-0.03, gamma=1.12):
    return np.clip((x + lift) / (1 + lift), 0, 1) ** gamma
a = curve(a)
lum = a.mean(axis=2, keepdims=True)
shadow = np.clip(1 - lum * 2.2, 0, 1)
a = a + shadow * np.array([0.010, -0.004, 0.035]) * 1.0
# saturación suave
g = a.mean(axis=2, keepdims=True)
a = g + (a - g) * 1.18

# --- viñeta
yy, xx = np.mgrid[0:H, 0:W]
d = np.sqrt(((xx - W * 0.5) / (W * 0.62)) ** 2 + ((yy - H * 0.47) / (H * 0.6)) ** 2)
vig = np.clip(1 - (d - 0.55) * 0.9, 0.25, 1)
a = a * vig[..., None]

# --- grano de película
rng = np.random.default_rng(21)
grain = rng.normal(0, 0.028, (H, W, 1)).astype(np.float32)
a = a + grain * (0.6 + 0.4 * (1 - a.mean(axis=2, keepdims=True)))

Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).save(dst)
print("OK", dst)
