import sys, importlib.util
from PIL import Image, ImageDraw
spec = importlib.util.spec_from_file_location('icons', sys.argv[1]); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
S=8; names=list(m.I); W=len(names)*140
im=Image.new('RGB',(W,160),'#FFF8F3'); d=ImageDraw.Draw(im)
for i,n in enumerate(names):
    g=m.I[n]; L=len(g); s=128//L
    for y,row in enumerate(g):
        for x,ch in enumerate(row):
            if ch!='.': d.rectangle([i*140+6+x*s,6+y*s,i*140+6+x*s+s-1,6+y*s+s-1],fill=m.PAL[ch])
    d.text((i*140+6,140),n,fill='#4A3A3A')
im.save(sys.argv[2])
