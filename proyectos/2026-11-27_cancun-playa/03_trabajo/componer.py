"""Composición: persona recortada sobre playa de Cancún (v01)."""
import sys
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

ver = sys.argv[1] if len(sys.argv) > 1 else "v01"
per = Image.open("02_assets/generados/persona-recortada.png").convert("RGBA")
W, H = per.size  # 1932x2576 (3:4 vertical)

# --- Fondo: recorte vertical 3:4 de la playa, con zona hotelera visible
bg = Image.open("01_referencias/visual/fondo-cancun-playa_wikimedia.jpg").convert("RGB")
bw, bh = bg.size
cw = int(bh * 3 / 4)
x0 = bw - cw - 60
bg = bg.crop((x0, 0, x0 + cw, bh)).resize((W, H), Image.LANCZOS)
bg = bg.filter(ImageFilter.GaussianBlur(4))          # profundidad tipo selfie
bg = ImageEnhance.Color(bg).enhance(1.05)

# --- Persona: de luz nocturna cálida a luz de día
rgb = np.asarray(per.convert("RGB")).astype(np.float32) / 255.0
a = np.asarray(per.split()[-1]).astype(np.float32) / 255.0
lin = rgb ** 2.2
lin *= 1.38                                            # exposición
lin *= np.array([1.0, 0.99, 1.04])                     # balance de blancos más frío
lin = np.clip(lin, 0, 1)
out = lin ** (1 / 2.2)
out = 0.5 + (out - 0.5) * 1.06                         # algo de contraste
# luz de cielo azulada suave en sombras
out = out + (1 - out) * np.array([0.0, 0.015, 0.04]) * (1 - out.mean(2, keepdims=True))
out = np.clip(out, 0, 1)

# bordes: suavizar alfa y "light wrap" con el color del fondo
alpha = Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
a2 = np.asarray(alpha).astype(np.float32) / 255.0
bgarr = np.asarray(bg).astype(np.float32) / 255.0
wrap = np.asarray(Image.fromarray((a2 * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(14))).astype(np.float32) / 255.0
edge = np.clip(a2 - wrap, 0, 1)[..., None] * 1.6
blurbg = np.asarray(bg.filter(ImageFilter.GaussianBlur(25))).astype(np.float32) / 255.0
out = out * (1 - edge * 0.35) + blurbg * edge * 0.35

comp = out * a2[..., None] + bgarr * (1 - a2[..., None])
# grano ligero unificador
rng = np.random.default_rng(1)
comp = np.clip(comp + rng.normal(0, 0.012, comp.shape), 0, 1)
res = Image.fromarray((comp * 255).astype(np.uint8))
dst = f"04_salidas/borradores/yo-en-cancun_{ver}.jpg"
res.save(dst, quality=92)
print(dst, res.size)
