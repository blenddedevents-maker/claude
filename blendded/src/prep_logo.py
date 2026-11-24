"""Rasterise the vector logo and build the shader texture.
R = anti-aliased coverage, G = inner bevel height, B = outer distance (glow/halo)."""
import io, sys, numpy as np, cv2, cairosvg
from PIL import Image
svg = open(sys.argv[1], 'rb').read()
TW, TH, LOGO_W = 4096, 1024, 3600            # texture size, logo width inside texture
SS = 2                                       # supersample factor
png = cairosvg.svg2png(bytestring=svg, output_width=LOGO_W * SS)
a = np.array(Image.open(io.BytesIO(png)).convert('RGBA'))[..., 3].astype(np.float32) / 255
H, W = TH * SS, TW * SS
canvas = np.zeros((H, W), np.float32)
y0, x0 = (H - a.shape[0]) // 2, (W - a.shape[1]) // 2
canvas[y0:y0 + a.shape[0], x0:x0 + a.shape[1]] = a
b = (canvas > 0.5).astype(np.uint8)
din = cv2.distanceTransform(b, cv2.DIST_L2, 5) / SS          # px in texture space
dout = cv2.distanceTransform(1 - b, cv2.DIST_L2, 5) / SS
cov = cv2.resize(canvas, (TW, TH), interpolation=cv2.INTER_AREA)
din = cv2.resize(din, (TW, TH), interpolation=cv2.INTER_AREA)
dout = cv2.resize(dout, (TW, TH), interpolation=cv2.INTER_AREA)
BEVEL = 14.0
h = np.clip(din / BEVEL, 0, 1); h = 1 - (1 - h) ** 2          # rounded bevel profile
h = cv2.GaussianBlur(h, (0, 0), 1.2)
glow = np.clip(dout / 260.0, 0, 1) ** 0.5
out = np.stack([cov, h, glow], -1)
Image.fromarray((out * 255 + 0.5).clip(0, 255).astype(np.uint8)).save(sys.argv[2])
# logo aspect inside texture (for shader mapping)
print('logo px in tex:', a.shape[1] / SS, a.shape[0] / SS)
