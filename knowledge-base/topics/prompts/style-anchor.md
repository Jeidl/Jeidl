---
id: 20261106-style-anchor
title: 风格锚 STYLE-A / 负面词 NEG-A / 场景色彩块
tags: [prompt, style]
created: 2026-11-06
updated: 2026-11-06
related: [20261106-style-decision, 20261106-prompt-formula, 20261106-character-bible, 20261106-visual-motifs, 20261106-blade-runner-2049]
summary: 每条提示词都要原样粘贴的英文 / 中文风格锚、负面词，以及每个场景的固定色彩光线块，保证全片质感统一。
---

# 风格锚 STYLE-A / 负面词 NEG-A / 场景色彩块

> Summary: 每条提示词都要原样粘贴的英文 / 中文风格锚、负面词，以及每个场景的固定色彩光线块，保证全片质感统一。

## 用法

- 本知识库里所有提示词中的 `[STYLE-A]`、`[NEG-A]`、`[ADA-REF]`、`[KEEPER-REF]`、`[SAM-REF]` 都是占位符。**粘贴前替换成下面的原文**（角色块见 [角色圣经](../concept/character-bible.md)）。
- 风格锚**一字不改**。改一个词，整片的质感就会漂移。

## STYLE-A（英文，推荐）

```text
Photorealistic live-action cinematic footage, shot on 65mm large-format film with anamorphic lenses, composed for a 2.39:1 widescreen crop, fine film grain and soft halation, cold steel-blue night palette with warm sodium-amber practical lights and a single accent of red, high contrast with deep inky blacks, soft volumetric haze, light snowfall, grounded realism, restrained composition, prestige psychological thriller tone.
```

## STYLE-A-CN（中文，可用于 Kling / Seedance 等支持中文的模型）

```text
写实真人电影画面，65mm 大画幅胶片拍摄，变形宽银幕镜头，按 2.39:1 宽银幕构图，细腻胶片颗粒与柔和光晕，冷峻钢蓝色夜景配钠灯琥珀暖光，唯一的点缀色是红色，高反差，深邃的黑色，柔和的体积雾，轻微飘雪，写实克制的构图，高级心理惊悚片质感。
```

## STYLE-A-SHORT（字数受限时用）

```text
Photorealistic cinematic film, 65mm anamorphic, film grain, cold steel-blue and sodium-amber palette, single red accent, high contrast, haze, snow, psychological thriller.
```

## NEG-A（负面词）

```text
cartoon, anime, illustration, 3D render, CGI look, video game graphics, plastic skin, waxy face, oversaturated colors, on-screen text, subtitles, captions, signage text, watermark, logo, distorted hands, extra fingers, warped face, face morphing, identity change, flicker, jitter, low resolution, blurry, overexposed
```

不支持负面词框的模型，就在正向提示词末尾写：`No text, no logos, no subtitles. Stable face and hands.`

## 场景色彩块（LOC-*）

把对应场景的色彩块加在环境描述之后，保证"一地一色"（见 [银翼杀手2049](../trailers/blade-runner-2049.md)）。

| 代号 | 场景 | 色彩块 |
|---|---|---|
| LOC-DAWN | 公寓清晨 | `cold pale-blue dawn light through a frosted window, deep shadows, one small warm lamp` |
| LOC-STREET | 街道、广场 | `warm sodium-amber streetlights, blue-black sky, falling snow catching the light` |
| LOC-ALLEY | 凶案小巷 | `pulsing red and blue police lights on wet brick, white breath vapor` |
| LOC-SUBWAY | 地铁通道 | `cold flickering fluorescent white, green-tinted tiles, haze` |
| LOC-BASEMENT | 教堂地下室 | `a single bare tungsten bulb, hard shadows, darkness at the edges` |
| LOC-TOWER | 钟楼内部 | `amber backlight through a huge translucent clock face, dust in light beams, silhouettes` |
| LOC-ROOF | 屋顶追逐 | `near-total darkness lit only by red firework glow on the snow` |

## 红色规则

**红色只属于"时间"**：怀表的红丝带、烟花、红色信号弹、警灯。其余物体不要出现大面积红色。如果模型给 Ada 加了红围巾这类东西，就在负面词里加 `red clothing`。

## 来源

- [Easton Dev：Veo 3 提示词公式（风格与技术参数结合）](https://eastondev.com/blog/en/posts/ai/20251204-veo3-prompt-writing-guide/)
- [invideo：AI 角色一致性（固定风格块）](https://invideo.io/blog/ai-character-consistency/)

## 相关笔记

- [风格定向](../brief/style-decision.md)：为什么是这种风格。
- [提示词公式](prompt-formula.md)：风格锚在公式里的位置。
- [角色与道具圣经](../concept/character-bible.md)：角色块。
- [视觉母题](../techniques/visual-motifs.md)：色彩母题。
- [银翼杀手2049](../trailers/blade-runner-2049.md)：一地一色的来源。
