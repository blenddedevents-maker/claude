import sys
from rembg import remove, new_session
from PIL import Image
s=new_session("birefnet-portrait")
im=Image.open(sys.argv[1]).convert("RGB")
out=remove(im,session=s)
out.save(sys.argv[2])
bg=Image.new("RGBA",out.size,(255,0,255,255)); bg.alpha_composite(out); bg.convert("RGB").save(sys.argv[3])
