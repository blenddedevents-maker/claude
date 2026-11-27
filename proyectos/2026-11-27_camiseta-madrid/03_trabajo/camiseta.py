"""Sudadera negra -> camiseta blanca estilo Madrid."""
import sys
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
ver = sys.argv[1] if len(sys.argv) > 1 else "v01"
im = np.asarray(Image.open('02_assets/generados/selfie-derecho.png')).astype(np.float32) / 255
m = np.asarray(Image.open('02_assets/generados/mascara-ropa.png')) > 127
H, W = m.shape
lum = im.mean(2)
# sombreado: pliegues de la tela, sin logos ni ruido
l = lum.copy(); l[~m] = np.median(lum[m])
l = np.minimum(l, np.percentile(lum[m], 55))          # elimina letras/parches blancos
l = ndimage.median_filter(l, size=41)
l = ndimage.gaussian_filter(l, 10)
p2, p98 = np.percentile(l[m], [2, 98])
s = np.clip((l - p2) / (p98 - p2), 0, 1)
# caída de luz: arriba (más cerca de la luz) más claro, hacia abajo-izquierda más oscuro
yy, xx = np.mgrid[0:H, 0:W] / np.array([H, W])[:, None, None]
grad = 1.0 - 0.22 * (yy - 0.55) / 0.45 - 0.10 * (0.5 - xx)
shade = (0.68 + 0.32 * s) * grad
# volumen: oscurecer hacia la silueta
dist0 = ndimage.distance_transform_edt(m)
shade = shade * (0.80 + 0.20 * np.clip(dist0 / (0.06 * W), 0, 1))
# pliegues con más contraste (paso medio de la luminancia original)
lc = ndimage.median_filter(np.minimum(lum, np.percentile(lum[m], 55)), size=15)
detail = ndimage.gaussian_filter(lc, 4) - ndimage.gaussian_filter(lc, 30)
detail = np.clip(detail, -0.04, 0.04)
shade = shade * (1 + 2.5 * detail * m)
# textura de malla deportiva
mesh = (np.sin(xx * W * 0.9) * np.sin(yy * H * 0.9))
shade = shade * (1 + 0.025 * mesh)
white = np.array([0.93, 0.92, 0.88])                  # blanco bajo luz cálida nocturna
shirt = white * shade[..., None]
# cuello: banda azul marino siguiendo el borde superior de la máscara
dist = ndimage.distance_transform_edt(m)
top = np.zeros_like(m); 
cols = np.where(m.any(0))[0]
first = np.argmax(m, axis=0)
for x in cols: top[first[x]:first[x] + 1, x] = True
dtop = ndimage.distance_transform_edt(~top)
neck_zone = (yy < 0.76) & (xx > 0.25) & (xx < 0.53)
collar = m & neck_zone & (dtop < 0.018 * H)
gold = m & neck_zone & (dtop >= 0.018 * H) & (dtop < 0.022 * H)
navy = np.array([0.10, 0.12, 0.25]) * (0.6 + 0.4 * shade[..., None])
goldc = np.array([0.75, 0.62, 0.30]) * (0.6 + 0.4 * shade[..., None])
shirt = np.where(collar[..., None], navy, shirt)
shirt = np.where(gold[..., None], goldc, shirt)
# grano para casar con la foto
rng = np.random.default_rng(2)
shirt = np.clip(shirt + rng.normal(0, 0.018, shirt.shape), 0, 1)
a = ndimage.gaussian_filter(m.astype(np.float32), 2.0)[..., None]
out = shirt * a + im * (1 - a)
dst = f'04_salidas/borradores/camiseta-madrid_{ver}.jpg'
Image.fromarray((out * 255).astype(np.uint8)).save(dst, quality=92)
print(dst)
