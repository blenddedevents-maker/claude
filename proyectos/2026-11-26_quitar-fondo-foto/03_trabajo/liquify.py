import sys, numpy as np, cv2
from PIL import Image
src, dst, s = sys.argv[1], sys.argv[2], float(sys.argv[3])
im = np.array(Image.open(src)).astype(np.float32)
H, W = im.shape[:2]
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
dx = np.zeros_like(xx); dy = np.zeros_like(yy)
tgt = np.array([495., 195.])  # centro de la cara
# (cx, cy, fuerza px, sigma)
for cx, cy, st, sg in [(530,232,5.5*s,20),(510,244,3.5*s,16),(462,224,2.5*s,16)]:
    v = tgt - [cx, cy]; v /= np.linalg.norm(v)
    w = np.exp(-((xx-cx)**2 + (yy-cy)**2) / (2*sg*sg))
    dx += w*st*v[0]; dy += w*st*v[1]
# push: muestrear desde p - d
out = np.stack([cv2.remap(im[...,c], xx-dx, yy-dy, cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT) for c in range(im.shape[2])], -1)
Image.fromarray(np.clip(out,0,255).astype(np.uint8)).save(dst)
