---
id: 20261106-prompt-formula
title: AI 视频提示词公式与模型选择（AKOOL 上的 Veo / Kling / Seedance / Wan）
tags: [prompt, akool]
created: 2026-11-06
updated: 2026-11-06
related: [20261106-style-anchor, 20261106-character-bible, 20261106-shot-prompt-library, 20261106-akool-workflow, 20261106-editing-rhythm]
summary: 九段式通用提示词公式、六条硬规则、各模型在 AKOOL 上的长处与分工、镜头和运镜词汇表、多镜头写法，以及常见翻车的修法。
---

# AI 视频提示词公式与模型选择（AKOOL 上的 Veo / Kling / Seedance / Wan）

> Summary: 九段式通用提示词公式、六条硬规则、各模型在 AKOOL 上的长处与分工、镜头和运镜词汇表、多镜头写法，以及常见翻车的修法。

## 背景

AKOOL 的视频生成器集成了多个第三方模型（官方页面列出 Kling、Veo、Seedance、Wan、MiniMax 等，具体版本以账号内为准）。下面的公式综合了 Veo 3.1、Kling 3.0、Seedance 2.0 的第三方提示词指南。这些都不是官方文档，**先用便宜的模型小规模测试**。

## 九段式公式

```
[STYLE-A]                        ← 风格锚（固定不变）
+ 景别 + 镜头焦段                 ← Extreme close-up, 100mm macro lens
+ 运镜（只写一个）                ← slow dolly-in / static / tracking
+ 主体（角色块）                  ← [ADA-REF]
+ 动作（一个动词）+ 物理细节       ← catches the mug mid-fall; coat flaring
+ 环境                           ← a dim apartment kitchen at dawn
+ 光线 + 色彩                     ← cold blue window light, amber lamp
+ 声音                           ← Sound: radio voice "…", soft whoosh
+ 时长 / 画幅                     ← 6 seconds, 16:9
+ [NEG-A]                        ← 负面词（模型支持时放进负面词框）
```

## 六条硬规则

1. **一个镜头只写一种运镜**。多个运镜会导致画面抖动、动作错乱。
2. **一个镜头只写一个主要动作**。10 秒内写太多动作，画面会变得卡顿。
3. **写具体的镜头术语**，不要写"很酷的运镜"。
4. **声音要明确写出来**。不写的话，Veo 这类有原生音频的模型会生成无声或随机音效。台词用英文引号，并写明是谁说的。
5. **台词控制在 12 个英文单词以内**，口型同步最可靠。
6. **不写导演名、演员名、电影名、品牌名**。用画面特征来描述。

## 模型分工（据第三方对比，以 AKOOL 账号内实际可用为准）

| 模型 | 长处 | 本片用来做 |
|---|---|---|
| **Veo 3.x** | 写实质感、原生音频、口型同步，最高 4K；时长 4 / 6 / 8 秒档 | 对白镜头（F 组）、人脸特写（A2）、按钮镜头（G1） |
| **Kling 3.x / 4.x** | 多镜头叙事（一次最多 6 个镜头共享音轨），约 10 秒 | 动作蒙太奇（D 组）、追逐 |
| **Seedance 2.x** | 多参考图驱动（第三方称最多 9 张图 + 3 段视频 + 3 段音频），角色一致性 | 需要 Ada 跨镜头一致的镜头 |
| **Wan** | 成本低 | 构图、运镜的草稿测试 |

## 词汇表

| 类别 | 英文 |
|---|---|
| 景别 | extreme wide shot, wide shot, medium shot, medium close-up, close-up, extreme close-up, macro |
| 焦段 | 18mm（超广）、24mm、35mm（叙事）、50mm（标准）、85mm（人像）、100mm macro |
| 运镜 | static / locked-off, slow dolly-in, push-in, pull-out, tracking shot, lateral tracking, crane up / down, tilt up, whip pan, handheld, steadicam follow, aerial drone glide, top-down |
| 速度 | slow motion (120fps), time-lapse, speed ramp, frozen |
| 光线 | backlit silhouette, rim light, practical lights, volumetric light, sodium-vapor streetlights, single hard key light, chiaroscuro |
| 构图 | symmetrical, one-point perspective, centered subject, negative space, low angle, high angle, Dutch angle |
| 质感 | fine film grain, halation, anamorphic lens flare, shallow depth of field |

## 多镜头写法（Kling 多镜头 / Seedance 时间轴）

```text
[STYLE-A] Multi-shot sequence, 10 seconds total, one action per shot, consistent character and lighting.
Shot 1 (0–2s): tracking shot — [ADA-REF] sprints across a snowy rooftop at night.
Shot 2 (2–5s): low-angle slow motion — she leaps the gap between two buildings.
Shot 3 (5–7s): close-up — she lands hard, rolls, snow bursting around her.
Shot 4 (7–10s): wide — she rises and looks up at the clock tower in the distance.
Sound: wind, footsteps, a heavy percussion hit on every cut.
```

规则：每个镜头标注时间，**总和等于总时长**；Kling 最多 6 个镜头。第三方指南提到，Seedance 写了运镜时，可能需要在设置里选择"不固定镜头"才会生效（未经官方证实）。

## 先图后视频（推荐流程）

1. 用图像生成做出该镜头的**关键帧**（便宜、快、可以反复改）。
2. 选出最好的一张，作为**首帧**做图生视频。
3. 首帧方式在动作复杂时容易漂移，所以**中等幅度、时长短的动作最稳**。

## 常见翻车与修法

| 现象 | 修法 |
|---|---|
| 脸在镜头里变了 | 加参考图；缩短时长；换成背影或剪影 |
| 手指变形 | 让手握着东西（怀表、手电、枪）；避免手部特写里的复杂动作 |
| 画面里出现乱码文字 | 加 `no text, no subtitles, no signage`；文字一律后期叠加 |
| 动作像慢放的果冻 | 只写一个动作；写清物理细节（重量、速度、惯性） |
| 运镜不动 | 写成 `the camera slowly dollies in`，主语用 camera；检查"固定镜头"设置 |
| 颜色每个镜头都不一样 | 固定 STYLE-A；后期统一 LUT |
| 雪 / 烟花糊成一片 | 写 `crisp individual snowflakes`，搭配 `shallow depth of field` |

## 来源

- [AKOOL 视频生成器](https://akool.com/apps/video-generator)
- [atlabs：Veo 3.1 提示词指南](https://www.atlabs.ai/blog/the-ultimate-prompting-guide-for-veo-3-1)
- [Easton Dev：Veo 3 五步公式](https://eastondev.com/blog/en/posts/ai/20251204-veo3-prompt-writing-guide/)
- [atlabs：Kling 3.0 提示词指南](https://www.atlabs.ai/blog/kling-3-0-prompting-guide-master-ai-video-generation)
- [Morphic：Kling 3.0 指南](https://morphic.com/resources/how-to/kling-3.0-guide)
- [MindStudio：Seedance 2 时间轴提示](https://www.mindstudio.ai/blog/timeline-prompting-seedance-2-cinematic-ai-video)
- [Fliki：Seedance 2.0 提示词指南](https://fliki.ai/blog/seedance-2-prompting-guide)
- [heyuan110：Seedance 2.0 最佳实践与失败模式](https://www.heyuan110.com/posts/ai/2026-07-11-seedance-2-prompt-guide/)
- [WaveSpeed：Seedance 2.0 / Kling 3.0 / Sora 2 / Veo 3.1 对比](https://wavespeed.ai/blog/posts/seedance-2-0-vs-kling-3-0-sora-2-veo-3-1-video-generation-comparison-2026/)
- [invideo：锚帧法](https://invideo.io/blog/anchor-frame-method-ai-video/)

## 相关笔记

- [风格锚](style-anchor.md)：STYLE-A 和 NEG-A 的全文。
- [角色与道具圣经](../concept/character-bible.md)：ADA-REF 等角色块。
- [镜头提示词库](shot-prompt-library.md)：按本公式写好的全部镜头。
- [AKOOL 制作流程](../production/akool-workflow.md)：在 AKOOL 里操作的步骤。
- [剪辑节奏](../techniques/editing-rhythm.md)：生成后怎么剪。
