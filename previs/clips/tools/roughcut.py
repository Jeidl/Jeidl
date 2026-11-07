"""Silent rough cut of EXHIBIT 47 from the AKOOL clips, on the shot-list timeline (88 s, 24 fps).

    python3 fetch_clips.py /tmp/clips
    python3 roughcut.py OUT.mp4 /tmp/clips [W H]

v1: Seedance 1.0 Pro Fast takes where they beat Akool Premium, the C2 entrance from a
Seedance Lite first/last-frame clip, the I2 lip-sync, and a dialogue track built from
previs/audio/voice (lines placed at the shot-list times; no music or effects yet).

Needs ffmpeg and Pillow. Stills come from previs/keyframes/v2/frames. Text cards are
placeholders (Liberation Sans); the AKOOL card is a placeholder for the official logo."""
import os, subprocess, sys, json
from PIL import Image, ImageDraw, ImageFont
import tempfile
HERE=os.path.dirname(os.path.abspath(__file__)); C=os.path.abspath(sys.argv[2])+'/'; T=tempfile.mkdtemp()+'/'
KF=os.path.normpath(os.path.join(HERE,'..','..','keyframes','v2','frames'))+'/'
W,H=(int(sys.argv[3]),int(sys.argv[4])) if len(sys.argv)>4 else (1280,720)
FPS=24
BOLD='/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
MONO='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
segs=[]; n=[0]
def run(cmd): subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
def out():
    n[0]+=1; p=f'{T}s{n[0]:03d}.mp4'; segs.append(p); return p
VF=f'scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},format=yuv420p'
def clip(name,start,frames,extra=''):
    vf=VF+(','+extra if extra else '')+f',tpad=stop_mode=clone:stop={frames}'
    o=out(); run(['ffmpeg','-y','-ss',str(start),'-i',C+name+'.mp4','-frames:v',str(frames),'-vf',vf,'-an','-c:v','libx264','-preset','veryfast','-crf','20','-r',str(FPS),'-video_track_timescale','12288',o])
    got=int(subprocess.run(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=nb_read_frames','-of','csv=p=0',o],capture_output=True,text=True).stdout.strip() or 0)
    if got!=frames: print('short segment',name,start,frames,got)
def still(img,frames):
    p=T+f'still{n[0]+1}.png'; img.convert('RGB').resize((W,H)).save(p)
    run(['ffmpeg','-y','-loop','1','-i',p,'-frames:v',str(frames),'-vf',VF,'-c:v','libx264','-preset','veryfast','-crf','20','-r',str(FPS),'-video_track_timescale','12288',out()])
def card(lines,frames,size=0.052,color=(236,232,224),sub=None,dot=None):
    im=Image.new('RGB',(W,H),(0,0,0)); d=ImageDraw.Draw(im)
    f=ImageFont.truetype(BOLD,int(H*size)); lh=int(H*size*1.35)
    y0=H//2-lh*len(lines)//2
    for i,t in enumerate(lines):
        w=d.textlength(t,font=f); d.text(((W-w)/2,y0+i*lh),t,font=f,fill=color)
    if sub:
        fs=ImageFont.truetype(BOLD,int(H*0.026)); w=d.textlength(sub,font=fs); d.text(((W-w)/2,y0+len(lines)*lh+H*0.02),sub,font=fs,fill=(150,150,150))
    if dot: r=int(H*0.012); x,y=dot; d.ellipse((x-r,y-r,x+r,y+r),fill=(224,40,28))
    still(im,frames)
def color(rgb,frames): still(Image.new('RGB',(W,H),rgb),frames)
def frame_of(name,t):
    p=T+f'grab_{name}_{t}.png'; run(['ffmpeg','-y','-ss',str(t),'-i',C+name+'.mp4','-frames:v','1',p]); return Image.open(p).copy()
def kf(name): return Image.open(KF+name)
def grid(frames,lost_at,unknown=False):
    """4x3 monitor wall from 12 clips; lost_at = {cell_index: frame_when_lost}"""
    cells=['04_C3__akp','13_B3__akp','19c_C1__akp','05_B1__akp','19h_X1__akp','15_B4__akp','10_B2a__akp','19e_B6__akp','19b_B9__akp','21_C2_start__akp','19d_B10__akp','19i_B8_start__akp']
    cw,ch=W//4,H//3; fm=ImageFont.truetype(MONO,int(ch*0.09)); fl=ImageFont.truetype(BOLD,int(ch*0.12))
    tmp=T+'gridf/'; os.makedirs(tmp,exist_ok=True)
    caps={}
    for i,c in enumerate(cells):
        p=tmp+f'c{i}_%04d.png'
        run(['ffmpeg','-y','-i',C+c+'.mp4','-frames:v',str(frames),'-vf',f'fps={FPS},scale={cw}:{ch}',p])
    for k in range(frames):
        im=Image.new('RGB',(W,H)); d=ImageDraw.Draw(im)
        for i in range(12):
            x,y=(i%4)*cw,(i//4)*ch
            if i in lost_at and k>=lost_at[i]:
                d.rectangle((x,y,x+cw-1,y+ch-1),fill=(0,0,0))
                t='SIGNAL LOST'; w=d.textlength(t,font=fl); d.text((x+(cw-w)/2,y+ch/2-ch*0.06),t,font=fl,fill=(200,200,200))
            else:
                im.paste(Image.open(tmp+f'c{i}_{k+1:04d}.png'),(x,y))
            d.rectangle((x,y,x+cw-1,y+ch-1),outline=(40,40,40))
            d.text((x+6,y+4),f'7-{i+1:02d}',font=fm,fill=(230,230,230))
        im.save(tmp+f'g_{k:04d}.png')
    run(['ffmpeg','-y','-framerate',str(FPS),'-i',tmp+'g_%04d.png','-vf',VF,'-c:v','libx264','-preset','veryfast','-crf','20','-r',str(FPS),'-video_track_timescale','12288',out()])
    run(['bash','-c',f'rm -f {tmp}*.png'])
F=lambda s: int(round(s*FPS))
# ---------------- timeline (shot list v3) ----------------
card(['AKOOL'],F(2.0),size=0.09,sub='official logo goes here')            # 01
clip('02_D1__akp',0.0,F(4.0))                                              # 02 D1
card(['12 OFFICERS WENT IN.'],F(1.5))                                      # 03
clip('04_C3__sdfast',0.6,F(4.0))                                              # 04 C3
clip('05_B1__sdfast',1.0,F(2.5))                                              # 05 B1
card(['1 CAME OUT.'],F(1.5))                                               # 06
clip('07_I1__sdfast',0.2,F(3.0))                                              # 07 I1
card(['13 CAMERAS WERE RECOVERED.'],F(1.5))                                # 08
clip('09_E1__akp',1.0,F(3.0))                                              # 09 E1
clip('10_B2a__sdfast',0.4,F(2.4)); clip('10_B2b__akp',0.0,12); clip('10_B2b__sdfast',0.3,F(1.6)-12)  # 10 B2: Seedance descent, Akool whip blur, Seedance hold
color((0,0,0),F(0.5))                                                      # 11
grid(F(3.0),{2:F(1.2),8:F(2.0)})                                           # 12 GRID
clip('13_B3__akp',0.3,F(3.0))                                              # 13 B3
card(['ONLY 12 CAMERAS WERE ISSUED.'],F(2.0))                              # 14
clip('15_B4__sdfast',2.5,F(2.5))                                              # 15 B4
card(['ONE CAMERA BELONGED','TO A DEAD MAN.'],F(2.0)-3)                    # 16
clip('S2_O1__akp',1.0,3) if os.path.exists(C+'S2_O1__akp.mp4') else still(kf('S2_O1.jpg'),3)
clip('17_O2__sdfast',1.5,F(2.5))                                              # 17 O2
clip('18_E3_register__akp',0.5,F(2.0)); clip('18_E3_tag__akp',0.2,F(1.0))  # 18 E3
clip('19a_B5__sdfast',0.6,F(1.0)); clip('19b_B9__akp',0.4,F(1.0)); clip('19c_C1__akp',0.8,F(1.0))      # 19a-c
pick=lambda a,b: a if os.path.exists(C+a+'.mp4') else b
clip('19d_B10__akp',0.4,F(1.0)); clip(pick('19e_B6__sdfast','19e_B6__akp'),0.5,F(1.0))                                     # 19d-e
grid(F(1.0),{0:0,2:0,8:0,3:F(0.2),6:F(0.5),10:F(0.8)})                    # 19f three more lost
clip('19g_B7__akp',2.0,F(1.5)); clip(pick('19h_X1__sdfast','19h_X1__akp'),1.0,F(1.5))           # 19g-h
clip('19i_B8_start__akp',2.8,F(0.7)); clip('19i_B8_reflection__akp',1.0,F(0.8))  # 19i
grid(F(1.0),{i:0 for i in range(11)}|{11:F(0.6)})                         # 20 last cell lost
color((0,0,0),F(1.5))
card(['UNKNOWN'],F(1.5),size=0.04,dot=(W//2,int(H*0.40)))
if os.path.exists(C+'21_C2_full__sdlite.mp4'): clip('21_C2_full__sdlite',0.8,F(2.4)); color((12,12,12),2); clip('21_C2_grab__akp',0.0,F(2.0))  # 21 C2: entrance, 2-frame CCTV dropout, grab and pull
else: clip('21_C2_grab__akp',0.0,F(4.5))
# 22 montage, 6.0 s = 144 frames
i2=kf('S1_I2.jpg'); glove=kf('21_C2_glove_insert.jpg'); tag=frame_of('24_E2__akp',0.4); refl=frame_of('19i_B8_reflection__akp',2.5)
clip('S1_I2__talk',0.2,36) if os.path.exists(C+'S1_I2__talk.mp4') else still(i2,36); color((255,255,255),2)
clip('S2_O1__akp',0.5,10) if os.path.exists(C+'S2_O1__akp.mp4') else still(kf('S2_O1.jpg'),10)
color((0,0,0),2); still(glove,4); color((0,0,0),2)
clip('10_B2a__akp',1.0,12); color((255,255,255),2); still(tag,4)
clip('17_O2__sdfast',2.5,10); still(refl,3); clip('19g_B7__akp',2.5,10); color((255,255,255),2)
card(['UNKNOWN'],3,size=0.04,dot=(W//2,int(H*0.40))); clip('19a_B5__sdfast',1.0,8)
still(glove,2); still(tag,2); still(refl,2); color((0,0,0),144-(36+2+10+2+4+2+12+2+4+10+3+10+2+3+8+6))
color((0,0,0),F(1.5))                                                      # 23 silence
i3='25a_I3__sdfast'
clip(i3,0.3,F(3.0))                                                        # 25a I3
clip('25b_I4__kling',0.6,F(4.0))                                           # 25b I4
clip('24_E2__akp',0.0,F(3.0),f"drawtext=fontfile={BOLD}:text='EXHIBIT 47':fontcolor=white:fontsize={int(H*0.075)}:x=(w-tw)/2:y=h*0.42:enable='gte(t,0.6)'")  # 24 E2 + title
card(['COMING NEVER'],F(2.5),size=0.06,sub='AKOOL')                        # 29
for k in range(3):                                                         # 30 red dot blinks
    card([''],F(0.45),dot=(W//2,H//2)); color((0,0,0),F(0.35))
card([''],F(3.5)-3*(F(0.45)+F(0.35)),dot=(W//2,H//2))
# ---------------- concat ----------------
lst=T+'list.txt'; open(lst,'w').write(''.join(f"file '{p}'\n" for p in segs))
silent=T+'silent.mp4'
if os.environ.get('RC_DEBUG'):
    for sp in segs: print(os.path.basename(sp), subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',sp],capture_output=True,text=True).stdout.strip())
inp=[]
for sp in segs: inp+=['-i',sp]
run(['ffmpeg','-y']+inp+['-filter_complex',''.join(f'[{i}:v]' for i in range(len(segs)))+f'concat=n={len(segs)}:v=1:a=0,fps={FPS}[v]','-map','[v]','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',silent])
# ---------------- dialogue (shot-list times, seconds) ----------------
VO=os.path.normpath(os.path.join(HERE,'..','..','audio','voice'))+'/'
PHONE='highpass=f=350,lowpass=f=3200,acrusher=bits=8:mix=0.25,volume=1.4'
RADIO='highpass=f=500,lowpass=f=2800,acrusher=bits=6:mix=0.4,volume=1.5'
LINES=[(3.0,'V1_nora_thirteen',''),
       (7.6,'V12_dispatch_emergency',PHONE),(9.0,'V11_caller_northgate',PHONE),(10.6,'V12_dispatch_who',PHONE),
       (15.8,'V2_ward_twelve_officers','aecho=0.6:0.4:40:0.15'),
       (23.0,'V5_brandt_count_off',''),(23.8,'V6_count_ten',''),(24.4,'V6_count_eleven',''),(25.0,'V7_nora_twelve',''),
       (25.9,'V8_thirteenth_twelve','volume=0.8'),(26.5,'V5_brandt_who',''),
       (31.0,'V9_reyes_still_recording',RADIO),(35.6,'V5_brandt_masks',''),(40.2,'V10_reyes_mine_stays_on','highpass=f=200,lowpass=f=5000'),
       (51.6,'V5_brandt_buried',''),(62.1,'V3_ward_safe_whisper','highpass=f=600,volume=0.55'),
       (72.3,'V4_ward_safe','aecho=0.6:0.4:40:0.15'),(86.0,'V8_thirteenth_twelve','highpass=f=500,volume=0.5')]
TRIM='silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse'
ins=[]; fl=[]
for i,(t,name,fx) in enumerate(LINES):
    ins+=['-i',VO+name+'.mp3']
    chain=TRIM+(','+fx if fx else '')+f',adelay={int(t*1000)}:all=1'
    fl.append(f'[{i}:a]{chain}[a{i}]')
n=len(LINES)
fl.append(''.join(f'[a{i}]' for i in range(n))+f'amix=inputs={n}:normalize=0:duration=longest,apad=whole_dur=88,atrim=0:88[mix]')
if os.path.exists(C+'S1_I2__talk.mp4'):   # the lip-sync line inside the montage (1:04.5)
    ins+=['-ss','0.2','-t','1.5','-i',C+'S1_I2__talk.mp4']
    fl[-1]=fl[-1].replace('[mix]','[dlg]')
    fl.append(f'[{n}:a]adelay=64500:all=1[lip]'); fl.append('[dlg][lip]amix=inputs=2:normalize=0:duration=first[mix]')
aud=T+'dialogue.m4a'
run(['ffmpeg','-y']+ins+['-filter_complex',';'.join(fl),'-map','[mix]','-c:a','aac','-b:a','160k',aud])
run(['ffmpeg','-y','-i',silent,'-i',aud,'-map','0:v','-map','1:a','-c:v','copy','-c:a','copy','-t','88',sys.argv[1]])
d=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',sys.argv[1]],capture_output=True,text=True).stdout)
print(len(segs),'segments,',round(d,2),'s')
