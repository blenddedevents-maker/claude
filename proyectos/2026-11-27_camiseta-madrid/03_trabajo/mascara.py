import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
im=np.asarray(Image.open('02_assets/generados/selfie-derecho.png')).astype(np.float32)/255
al=np.asarray(Image.open('02_assets/generados/persona-recortada.png').split()[-1]).astype(np.float32)/255
H,W=al.shape
lum=im.mean(2); sat=im.max(2)-im.min(2)
yy=np.arange(H)[:,None]*np.ones((1,W))
m=(al>0.5)&(lum<0.27)&(sat<0.11)&(yy>0.52*H)
m=ndimage.binary_opening(m,iterations=3)
lab,n=ndimage.label(m); sizes=ndimage.sum(m,lab,range(1,n+1))
m=np.isin(lab,1+np.where(sizes>0.02*m.sum())[0])
m=ndimage.binary_closing(m,iterations=16); m=ndimage.binary_fill_holes(m)
m=m&(al>0.85)
Image.fromarray((m*255).astype(np.uint8)).save('02_assets/generados/mascara-ropa.png')
ov=im.copy(); ov[m]=ov[m]*0.5+np.array([1,0,0])*0.5
Image.fromarray((ov*255).astype(np.uint8)).resize((480,640)).save('/tmp/claude-0/-home-user-claude/a0adde3b-fc66-5875-9f38-4af2202cc77e/scratchpad/mask.jpg')
