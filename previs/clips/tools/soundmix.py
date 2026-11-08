"""Mix dialogue, music and sound effects onto rough cut v3, placed on the picture's own frames.

    python3 soundmix.py CUT.mp4 OUT.mp4 [CLIP_DIR]

CUT.mp4 comes from roughcut.py, which also writes CUT.timeline.json. Every cue below is
anchored to a segment of that timeline: at('B1', src=2.21) is "the frame of 05_B1 at 2.21 s,
wherever it lands in the cut", at('B2h', 0.15) is "0.15 s into the B2h segment". Nothing
uses a fixed second, so re-cutting the picture moves the sound with it. Gunshots in B5 and
C1 go on the muzzle flashes roughcut.py found in those segments.

CLIP_DIR  optional: folder with S1_I2__talk.mp4, for the lip-synced line in the montage.

Sources (relative to this file): ../../audio/voice/*.mp3 (AKOOL TTS), ../../audio/sfx/*.mp3
(LibTV Seed Audio; FX7_shot_* are single shots cut from FX7), ../../audio/music/SC1_music_bed.mp3
(LibTV ElevenMusic). Effect files are peak-normalised to -1 dBFS, so gains are relative.
HIT holds how far into each effect file its hit is (default 0.1 s, the generator's lead-in).
Each dialogue line is levelled to -20 dBFS mean before its own filter. The mix is normalised
in two passes (linear) to -14 LUFS with a -2 dBTP ceiling (about -1.4 dBTP after AAC).
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.normpath(os.path.join(HERE, '..', '..', 'audio'))
VO, FX, MU = A + '/voice/', A + '/sfx/', A + '/music/'
IN, OUT = sys.argv[1], sys.argv[2]
CLIPS = sys.argv[3] if len(sys.argv) > 3 else None
TL = json.load(open(os.path.splitext(IN)[0] + '.timeline.json'))
S = {s['id']: s for s in TL['segments']}
DUR = round(TL['duration'], 3)


def at(sid, off=0.0, src=None):
    """Absolute time of a point in segment sid: off seconds in, or source time src of its clip."""
    s = S[sid]
    return s['start'] + (src - s['src_in'] if src is not None else off)


def end(sid):
    return S[sid]['start'] + S[sid]['dur']


SILENT = [(at('DEAD'), end('DEAD')), (at('BLACK2'), end('BLACK2'))]   # total silence
HIT = {'FX12a_impact': 0.45, 'FX_whoosh': 0.5, 'FX6_door_breach': 0.19, 'FX12b_braaam': 0.13, 'SC2_riser': 0.0,
       'FX4_compressor': 0.0, 'FX_wind_drone': 0.0, 'FX7_shot_a': 0.02, 'FX7_shot_b': 0.02, 'FX7_shot_c': 0.02}

PHONE = 'highpass=f=350,lowpass=f=3200,acrusher=bits=8:mix=0.25,atempo=1.1,volume=1.4'
RADIO = 'highpass=f=500,lowpass=f=2800,acrusher=bits=6:mix=0.4,volume=1.5'
SHOUT_RADIO = 'highpass=f=300,lowpass=f=3800,acrusher=bits=10:mix=0.25,volume=1.3'
OLD_TAPE = 'highpass=f=250,lowpass=f=4200,acrusher=bits=9:mix=0.2'
ROOM = 'aecho=0.9:0.9:40:0.15'   # in x out gain stays near unity
DISTANT = 'lowpass=f=1800,aecho=0.8:0.6:60:0.3'   # what a CCTV microphone would hear
# silenceremove and areverse drop the timestamps, so every chain ends in asetpts=N/SR/TB
TRIM = 'silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse'

# (time, file, filter) -- dialogue, each on the picture it belongs to
DIALOGUE = [
    # the call starts under the AKOOL card (sound first) and ends before the hammer comes down
    (0.55, 'V11_caller_northgate', PHONE), (at('C3', 2.25), 'V12_dispatch_who', PHONE),
    (at('CARD12', 0.35), 'V11_caller_seven_twelve', PHONE),
    (at('D1', 0.3), 'V1_nora_thirteen', 'volume=1.3'),                       # over the survivor walking out
    (at('I1', 0.1), 'V2_ward_twelve_officers', ROOM),
    # Nora's camera: count off, she says twelve, a pause, the swing back, a second twelve
    (at('B2', 0.2), 'V5_brandt_count_off', ''), (at('B2', 0.9), 'V6_count_ten', ''),
    (at('B2', 1.4), 'V6_count_eleven', ''), (at('B2', 1.85), 'V7_nora_twelve', ''),
    (at('B2h', 0.12), 'V8_thirteenth_twelve', 'volume=0.9'), (at('B2h', 0.62), 'V5_brandt_who', ''),
    (at('B3', 0.3), 'V9_reyes_still_recording', RADIO),
    (at('B4', 0.15), 'V5_brandt_masks_quiet', 'volume=0.85'),       # held back: suspicion, not a shout
    (at('O2', 0.05), 'V10_reyes_mine_stays_on', OLD_TAPE + ',volume=1.4'),
    (at('E3TAG', 0.75), 'V5_brandt_fall_back', SHOUT_RADIO + ',volume=1.5'),         # the firefight's goal: get out
    (at('B7', 0.15), 'V5_brandt_buried', 'acrusher=bits=9:mix=0.4,volume=1.4'),
    (at('C2i', 0.0), 'V3_ward_safe_whisper', 'highpass=f=400,volume=2.2'),
    (at('I3', 0.5), 'V4_ward_safe', ROOM),
    (at('DOTHOLD', 0.2), 'V8_thirteenth_twelve', 'highpass=f=500,volume=1.6'),
]
LIP = at('M_I2') if 'M_I2' in S else None        # I2 lip-sync audio runs its whole line (L-cut)

# (time, file, gain, extra filter) -- effects
shots = ['FX7_shot_a', 'FX7_shot_b', 'FX7_shot_c']
GUNS = [(at('B5', t), shots[k % 3], 0.7, '') for k, t in enumerate(S['B5'].get('flashes', []))]
GUNS += [(at('C1', t), shots[(k + 1) % 3], 0.5, DISTANT) for k, t in enumerate(S['C1'].get('flashes', []))]
EFFECTS = GUNS + [
    (0.3, 'FX3_radio', 0.45, ''),
    (at('CARD12', 1.15), 'FX2_dropout', 0.35, 'atrim=0:0.25'),       # the caller hangs up
    (at('B1', src=2.21), 'FX6_door_breach', 1.0, 'atrim=0.8:4'),     # from the second bang (0.99 s in the file): the hit we see, then the door gives
    (at('CARD1'), 'FX12a_impact', 0.55, ''),
    (at('D1'), 'FX_wind_drone', 0.35, 'afade=t=in:d=0.3,afade=t=out:st=2.1:d=0.4'),
    (at('CARD13', 0.05), 'FX1_beep', 0.5, ''),
    (at('B2', -0.3), 'FX1_beep', 0.4, ''),                          # Nora's camera starts recording
    (at('B2w', 0.25), 'FX_whoosh', 0.5, ''),
    (at('B2h', 0.1), 'FX10_breath', 0.3, ''),
    (at('BLACK1', 0.25), 'FX12b_braaam', 1.0, ''),
    (at('GRID1', 1.2), 'FX2_dropout', 0.6, ''), (at('GRID1', 2.0), 'FX2_dropout', 0.6, ''),
    (at('B3'), 'FX5_curtain', 0.8, ''), (at('B3', 0.1), 'FX3_radio', 0.6, ''),
    (at('CARD_DEAD'), 'FX12a_impact', 0.6, 'afade=t=out:st=1.4:d=0.4'), (at('O1F'), 'FX2_dropout', 0.5, ''),
    (at('O2'), 'FX2_dropout', 0.3, 'atrim=0:0.4'),                   # tape starting
    (at('E3REG'), 'FX12a_impact', 0.35, 'lowpass=f=900'),
    (at('E3REG', S['E3REG'].get('stamp_at', 1.0)), 'FX12a_impact', 0.7, 'atrim=0:0.5,lowpass=f=1500,afade=t=out:st=0.35:d=0.15'),  # LOST
    (at('E3TAG', -0.02), 'FX_whoosh', 0.6, ''), (at('E3TAG', 0.35), 'FX1_beep', 0.3, ''),
    (at('B9', 0.35), 'FX7_shot_b', 0.7, ''), (at('B9', 0.75), 'FX_flashlight_drop', 0.8, ''),
    (at('B10'), 'FX_flashbang_ring', 0.9, ''),
    (at('B6'), 'FX8_gas_alarm', 0.9, 'afade=t=out:st=2.5:d=1'),     # the pipe bursts: the way back is gas
    (at('GRID2', 0.2), 'FX2_dropout', 0.55, ''), (at('GRID2', 0.5), 'FX2_dropout', 0.5, ''),
    (at('GRID2', 0.8), 'FX2_dropout', 0.5, ''),
    (at('X1'), 'FX10_breath', 0.7, ''), (at('X1'), 'FX7_gunshots', 0.22, 'lowpass=f=1200'),
    (at('B8s'), 'FX9_steps', 0.6, 'afade=t=out:st=0.6:d=0.2'),
    (at('B8r', 0.05), 'FX12a_impact', 0.45, 'lowpass=f=600'),       # the reveal: his own reflection
    (at('GRID3', 0.6), 'FX2_dropout', 0.7, ''),
    (at('FEED13', 2 / 24), 'FX1_beep', 0.35, ''), (at('FEED13', 0.3), 'FX10_breath', 0.25, ''),
    (at('C2e'), 'FX8_gas_alarm', 0.3, 'lowpass=f=3000,afade=t=in:d=0.5,afade=t=out:st=3:d=1.5'),
    (at('C2d'), 'FX2_dropout', 0.45, 'atrim=0:0.3'),
    (at('C2g', 0.03), 'FX5_curtain', 0.5, 'atrim=0.3:0.7,lowpass=f=2500'),        # strap grabbed
    (at('C2i'), 'FX12a_impact', 0.35, 'atrim=0:0.4,lowpass=f=400'),              # her camera knocked
    (at('C2p', src=0.8), 'FX7_shot_c', 0.6, DISTANT),                            # sparks where she stood
    (at('C2p', src=1.1), 'FX9_steps', 0.5, 'atrim=0:0.5,' + DISTANT),            # feet dragged
    (at('C2p', src=1.5), 'FX12a_impact', 0.4, 'atrim=0:0.5,lowpass=f=500'),      # behind the crates
    (at('M_w1'), 'FX12a_impact', 0.35, 'atrim=0:1.2'), (at('M_w3'), 'FX12a_impact', 0.7, 'atrim=0:1.2'),
    (at('I3', 0.1), 'FX11_pen', 0.7, ''),
    (at('TITLE', S['TITLE'].get('title_at', 0.6)), 'FX12a_impact', 1.0, ''),     # the one ending hit
    (at('TITLE', S['TITLE'].get('title_at', 0.6)), 'FX1_beep', 0.5, ''),
] + [(at(f'DOT{k}'), 'FX1_beep', 0.22, '') for k in range(3)] + [(at('DOTHOLD'), 'FX1_beep', 0.3, '')]

# riser and music peak end exactly where the montage cuts to black
M0, M1 = at('M_I2'), at('M_end')
L = round(M1 - M0, 3)
EFFECTS.append((M0, 'SC2_riser', 0.8, f'atrim={6.0 - L:.3f}:6.0,asetpts=PTS-STARTPTS,afade=t=out:st={L - 0.06:.3f}:d=0.06'))

# (timeline start, source start, length, gain) -- SC1 cut to this picture
pulse_a = at('DEAD') - at('GRID1')
MUSIC = [
    (0.0, 0.0, at('BLACK1'), 0.30),                       # sparse intro under act one
    (at('GRID1'), 35.8, pulse_a, 0.38),                    # pulse until the wall dies
    (at('C2e'), 35.8 + pulse_a, end('C2p') - at('C2e'), 0.38),   # back in for C2 (FEED 13 has none)
    (M0, 102.4 - L, L, 0.70),                              # peak; its own dead stop lands on the cut to black
    (at('I3'), 104.0, end('CN') - at('I3'), 0.10),         # quiet tail under I3, I4, the title
]

inputs, chains = [], []


def add_input(path, pre=None):
    """Add an ffmpeg input and return its index."""
    inputs.extend((pre or []) + ['-i', path])
    return inputs.count('-i') - 1


def ms(t, name=None):
    """adelay in ms so the file's hit (if it is an effect) lands at time t."""
    return max(0, int(round((t - (HIT.get(name, 0.1) if name else 0)) * 1000)))


def level(path, pre=None, target=-20.0):
    """Gain in dB that brings the line's mean level (leading/trailing silence trimmed) to target dBFS.
    The TTS voices come out at different levels, so every line is levelled before its own filter."""
    err = subprocess.run(['ffmpeg', '-hide_banner'] + (pre or []) + ['-i', path, '-af', TRIM + ',volumedetect',
                          '-f', 'null', '-'], capture_output=True, text=True).stderr
    mean = float(err.split('mean_volume:')[1].split('dB')[0])
    return round(target - mean, 1)


bus = {'dlg': [], 'fx': [], 'mus': []}
for t, name, fx in DIALOGUE:
    i = add_input(VO + name + '.mp3')
    chains.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo,{TRIM},volume={level(VO + name + ".mp3")}dB' +
                  (f',{fx}' if fx else '') + f',adelay={ms(t)}:all=1,asetpts=N/SR/TB[d{i}]')
    bus['dlg'].append(f'[d{i}]')
if LIP is not None and CLIPS and os.path.exists(os.path.join(CLIPS, 'S1_I2__talk.mp4')):
    talk, pre = os.path.join(CLIPS, 'S1_I2__talk.mp4'), ['-ss', '0.2', '-t', '2.9']
    i = add_input(talk, pre)
    chains.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo,volume={level(talk, pre, -15.0)}dB,'
                  f'afade=t=out:st=2.7:d=0.2,adelay={ms(LIP)}:all=1,asetpts=N/SR/TB[d{i}]')
    bus['dlg'].append(f'[d{i}]')
for t, name, g, fx in EFFECTS:
    i = add_input(FX + name + '.mp3')
    chains.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo' + (f',{fx}' if fx else '') +
                  f',volume={g},adelay={ms(t, name)}:all=1,asetpts=N/SR/TB[f{i}]')
    bus['fx'].append(f'[f{i}]')
for t, s, length, g in MUSIC:
    i = add_input(MU + 'SC1_music_bed.mp3')
    chains.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo,atrim={s}:{s + length},asetpts=PTS-STARTPTS,'
                  f'afade=t=in:d=0.05,afade=t=out:st={length - 0.08}:d=0.08,volume={g},adelay={ms(t)}:all=1,asetpts=N/SR/TB[m{i}]')
    bus['mus'].append(f'[m{i}]')
i = add_input(FX + 'FX4_compressor.mp3', ['-stream_loop', '-1'])
chains.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{DUR},asetpts=N/SR/TB,volume=0.08[amb]')


def mix(labels, out):
    chains.append(''.join(labels) + f'amix=inputs={len(labels)}:normalize=0:duration=longest,apad=whole_dur={DUR},atrim=0:{DUR}[{out}]')


mix(bus['dlg'], 'dlg0'); mix(bus['fx'], 'fx'); mix(bus['mus'], 'mus0')
chains.append('[dlg0]asplit=2[dlg][dsc]')
chains.append('[mus0][dsc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=350[mus]')
mute = '+'.join(f'between(t,{a:.3f},{b:.3f})' for a, b in SILENT)
chains.append(f'[dlg][mus][fx][amb]amix=inputs=4:normalize=0:duration=longest,'
              f"volume='if({mute},0,1)':eval=frame,alimiter=limit=0.7:level=false[out]")
pre, tmp = OUT + '.pre.wav', OUT + '.mix.wav'
subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inputs + ['-filter_complex', ';'.join(chains), '-map', '[out]',
                '-t', str(DUR), '-c:a', 'pcm_s24le', pre], check=True)
# loudnorm pass 1 (measure), pass 2 (linear gain, so the silences and the dynamics stay as mixed)
LN = 'loudnorm=I=-14:TP=-2:LRA=11'   # -2 before AAC lands at or below -1.5 dBTP after it
log = subprocess.run(['ffmpeg', '-hide_banner', '-i', pre, '-af', LN + ':print_format=json', '-f', 'null', '-'],
                     capture_output=True, text=True).stderr
m = json.loads(log[log.rindex('{'):log.rindex('}') + 1])
ln2 = (f"{LN}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
       f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', pre, '-af', ln2 + ',aresample=48000', '-c:a', 'pcm_s16le', tmp], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', IN, '-i', tmp, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                '-c:a', 'aac', '-b:a', '192k', '-t', str(DUR), OUT], check=True)
os.remove(pre); os.remove(tmp)
cues = {'dialogue': [(round(t, 3), n) for t, n, _ in DIALOGUE], 'effects': [(round(t, 3), n) for t, n, _, _ in EFFECTS],
        'music': [(round(t, 3), s, round(l, 3)) for t, s, l, _ in MUSIC], 'silent': [(round(a, 3), round(b, 3)) for a, b in SILENT]}
json.dump(cues, open(os.path.splitext(OUT)[0] + '.cues.json', 'w'), indent=1)
print('mixed', len(DIALOGUE), 'lines,', len(EFFECTS), 'effects,', len(MUSIC), 'music cuts ->', OUT, f'({DUR} s)')
