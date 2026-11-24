"""Genera un cartel estilo 'tour' (blur, glitch, tonos morados) a partir de una foto.

Uso:  python3 cartel.py foto.jpg salida.png
Edita los textos de CONFIG para poner tu nombre, fechas y salas.
"""
import sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
F = lambda n: os.path.join(HERE, "fonts", n)

# ----------------------------- CONFIG -----------------------------
NOMBRE = ("TU", "NOMBRE")          # se dibuja en dos líneas solapadas
TOUR = ("TOUR", "2027")
TITULO_FONDO = ("PRÓXIMAS", "FECHAS")
MES_1, FECHAS_1 = "DICIEMBRE", [
    ("05/12", "SALA APOLO, BARCELONA", True),
    ("06/12", "LA RIVIERA, MADRID", False),
    ("12/12", "SALA MOON, VALENCIA", True),
    ("13/12", "INDUSTRIAL COPERA, GRANADA", False),
    ("19/12", "SALA X, SEVILLA", True),
    ("20/12", "TBA", False),
    ("27/12", "RAZZMATAZZ, BARCELONA", True),
]
MES_2, FECHAS_2 = "ENERO", [
    ("09/01", "SALA CAPITOL, SANTIAGO", False),
    ("10/01", "KAFE ANTZOKIA, BILBAO", True),
    ("16/01", "SALA LA RAQUETA, MURCIA", False),
    ("17/01", "LA PEREZA, ZARAGOZA", True),
    ("23/01", "TBA", False),
    ("30/01", "SALA BUT, MADRID", True),
    ("31/01", "SALA APOLO, BARCELONA", True),
]
PIE = "más fechas por confirmar"
LETRA_PEQUENA = ("ESTO SOLO ES EL PRINCIPIO · CADA NOCHE UNA HISTORIA DISTINTA · "
                 "NOS VEMOS DELANTE DEL ESCENARIO · GRACIAS POR ESTAR AQUÍ DESDE EL PRIMER DÍA")
# -------------------------------------------------------------------

W, H = 1080, 1920
SS = 2  # supersampling del texto


def font(name, size, var=None):
    f = ImageFont.truetype(F(name), size)
    if var:
        try:
            f.set_variation_by_name(var)
        except Exception:
            pass
    return f


def motion_blur(img, k, axis=1):
    """Desenfoque de movimiento horizontal (box blur 1D) sobre array float."""
    a = img.astype(np.float32)
    pad = [(0, 0)] * a.ndim
    pad[axis] = (k, k)
    p = np.pad(a, pad, mode="edge")
    c = np.cumsum(p, axis=axis)
    n = a.shape[axis]
    hi = np.take(c, np.arange(2 * k, 2 * k + n), axis=axis)
    lo = np.take(c, np.arange(0, n), axis=axis)
    return (hi - lo) / (2 * k)


def screen(a, b):
    return 1 - (1 - a) * (1 - b)


def smooth(x, e0, e1):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def build(src, out):
    rng = np.random.default_rng(7)
    im = Image.open(src).convert("RGB")
    sw, sh = im.size
    # recorta el borde blanco superior de la foto (fondo de estudio empieza ~17%)
    top = int(sh * 0.205)
    im = im.crop((0, top, sw, sh))
    scale = W / im.width
    im = im.resize((W, int(im.height * scale)), Image.LANCZOS)
    y0 = H - im.height

    # lienzo base: degradado gris claro tipo pared de estudio
    yy = np.linspace(0, 1, H)[:, None, None]
    base = np.ones((H, W, 3), np.float32) * (0.86 - 0.05 * yy)
    photo = np.asarray(im, np.float32) / 255
    base[y0:] = photo
    # fundido suave entre la foto y la parte superior
    fade = 120
    a = np.linspace(0, 1, fade)[:, None, None]
    base[y0:y0 + fade] = base[y0 - 1] * (1 - a) + photo[:fade] * a

    img = base
    X = np.linspace(0, 1, W)[None, :]
    Y = np.linspace(0, 1, H)[:, None]

    # ---------- smear / motion blur (sobre todo en cabeza y torso) ----------
    strong = motion_blur(img, 60)
    mid = motion_blur(img, 22)
    band = (np.exp(-((Y - 0.38) / 0.10) ** 2) * 0.95 +
            np.exp(-((Y - 0.62) / 0.06) ** 2) * 0.55)
    band = band * (0.55 + 0.45 * np.exp(-((X - 0.55) / 0.35) ** 2))
    band = np.clip(band, 0, 1)[..., None]
    img = img * (1 - band) + (strong * 0.6 + mid * 0.4) * band
    # fantasma desplazado (doble exposición)
    ghost = np.roll(motion_blur(img, 30), 70, axis=1)
    gm = (np.exp(-((Y - 0.36) / 0.12) ** 2) * 0.35)[..., None]
    img = img * (1 - gm) + screen(img, ghost * 0.9) * gm

    # ---------- separación RGB ----------
    r = np.roll(img[..., 0], 9, axis=1)
    b = np.roll(img[..., 2], -9, axis=1)
    img = np.stack([r, img[..., 1], b], -1)

    # ---------- etalonaje: sombras moradas, luces frías ----------
    lum = img @ np.array([0.299, 0.587, 0.114], np.float32)
    img = img * 0.55 + lum[..., None] * 0.45  # desaturar
    shadow = np.array([0.16, 0.06, 0.24], np.float32)
    light = np.array([0.93, 0.95, 0.97], np.float32)
    l = np.clip(lum, 0, 1)[..., None]
    graded = shadow * (1 - l) ** 1.4 + light * l ** 0.9
    img = img * 0.35 + graded * 0.65
    img = (img - 0.5) * 1.25 + 0.5
    img = np.clip(img, 0, 1) ** 1.35  # más oscuro y denso
    # sombra morada que sube desde abajo y desde la derecha
    dark = np.array([0.10, 0.04, 0.16], np.float32)
    dm = (smooth(Y, 0.45, 1.0) * 0.75 + smooth(X, 0.55, 1.0) * smooth(Y, 0.3, 0.7) * 0.35)
    dm = np.clip(dm, 0, 0.85)[..., None]
    img = img * (1 - dm) + dark * dm

    # ---------- luces moradas / cian (light leaks) ----------
    def blob(cx, cy, rx, ry):
        return np.exp(-(((X - cx) / rx) ** 2 + ((Y - cy) / ry) ** 2))[..., None]
    purple = np.array([0.62, 0.30, 0.95], np.float32)
    lilac = np.array([0.80, 0.62, 1.0], np.float32)
    cyan = np.array([0.55, 0.85, 0.88], np.float32)
    img = screen(img, purple * blob(0.92, 0.40, 0.22, 0.14) * 0.75)
    img = screen(img, purple * blob(0.45, 0.78, 0.35, 0.12) * 0.8)
    img = screen(img, purple * blob(0.75, 0.58, 0.18, 0.10) * 0.5)
    img = screen(img, lilac * blob(0.15, 0.06, 0.45, 0.10) * 0.55)
    img = screen(img, cyan * blob(0.0, 0.25, 0.20, 0.25) * 0.35)
    img = screen(img, lilac * blob(1.0, 0.95, 0.25, 0.10) * 0.45)
    # oscurecer bordes
    vig = 1 - 0.35 * np.clip(((X - 0.5) ** 2 * 1.4 + (Y - 0.55) ** 2 * 0.9), 0, 1) ** 0.8
    img = img * vig[..., None]
    img = np.clip(img, 0, 1)

    canvas = Image.fromarray((img * 255).astype(np.uint8))

    # ---------- textos ----------
    def text_layer():
        return Image.new("L", (W * SS, H * SS), 0)

    def comp(layer_L, color, opacity=1.0, smear=0, smear_amt=0.0, shift=0):
        """Pega una capa de texto con color; opcionalmente con estela horizontal."""
        nonlocal canvas
        m = layer_L.resize((W, H), Image.LANCZOS)
        ma = np.asarray(m, np.float32) / 255
        if shift:
            ma = np.roll(ma, shift, axis=1)
        if smear:
            tail = motion_blur(ma, smear)
            tail = np.roll(tail, smear // 2, axis=1)
            ma = np.maximum(ma, tail * smear_amt)
        ma = (ma * opacity)[..., None]
        c = np.asarray(canvas, np.float32) / 255
        col = np.array(color, np.float32) / 255
        c = c * (1 - ma) + col * ma
        canvas = Image.fromarray((np.clip(c, 0, 1) * 255).astype(np.uint8))

    # título fantasma gigante al fondo
    L = text_layer(); d = ImageDraw.Draw(L)
    ft = font("Playfair.ttf", 300 * SS, "Black")
    d.text((-30 * SS, -60 * SS), TITULO_FONDO[0], font=ft, fill=255)
    d.text((140 * SS, 170 * SS), TITULO_FONDO[1], font=ft, fill=255)
    L = L.filter(ImageFilter.GaussianBlur(4 * SS))
    comp(L, (200, 180, 235), 0.42, smear=40, smear_amt=0.6)

    # listado de fechas
    fm = font("Playfair.ttf", 38 * SS, "Black")
    fd = font("Oswald.ttf", 23 * SS, "Medium")
    colx = [80, 560]
    ytop = 150
    step = 36
    L = text_layer(); d = ImageDraw.Draw(L)
    Lhi = text_layer(); dh = ImageDraw.Draw(Lhi)
    for cx, mes, fechas in ((colx[0], MES_1, FECHAS_1), (colx[1], MES_2, FECHAS_2)):
        d.text((cx * SS, ytop * SS), mes, font=fm, fill=255)
        for i, (dia, sala, hot) in enumerate(fechas):
            y = (ytop + 56 + i * step) * SS
            d.text((cx * SS, y), dia, font=fd, fill=255)
            d.text(((cx + 68) * SS, y), sala, font=fd, fill=255)
            if hot:  # marcador: pequeño círculo con ★ (sold out / pocas entradas)
                tw = d.textlength(sala, font=fd)
                ox = (cx + 68) * SS + tw + 12 * SS
                dh.ellipse((ox, y + 6 * SS, ox + 22 * SS, y + 28 * SS), outline=255, width=3 * SS)
                dh.ellipse((ox + 7 * SS, y + 13 * SS, ox + 15 * SS, y + 21 * SS), fill=255)
    comp(L, (40, 30, 55), 0.92, smear=26, smear_amt=0.55)
    comp(Lhi, (95, 70, 120), 0.85, smear=10, smear_amt=0.4)

    # nombre (izq) y tour (der), dos líneas solapadas
    fn = font("Playfair.ttf", 54 * SS, "Black")
    for txt, x, align in ((NOMBRE, 50, "l"), (TOUR, 1030, "r")):
        L = text_layer(); d = ImageDraw.Draw(L)
        for j, t in enumerate(txt):
            tw = d.textlength(t, font=fn)
            px = x * SS if align == "l" else x * SS - tw
            d.text((px, (1000 + j * 30) * SS), t, font=fn, fill=255)
        comp(L, (20, 14, 26), 0.95)
        comp(L, (150, 90, 210), 0.35, shift=5)

    # pie: "más fechas por confirmar"
    L = text_layer(); d = ImageDraw.Draw(L)
    fp = font("Oswald.ttf", 30 * SS, "Light")
    tw = d.textlength(PIE, font=fp)
    d.text(((W * SS - tw) / 2, 1560 * SS), PIE, font=fp, fill=255)
    comp(L, (238, 234, 246), 0.9, smear=40, smear_amt=0.5)

    # letra pequeña espaciada
    L = text_layer(); d = ImageDraw.Draw(L)
    fs = font("Oswald.ttf", 11 * SS, "Regular")
    words = LETRA_PEQUENA.split(" ")
    lines, cur = [], ""
    for w_ in words:
        if len(cur) + len(w_) > 70:
            lines.append(cur); cur = w_
        else:
            cur = (cur + " " + w_).strip()
    lines.append(cur)
    for i, ln in enumerate(lines):
        spaced = " ".join(ln)
        tw = d.textlength(spaced, font=fs)
        d.text(((W * SS - tw) / 2, (1670 + i * 18) * SS), spaced, font=fs, fill=255)
    comp(L, (235, 230, 245), 0.75, smear=12, smear_amt=0.4)

    # sello abajo a la derecha
    L = text_layer(); d = ImageDraw.Draw(L)
    bx, by = 950 * SS, 1745 * SS
    d.rectangle((bx, by, bx + 70 * SS, by + 84 * SS), outline=255, width=3 * SS)
    d.rectangle((bx + 6 * SS, by + 6 * SS, bx + 64 * SS, by + 20 * SS), fill=255)
    fb = font("Playfair.ttf", 50 * SS, "Black")
    tw = d.textlength(NOMBRE[0][0], font=fb)
    d.text((bx + 35 * SS - tw / 2, by + 16 * SS), NOMBRE[0][0], font=fb, fill=255)
    comp(L, (245, 242, 250), 0.9)

    # ---------- grano + scanlines suaves ----------
    c = np.asarray(canvas, np.float32) / 255
    g = rng.normal(0, 0.055, (H, W, 1)).astype(np.float32)
    g = g + rng.normal(0, 0.02, (H, W, 3)).astype(np.float32)
    c = c + g
    c *= (1 - 0.025 * (np.arange(H) % 3 == 0))[:, None, None]
    c = np.clip(c, 0, 1)
    Image.fromarray((c * 255).astype(np.uint8)).save(out, quality=95)
    print("guardado", out)


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "cartel.png")
