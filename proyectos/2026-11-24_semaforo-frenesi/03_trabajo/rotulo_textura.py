"""Textura del rótulo pintado en la persiana: 'FIESTA DEL' / 'SEMÁFORO' con chorreones.
Salida: PNG en escala de grises (blanco = pintura). Cubre un rectángulo de 2.4 x 1.2 m en la escena.
Uso: python3 rotulo_textura.py <salida.png>
"""
import sys, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

out = sys.argv[1]
W, H = 4096, 2048
FONT = "../02_assets/generados/fuentes/anton-latin-400-normal.ttf"
im = Image.new("L", (W, H), 0)
d = ImageDraw.Draw(im)

def centered(text, size, y, spacing=0):
    f = ImageFont.truetype(FONT, size)
    widths = [d.textlength(c, font=f) for c in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x = (W - total) / 2
    for c, w in zip(text, widths):
        d.text((x, y), c, fill=255, font=f)
        x += w + spacing
    return f

# "FIESTA" y "DEL" a los lados: en medio queda el semáforo
f1 = ImageFont.truetype(FONT, 300)
def spaced(text, x, y, spacing, align="left"):
    widths = [d.textlength(c, font=f1) for c in text]
    total = sum(widths) + spacing * (len(text) - 1)
    if align == "right": x -= total
    for c, w in zip(text, widths):
        d.text((x, y), c, fill=255, font=f1); x += w + spacing
spaced("FIESTA", 1430, 90, 40, "right")
spaced("DEL", 2900, 90, 40)
centered("SEMÁFORO", 1010, 420, spacing=18)

# chorreones de pintura desde la base de las letras grandes
a = np.asarray(im)
rnd = random.Random(7)
for _ in range(26):
    x = rnd.randint(300, W - 300)
    col = np.where(a[:, x] > 128)[0]
    col = col[col > 900]
    if len(col) == 0:
        continue
    y0 = col.max()
    ln = rnd.randint(40, 260); w = rnd.randint(9, 18)
    d.rounded_rectangle([x - w / 2, y0 - 10, x + w / 2, y0 + ln], radius=w / 2, fill=255)
    d.ellipse([x - w * .75, y0 + ln - w, x + w * .75, y0 + ln + w * .5], fill=255)

im = im.filter(ImageFilter.GaussianBlur(1.2))
im.save(out)
print("OK", out)
