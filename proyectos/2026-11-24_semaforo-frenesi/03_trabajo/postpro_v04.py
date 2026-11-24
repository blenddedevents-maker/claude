"""v04 — Revelado tipo foto con flash directo (como la referencia del teléfono).
Uso: python3 postpro_v04.py <render.png> <salida.png>
"""
import sys
import numpy as np
from PIL import Image, ImageFilter

src, dst = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(np.float32) / 255

def to_im(x): return Image.fromarray((np.clip(x, 0, 1) * 255).astype(np.uint8))
def from_im(i): return np.asarray(i).astype(np.float32) / 255

# 1) contraste local (claridad) y nitidez: textura de la chapa y rayones
blur_big = from_im(to_im(a).filter(ImageFilter.GaussianBlur(W * .012)))
a = np.clip(a + (a - blur_big) * .45, 0, 1)
a = from_im(to_im(a).filter(ImageFilter.UnsharpMask(radius=1.6, percent=70, threshold=2)))

# 2) caída del flash: centro (algo arriba-izquierda) iluminado, bordes a negro
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
d = np.sqrt(((xx - W * .45) / (W * .75)) ** 2 + ((yy - H * .42) / (H * .7)) ** 2)
fall = np.clip(1.08 - d ** 2 * .95, .12, 1.08)[..., None]
a = a * fall

# 3) curva: negros aplastados, altas luces suaves
a = np.clip((a - .02) / .98, 0, 1)
a = a ** 1.08
a = 1 - (1 - a) ** 1.04

# 4) color: sombras frías azuladas (como la referencia), luces neutras-cálidas
lum = a.mean(axis=2, keepdims=True)
sh = np.clip(1 - lum * 2.4, 0, 1); hi = np.clip((lum - .55) * 2, 0, 1)
a = a + sh * np.array([-.006, .004, .03]) + hi * np.array([.02, .008, -.012])
g = a.mean(axis=2, keepdims=True)
a = g + (a - g) * 1.22

# 5) halo de las luces del semáforo
mx = a.max(axis=2); sat = mx - a.min(axis=2)
hm = np.clip((mx - .6) / .4, 0, 1) * np.clip(sat * 2.5, 0, 1)
hl = to_im(a * hm[..., None])
glow = sum(from_im(hl.filter(ImageFilter.GaussianBlur(r))) * w
           for r, w in ((W * .004, .5), (W * .016, .5), (W * .045, .35)))
a = 1 - (1 - a) * (1 - np.clip(glow, 0, 1))

# 6) aberración cromática leve en los bordes
def radial_shift(ch, k):
    i = Image.fromarray((np.clip(ch, 0, 1) * 255).astype(np.uint8), "L")
    s = 1 + k
    i2 = i.resize((int(W * s), int(H * s)), Image.BICUBIC)
    l, t = (i2.width - W) // 2, (i2.height - H) // 2
    return np.asarray(i2.crop((l, t, l + W, t + H))).astype(np.float32) / 255
a = np.dstack([radial_shift(a[..., 0], .0018), a[..., 1], radial_shift(a[..., 2], -.0012)])

# 7) grano de película (algo grueso, más en sombras)
rng = np.random.default_rng(4)
n = rng.normal(0, 1, (H, W)).astype(np.float32)
n = from_im(Image.fromarray(((n * .18 + .5).clip(0, 1) * 255).astype(np.uint8), "L").filter(ImageFilter.GaussianBlur(.7)))
n = (n - .5) * 2
lum = a.mean(axis=2, keepdims=True)
a = a + n[..., None] * (.035 + .03 * (1 - lum))

to_im(a).save(dst)
print("OK", dst)
