"""Put Ward's scar (traced from I3) into the CAM 11 playback-zoom insert, same shape, same direction.

    python3 scar_composite.py   (run from previs/keyframes/tools)

Reads ../v2/frames/21_C2_cam11_zoom_generated.jpg (LibTV, node i-D1IdSQ2K1M: the hand from the crates,
Nora looking at it, but with a round "window" in the glove and a short scar) and ../v2/frames/25a_I3.jpg.
Fills the round hole with glove fabric, cuts a ragged rip along the scar, lays the real I3 skin under it
(turned 180 degrees: on a hand pointing right the wrist-to-index-knuckle line is the same "/" as in I3),
lifts the traced scar so it reads in infrared, then degrades the frame like a 4x playback zoom.
Writes ../v2/frames/21_C2_cam11_zoom.jpg. Needs numpy, Pillow, opencv-python-headless."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
rng=np.random.default_rng(12)
# scar centre line traced on I3 (1280x720), wrist end first; the first point is the small hook
TRACE=[(700,224),(697.5,232.5),(680,245),(660,255),(635,265),(610,275),(590,287.5),(572.5,302.5),(557.5,317.5)]
WID=[3,5,7,8,9,8,7,5,3]          # relative width along the scar
z=Image.open('../v2/frames/21_C2_cam11_zoom_generated.jpg').convert('L').resize((1920,1078),Image.LANCZOS)
import cv2
zz=np.asarray(z).copy()
hole=np.zeros_like(zz); hole[440:690,630:870]=(zz[440:690,630:870]>120).astype(np.uint8)*255
hole=cv2.dilate(hole,np.ones((15,15),np.uint8))
zz=cv2.inpaint(zz,hole,9,cv2.INPAINT_TELEA)
z=Image.fromarray(zz)
cx,cy=752,560; S=1.55
c=np.mean(TRACE[1:],axis=0)
pts=[(cx-(x-c[0])*S, cy-(y-c[1])*S) for x,y in TRACE]       # 180 deg: wrist end now lower-left, knuckle end upper-right
# skin: the real I3 skin around the scar, turned 180 degrees and scaled like the trace, in IR grey
i3=Image.open('../v2/frames/25a_I3.jpg').convert('L')
box=(int(c[0]-140),int(c[1]-105),int(c[0]+140),int(c[1]+105))
p=i3.crop(box).rotate(180).resize((int(280*S),int(210*S)),Image.LANCZOS)
pa=np.asarray(p,float); pa=(pa-pa.mean())*0.9+150
skin=np.full((1078,1920),150.0)
x0,y0=int(cx-p.width/2),int(cy-p.height/2)
skin[y0:y0+p.height,x0:x0+p.width]=pa
skin=Image.fromarray(np.clip(skin,0,255).astype(np.uint8))
ridge=Image.new('L',z.size,0); shadow=Image.new('L',z.size,0)
dr=ImageDraw.Draw(ridge); ds=ImageDraw.Draw(shadow)
for (p,q),w in zip(zip(pts[:-1],pts[1:]),WID[1:]):
    dr.line([p,q],fill=255,width=int(w*S*1.3)); ds.line([(p[0]+3,p[1]+4),(q[0]+3,q[1]+4)],fill=255,width=int(w*S*1.3))
ridge=ridge.filter(ImageFilter.GaussianBlur(3)); shadow=shadow.filter(ImageFilter.GaussianBlur(4))
sk=np.asarray(skin,float)*(1-0.35*np.asarray(shadow,float)/255)
sk=sk+(215-sk)*0.6*np.asarray(ridge,float)/255
skin=Image.fromarray(np.clip(sk,0,255).astype(np.uint8))
# a rip along the scar: tapered at both ends, ragged edges, a few threads across the gap
P=np.array(pts[1:]); 
seg=np.linspace(0,1,60)
cum=np.r_[0,np.cumsum(np.linalg.norm(np.diff(P,axis=0),axis=1))]; cum/=cum[-1]
ext=0.18                                                       # the rip runs a little past both ends of the scar
u=np.linspace(-ext,1+ext,90)
cxs=np.interp(np.clip(u,0,1),cum,P[:,0]); cys=np.interp(np.clip(u,0,1),cum,P[:,1])
d0=P[-1]-P[0]; d0=d0/np.linalg.norm(d0)
cxs=cxs+np.where(u<0,u,np.where(u>1,u-1,0))*np.linalg.norm(P[-1]-P[0])*d0[0]
cys=cys+np.where(u<0,u,np.where(u>1,u-1,0))*np.linalg.norm(P[-1]-P[0])*d0[1]
nrm=np.array([-d0[1],d0[0]])
half=np.clip(np.sin(np.pi*(u+ext)/(1+2*ext)),0,1)**0.7*58
upper=[(x+nrm[0]*(h+rng.normal(0,5)), y+nrm[1]*(h+rng.normal(0,5))) for x,y,h in zip(cxs,cys,half)]
lower=[(x-nrm[0]*(h+rng.normal(0,5)), y-nrm[1]*(h+rng.normal(0,5))) for x,y,h in zip(cxs,cys,half)]
outline=upper+lower[::-1]
mask=Image.new('L',z.size,0); d=ImageDraw.Draw(mask); d.polygon(outline,fill=255); mask=mask.filter(ImageFilter.GaussianBlur(1.0))
# shading: darker toward the torn edges (the glove sits above the skin)
edge=np.asarray(mask.filter(ImageFilter.GaussianBlur(14)),float)/255
skin=Image.fromarray(np.clip(np.asarray(skin,float)*(0.55+0.45*edge),0,255).astype(np.uint8))
out=Image.composite(skin,z,mask)
rim=Image.new('L',z.size,0); ImageDraw.Draw(rim).line(outline+[outline[0]],fill=255,width=8)
rim=rim.filter(ImageFilter.GaussianBlur(2.5))
o=np.asarray(out,float)*(1-0.6*np.asarray(rim,float)/255)
out=Image.fromarray(o.astype(np.uint8)); dd=ImageDraw.Draw(out)
for k in (20,47,66):                                           # three loose threads across the rip
    p=upper[k]; q=lower[k+int(rng.integers(-3,4))]
    m=((p[0]+q[0])/2+rng.normal(0,6),(p[1]+q[1])/2+rng.normal(0,6))
    dd.line([p,m,(m[0]*0.7+q[0]*0.3,m[1]*0.7+q[1]*0.3)],fill=int(rng.uniform(85,115)),width=1)
small=out.resize((480,270),Image.BILINEAR); big=small.resize((1920,1078),Image.BILINEAR)
b=np.asarray(big,float); b=(b-128)*1.12+128+rng.normal(0,8,b.shape)
Image.fromarray(np.clip(b,0,255).astype(np.uint8)).convert('RGB').resize((1920,1080),Image.LANCZOS).save('../v2/frames/21_C2_cam11_zoom.jpg',quality=92)
i3=Image.open('../v2/frames/25a_I3.jpg').convert('RGB')
