---
id: 20261106-music-sfx-prompts
title: 音乐、音效与配音提示词
tags: [prompt, music, sound]
created: 2026-11-06
updated: 2026-11-06
related: [20261106-music-strategy, 20261106-sound-design, 20261106-text-card-copy, 20261106-fincher-cover-song-teasers, 20261106-sicario, 20261106-us]
summary: 《友谊地久天长》温暖版 / 扭曲版配乐、悬疑垫底音、16 种音效清单，以及每个角色的配音声音设定提示词。
---

# 音乐、音效与配音提示词

> Summary: 《友谊地久天长》温暖版 / 扭曲版配乐、悬疑垫底音、16 种音效清单，以及每个角色的配音声音设定提示词。

## 背景

为什么用《友谊地久天长》、哪些曲子有版权，见 [音乐策略](../techniques/music-strategy.md)。下面的提示词适用于常见的 AI 音乐 / 音效 / 配音工具。**使用前先确认工具的商用许可。**

## 配乐

**M1 温暖版（第一幕）**
```text
A gentle, nostalgic music-box arrangement of the traditional public-domain melody "Auld Lang Syne" in a major key; antique music box, soft celesta and glockenspiel; cozy New Year's Eve warmth with a faint melancholy; 72 BPM; 25 seconds; instrumental, no vocals.
```

**M2 扭曲版（第二幕后半 → 第三幕）**
```text
The traditional "Auld Lang Syne" melody reharmonized in a dark minor key for a psychological thriller trailer: low pizzicato strings, a relentless cello ostinato, dissonant violin swells, deep taiko and orchestral percussion hits every bar, a wordless choir entering at the climax; starts at 72 BPM and accelerates to 110 BPM; ends abruptly on a cut to silence; 35 seconds; instrumental.
```

**M3 悬疑垫底音（全片底层）**
```text
Cinematic thriller underscore: a slow, menacing sub-bass pulse at 54 BPM, like something breathing beneath the earth; low bowed double bass, distant metallic scrapes, a faint ticking clock woven into the rhythm; no melody; dark, oppressive, restrained. 75 seconds, instrumental.
```

**M4 无词女声合唱（坠落 / 冻结人群）**
```text
A dissonant, eerie wordless female choir holding clustered chords, slowly rising in pitch, cathedral reverb, sacred and terrifying, no lyrics, no percussion, 15 seconds.
```

**M5 片名钢琴音**
```text
A single very low piano note struck hard and left to ring, with a long dark reverb tail and a faint music-box echo of the first four notes of "Auld Lang Syne" underneath. 6 seconds.
```

## 音效清单

| # | 音效 | 生成提示词 / 做法 |
|---|---|---|
| S1 | 慢滴答 | `antique pocket watch ticking slowly at 54 beats per minute, close-up, dry` |
| S2 | 倒放滴答 | 用 S1 在剪辑软件里倒放 |
| S3 | BRAAAM | `massive low brass and synthesizer BRAAAM hit, cinematic trailer, long tail` |
| S4 | 升调 | `cinematic riser, rising strings and synth, 6 seconds, ending in a hard stop` |
| S5 | 抽空 | `reverse cymbal swell into sudden silence` |
| S6 | 翻页钟 | `vintage flip clock card flipping, crisp mechanical clack` |
| S7 | 收音机压缩人声 | 用 AKOOL 配音生成 R1，再加带通滤波（300–3000 Hz）和少量失真 |
| S8 | 唱片减速 | 把 M1 的结尾在剪辑软件里变速到 20% 并降调 |
| S9 | 雪地脚步 | `slow footsteps crunching on fresh snow, quiet night, close` |
| S10 | 枪声截断 | `single pistol gunshot, cut off abruptly after 3 frames` |
| S11 | 玻璃碎裂 | `glass skylight shattering, debris falling, cinematic` |
| S12 | 人群倒数 | `huge New Year's Eve crowd chanting a countdown from ten to one in unison, outdoors, reverb` |
| S13 | 灯泡开关 | `old light switch clack, bare tungsten bulb buzzing` |
| S14 | 远处教堂钟 | `distant church bell single toll, cold winter air, reverb` |
| S15 | 冲击重音 | `deep cinematic impact boom with sub-bass, trailer hit` |
| S16 | 倒放呼啸 | `reverse whoosh, airy, 1 second` |

## 配音（AKOOL 配音 / 语音工具，以账号内可用为准）

| 角色 | 声音设定提示词 |
|---|---|
| 收音机主持人 | `Cheerful middle-aged male radio host, warm, slightly old-fashioned, bright and upbeat, American accent` |
| Ada | `Tired woman in her thirties, low, calm, flat delivery, quiet intensity, slight rasp` |
| Sam | `Gravelly man in his fifties, weary, warm, slightly confused` |
| 守时人 | `Calm, soft-spoken man, intimate whisper very close to the microphone, gentle, almost compassionate, unsettlingly kind` |

台词全文见 [字卡文案库](text-card-copy.md)。

## 来源

- [Rareform Audio：好莱坞预告的声音设计](https://www.rareformaudio.com/blog/sound-design-in-film-trailers)
- [The Film Stage：Jóhann Jóhannsson 的 Sicario 配乐](https://thefilmstage.com/news/listen-to-johann-johannssons-full-score-for-denis-villeneuves-sicario/)

## 相关笔记

- [音乐策略](../techniques/music-strategy.md)：为什么这样选曲。
- [声音设计](../techniques/sound-design.md)：每个音效用在哪里。
- [字卡文案库](text-card-copy.md)：台词全文。
- 样本：[芬奇翻唱前导](../trailers/fincher-cover-song-teasers.md)、[边境杀手](../trailers/sicario.md)、[我们](../trailers/us.md)。
