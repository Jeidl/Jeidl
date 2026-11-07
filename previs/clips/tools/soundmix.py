"""Mix dialogue, music and sound effects onto the 88 s rough cut (shot-list times).

    python3 soundmix.py IN.mp4 OUT.mp4 [CLIP_DIR]

IN.mp4    the rough cut (its own audio is ignored)
CLIP_DIR  optional: folder with S1_I2__talk.mp4, for the lip-synced line in the montage

Sources (relative to this file): ../../audio/voice/*.mp3 (AKOOL TTS),
../../audio/sfx/*.mp3 (LibTV Seed Audio), ../../audio/music/SC1_music_bed.mp3 (LibTV ElevenMusic).
Every effect file is peak-normalised to -1 dBFS (see ../../audio/sfx_music.json), so the
gains below are relative levels. An event time is when the effect's hit should land; HIT
holds how far into each file that hit is (default 0.1 s, the generator's lead-in).
The final mix is normalised in two passes (linear) to -14 LUFS with a -2 dBTP ceiling; after AAC
encoding the true peak measures about -1.4 dBTP.
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.normpath(os.path.join(HERE, '..', '..', 'audio'))
VO, FX, MU = A + '/voice/', A + '/sfx/', A + '/music/'
IN, OUT = sys.argv[1], sys.argv[2]
CLIPS = sys.argv[3] if len(sys.argv) > 3 else None
DUR = 88.0
SILENT = [(57.05, 58.45), (70.55, 71.95)]   # shot 20 and shot 23: total silence
HIT = {'FX12a_impact': 0.45, 'FX_whoosh': 0.5, 'FX6_door_breach': 0.22, 'FX12b_braaam': 0.13, 'SC2_riser': 0.0,
       'FX4_compressor': 0.0, 'FX_wind_drone': 0.0}

PHONE = 'highpass=f=350,lowpass=f=3200,acrusher=bits=8:mix=0.25,volume=1.4'
RADIO = 'highpass=f=500,lowpass=f=2800,acrusher=bits=6:mix=0.4,volume=1.5'
ROOM = 'aecho=0.9:0.9:40:0.15'   # in x out gain stays near unity
# silenceremove and areverse drop the timestamps, so every chain ends in asetpts=N/SR/TB
TRIM = 'silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse'

# (time, file, filter) -- dialogue
DIALOGUE = [
    (3.0, 'V1_nora_thirteen', ''),
    (7.6, 'V12_dispatch_emergency', PHONE), (9.0, 'V11_caller_northgate', PHONE), (10.6, 'V12_dispatch_who', PHONE),
    (15.8, 'V2_ward_twelve_officers', ROOM),
    (23.0, 'V5_brandt_count_off', ''), (23.8, 'V6_count_ten', ''), (24.4, 'V6_count_eleven', ''), (25.0, 'V7_nora_twelve', ''),
    (25.9, 'V8_thirteenth_twelve', ''), (26.5, 'V5_brandt_who', ''),
    (31.0, 'V9_reyes_still_recording', RADIO), (35.6, 'V5_brandt_masks', 'acrusher=bits=10:mix=0.3,volume=1.3'),
    (40.2, 'V10_reyes_mine_stays_on', 'highpass=f=200,lowpass=f=5000'),
    (51.6, 'V5_brandt_buried', 'acrusher=bits=9:mix=0.4,volume=1.4'),
    (62.1, 'V3_ward_safe_whisper', 'highpass=f=400,volume=2.2'),
    (72.3, 'V4_ward_safe', ROOM), (86.0, 'V8_thirteenth_twelve', 'highpass=f=500,volume=1.6'),
]

# (time, file, gain, extra filter) -- sound effects, placed from the shot list's sound column
EFFECTS = [
    (0.5, 'FX3_radio', 0.5, ''),
    (2.0, 'FX_wind_drone', 0.55, 'afade=t=out:st=3.5:d=1'),
    (6.0, 'FX12a_impact', 0.55, ''), (14.0, 'FX12a_impact', 0.6, ''),
    (11.5, 'FX6_door_breach', 1.0, ''),
    (18.6, 'FX1_beep', 0.5, ''), (22.6, 'FX1_beep', 0.45, ''),
    (23.2, 'FX10_breath', 0.35, ''), (25.6, 'FX_whoosh', 0.5, ''),
    (27.0, 'FX12b_braaam', 1.0, ''),
    (28.7, 'FX2_dropout', 0.6, ''), (29.5, 'FX2_dropout', 0.6, ''),
    (30.5, 'FX5_curtain', 0.8, ''), (30.8, 'FX3_radio', 0.6, ''),
    (38.0, 'FX12a_impact', 0.6, ''), (39.85, 'FX2_dropout', 0.5, ''),
    (40.3, 'FX1_beep', 0.25, 'atempo=1.5'), (41.0, 'FX1_beep', 0.25, 'atempo=1.5'), (41.7, 'FX1_beep', 0.25, 'atempo=1.5'),
    (44.6, 'FX1_beep', 0.5, ''),
    (45.5, 'FX7_gunshots', 0.95, ''), (46.5, 'FX7_gunshots', 0.8, ''), (47.1, 'FX_flashlight_drop', 0.8, ''),
    (47.5, 'FX7_gunshots', 0.4, 'lowpass=f=2500'),
    (48.5, 'FX_flashbang_ring', 0.9, ''), (49.5, 'FX8_gas_alarm', 0.9, 'afade=t=out:st=3:d=1.5'),
    (50.5, 'FX2_dropout', 0.55, ''), (50.7, 'FX2_dropout', 0.5, ''), (51.0, 'FX2_dropout', 0.5, ''), (51.3, 'FX2_dropout', 0.5, ''),
    (53.0, 'FX10_breath', 0.7, ''), (53.0, 'FX7_gunshots', 0.25, 'lowpass=f=1200'),
    (54.5, 'FX9_steps', 0.6, 'afade=t=out:st=1.2:d=0.3'),
    (56.6, 'FX2_dropout', 0.7, ''), (58.5, 'FX1_beep', 0.6, ''),
    (60.0, 'FX8_gas_alarm', 0.35, 'lowpass=f=3000,afade=t=in:d=0.5,afade=t=out:st=3:d=1.5'),
    (62.4, 'FX2_dropout', 0.5, ''), (63.0, 'FX7_gunshots', 0.45, 'atrim=0:0.8,afade=t=out:st=0.5:d=0.3'),
    (64.5, 'SC2_riser', 1.0, 'atrim=0:6,afade=t=out:st=5.9:d=0.1'),
    (66.0, 'FX12a_impact', 0.7, 'atrim=0:1.2'), (67.33, 'FX12a_impact', 0.7, 'atrim=0:1.2'), (68.54, 'FX12a_impact', 0.7, 'atrim=0:1.2'),
    (72.1, 'FX11_pen', 0.7, ''),
    (79.6, 'FX1_beep', 0.6, ''), (79.6, 'FX12a_impact', 1.0, ''),
    (84.5, 'FX1_beep', 0.4, ''), (85.3, 'FX1_beep', 0.4, ''), (86.1, 'FX1_beep', 0.4, ''), (86.9, 'FX1_beep', 0.5, ''),
]

# (timeline start, source start, length, gain) -- SC1 cut to the trailer's structure
MUSIC = [
    (0.0, 0.0, 27.0, 0.30),     # sparse intro
    (27.5, 35.8, 37.0, 0.38),   # pulse under the investigation and the firefight
    (64.5, 96.4, 6.0, 0.70),    # peak; its own dead stop lands on 70.5
    (72.0, 104.0, 12.5, 0.10),  # quiet tail under I3, I4 and the title
]

inputs, chains = [], []


def add_input(path, pre=None):
    """Add an ffmpeg input and return its index."""
    inputs.extend((pre or []) + ['-i', path])
    return inputs.count('-i') - 1


def at(t, name):
    """adelay in ms so the file's hit lands at time t."""
    return max(0, int(round((t - HIT.get(name, 0.1)) * 1000)))


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
                  (f',{fx}' if fx else '') + f',adelay={int(t*1000)}:all=1,asetpts=N/SR/TB[d{i}]')
    bus['dlg'].append(f'[d{i}]')
if CLIPS and os.path.exists(os.path.join(CLIPS, 'S1_I2__talk.mp4')):
    talk, pre = os.path.join(CLIPS, 'S1_I2__talk.mp4'), ['-ss', '0.2', '-t', '1.5']
    i = add_input(talk, pre)
    chains.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo,volume={level(talk, pre, -17.0)}dB,'
                  f'adelay=64500:all=1,asetpts=N/SR/TB[d{i}]')
    bus['dlg'].append(f'[d{i}]')
for t, name, g, fx in EFFECTS:
    i = add_input(FX + name + '.mp3')
    chains.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo' + (f',{fx}' if fx else '') +
                  f',volume={g},adelay={at(t, name)}:all=1,asetpts=N/SR/TB[f{i}]')
    bus['fx'].append(f'[f{i}]')
for t, s, length, g in MUSIC:
    i = add_input(MU + 'SC1_music_bed.mp3')
    chains.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo,atrim={s}:{s+length},asetpts=PTS-STARTPTS,'
                  f'afade=t=in:d=0.05,afade=t=out:st={length-0.08}:d=0.08,volume={g},adelay={int(t*1000)}:all=1,asetpts=N/SR/TB[m{i}]')
    bus['mus'].append(f'[m{i}]')
i = add_input(FX + 'FX4_compressor.mp3', ['-stream_loop', '-1'])
chains.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{DUR},asetpts=N/SR/TB,volume=0.08[amb]')


def mix(labels, out):
    chains.append(''.join(labels) + f'amix=inputs={len(labels)}:normalize=0:duration=longest,apad=whole_dur={DUR},atrim=0:{DUR}[{out}]')


mix(bus['dlg'], 'dlg0'); mix(bus['fx'], 'fx'); mix(bus['mus'], 'mus0')
chains.append('[dlg0]asplit=2[dlg][dsc]')
chains.append('[mus0][dsc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=350[mus]')
mute = '+'.join(f'between(t,{a},{b})' for a, b in SILENT)
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
print('mixed', len(DIALOGUE), 'lines,', len(EFFECTS), 'effects,', len(MUSIC), 'music cuts ->', OUT)
