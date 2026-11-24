"""Versión animada del cartel (MP4 vertical 1080x1920 para stories).

Uso:  python3 animar.py foto.jpg cartel.mp4
Los textos se cambian en CONFIG dentro de cartel.py.
"""
import sys, subprocess
import numpy as np
from PIL import Image
import cartel
from cartel import W, H, motion_blur

FPS = 30
DUR = 8.0


def ease(x):
    x = np.clip(x, 0, 1)
    return 1 - (1 - x) ** 3


def ramp(t, t0, d):
    return float(ease((t - t0) / d))


def main(src, out):
    data = {}
    cartel.build(src, "cartel.png", collect=data)  # también regenera el cartel fijo
    bg = data["bg"].astype(np.float32)
    bg_blur = motion_blur(bg, 90)
    rng = np.random.default_rng(3)

    layers = {}
    for name, m, col in data["layers"]:
        layers.setdefault(name, []).append((m.astype(np.float32), col))

    # máscaras por fila para que las fechas entren una a una
    rows, step = data["rows"], data["step"]
    yy = np.arange(H)[:, None]
    bands = []
    for i, r in enumerate(rows):
        h = step * 1.5 if i == 0 else step
        bands.append(((yy >= r - 12) & (yy < r + h)).astype(np.float32))

    grains = [rng.normal(0, 0.06, (H, W, 1)).astype(np.float32) +
              rng.normal(0, 0.02, (H, W, 3)).astype(np.float32) for _ in range(6)]
    scan = (1 - 0.025 * (np.arange(H) % 3 == 0)).astype(np.float32)[:, None, None]

    # momentos de glitch (aleatorios pero fijos)
    glitch_times = [0.95, 2.25, 3.6, 4.9, 6.1, 7.3]

    def zoom(a, z, dx=0):
        im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
        w, h = int(W * z), int(H * z)
        im = im.resize((w, h), Image.BILINEAR)
        x0 = (w - W) // 2 + dx
        y0 = (h - H) // 2
        return np.asarray(im.crop((x0, y0, x0 + W, y0 + H)), np.float32) / 255

    def over(c, m, col):
        m = m[..., None]
        return c * (1 - m) + col * m

    n = int(FPS * DUR)
    ff = subprocess.Popen([
        "ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium",
        "-movflags", "+faststart", out], stdin=subprocess.PIPE)

    for f in range(n):
        t = f / FPS
        # glitch activo?
        g = any(0 <= t - gt < 0.12 for gt in glitch_times)

        # fondo: entra desde un barrido de movimiento y hace un zoom lento
        intro = ramp(t, 0, 1.2)
        z = 1.10 - 0.07 * ease(t / DUR)
        drift = int(18 * np.sin(t * 0.9))
        base = bg * intro + bg_blur * (1 - intro)
        c = zoom(base, z, drift)
        c = c * (0.15 + 0.85 * ramp(t, 0, 0.6))

        # respiración del smear: pulso suave de desenfoque horizontal
        pulse = 0.5 + 0.5 * np.sin(t * 2.2)
        if pulse > 0.85 or g:
            k = 14 if not g else 40
            c = c * 0.6 + motion_blur(c, k) * 0.4

        # logo fantasma gigante
        a = ramp(t, 0.3, 1.4)
        for m, col in layers["ghost"]:
            sh = int(120 * (1 - a) + 14 * np.sin(t * 1.3))
            c = over(c, np.roll(m, sh, axis=1) * a * (0.85 + 0.15 * np.sin(t * 3)), col)

        # fechas, una a una con estela
        for i, band in enumerate(bands):
            t0 = 1.0 + i * 0.28
            a = ramp(t, t0, 0.45)
            if a <= 0:
                continue
            sh = int(-90 * (1 - a))
            for m, col in layers["dates"]:
                mm = np.roll(m * band, sh, axis=1)
                if a < 1:
                    mm = np.maximum(mm, motion_blur(mm, 40) * (1 - a) * 1.5)
                c = over(c, mm * a, col)

        # logo y TOUR con parpadeo glitch al entrar
        for name, t0 in (("logo", 2.4), ("tour", 2.6)):
            a = ramp(t, t0, 0.5)
            if a <= 0:
                continue
            flick = 1.0 if t > t0 + 0.45 else float(rng.random() > 0.35)
            for m, col in layers[name]:
                jit = int(rng.integers(-25, 25)) if (t < t0 + 0.45 or g) else 0
                c = over(c, np.roll(m, jit, axis=1) * a * flick, col)

        for name, t0 in (("pie", 3.2), ("small", 3.5), ("badge", 3.7)):
            a = ramp(t, t0, 0.6)
            if a > 0:
                for m, col in layers[name]:
                    c = over(c, np.roll(m, int(60 * (1 - a)), axis=1) * a, col)

        # glitch: franjas desplazadas + separación RGB fuerte
        if g:
            for _ in range(int(rng.integers(4, 9))):
                y0 = int(rng.integers(0, H - 40))
                hh = int(rng.integers(8, 90))
                c[y0:y0 + hh] = np.roll(c[y0:y0 + hh], int(rng.integers(-80, 80)), axis=1)
            s = int(rng.integers(12, 26))
            c = np.stack([np.roll(c[..., 0], s, 1), c[..., 1], np.roll(c[..., 2], -s, 1)], -1)

        c = c + grains[f % len(grains)]
        c = c * scan
        # fundido a negro final para que el loop corte limpio
        c = c * (1 - ramp(t, DUR - 0.35, 0.35) * 0.9)
        ff.stdin.write((np.clip(c, 0, 1) * 255).astype(np.uint8).tobytes())
        if f % 30 == 0:
            print(f"frame {f}/{n}", flush=True)

    ff.stdin.close()
    ff.wait()
    print("guardado", out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "cartel.mp4")
