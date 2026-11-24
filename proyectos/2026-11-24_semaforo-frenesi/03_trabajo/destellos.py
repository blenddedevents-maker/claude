"""Destellos de estrella de 4 puntas (estilo logo Blendded) sobre los brillos del cromo.
Uso: python3 destellos.py <entrada.png> <salida.png> x1,y1,s1 x2,y2,s2 ...   (x,y en 0-1; s = tamaño relativo)
"""
import sys
import numpy as np
from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
pts = [tuple(float(v) for v in p.split(",")) for p in sys.argv[3:]]
im = Image.open(src).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(np.float32) / 255
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)

for (px, py, s) in pts:
    cx, cy, R = px * W, py * H, s * W
    dx, dy = np.abs(xx - cx), np.abs(yy - cy)
    # estrella: rayos horizontal y vertical muy finos + núcleo + halo violeta
    ray_h = np.exp(-(dy / (R * .012)) ** 2) * np.clip(1 - dx / R, 0, 1) ** 2.2
    ray_v = np.exp(-(dx / (R * .012)) ** 2) * np.clip(1 - dy / (R * .8), 0, 1) ** 2.2
    d = np.sqrt(dx ** 2 + dy ** 2)
    core = np.exp(-(d / (R * .035)) ** 2)
    halo = np.exp(-(d / (R * .22)) ** 2)
    white = np.clip(ray_h + ray_v + core * 1.5, 0, 1.5)[..., None]
    purple = (halo * .55 + (ray_h + ray_v) * .35)[..., None] * np.array([.62, .25, 1.0])
    add = white * np.array([1, 1, 1]) + purple
    a = 1 - (1 - a) * (1 - np.clip(add, 0, 1))

Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).save(dst)
print("OK", dst)
