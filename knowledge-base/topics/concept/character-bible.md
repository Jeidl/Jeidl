---
id: 20261106-character-bible
title: 角色与道具圣经（一致性锚点）
tags: [concept, prompt, production]
created: 2026-11-06
updated: 2026-11-06
related: [20261106-untomorrow-concept, 20261106-style-anchor, 20261106-prompt-formula, 20261106-akool-workflow, 20261106-untomorrow-shot-list, 20261106-longlegs-teasers, 20261106-exhibit-47-character-bible]
summary: 女主 Ada、守时人、搭档 Sam 和关键道具 / 场景的固定英文描述块（ADA-REF 等），以及角色设定图的生成提示词，保证跨镜头一致。
---

# 角色与道具圣经（一致性锚点）

> Summary: 女主 Ada、守时人、搭档 Sam 和关键道具 / 场景的固定英文描述块（ADA-REF 等），以及角色设定图的生成提示词，保证跨镜头一致。

## 背景

AI 视频的一致性主要靠**固定参考图**，光靠重复提示词不够。做法是：先锁定一张满意的角色图，再生成多角度设定图，之后每个镜头都用"参考图 + 下面这段固定文字"。下面的英文块在所有提示词里**一字不改**地粘贴。

## 角色

### ADA-REF：女主 Ada Lin（林艾达），凶案组警探

```text
Detective Ada Lin, a 34-year-old East Asian woman, sharp tired eyes, a thin scar through her left eyebrow, shoulder-length black hair loosely tied back, dark olive-green wool field coat over a charcoal hoodie, silver wristwatch on her left wrist
```

- 识别点：**左眉疤痕、橄榄绿外套、左腕银表**。这三样在每个镜头里都要能看见至少一样。
- 表演基调：疲惫、平静、像是什么都见过（她已经过了几千次同一天）。

### KEEPER-REF：守时人 The Timekeeper（反派）

```text
The Timekeeper, a tall man in a long black wool overcoat and black leather gloves, his face never visible — always in deep shadow, turned away, or out of focus — holding an antique brass pocket watch on a red silk ribbon
```

- **永远不露脸**。这既是悬疑手法（参考 [长腿](../trailers/longlegs-teasers.md)），也绕开了 AI 人脸一致性的难题。
- 写提示词时始终加上 `face hidden` / `back to camera` / `silhouette`。

### SAM-REF：搭档 Sam Okafor（只出现一次对白）

```text
Detective Sam Okafor, a 55-year-old Black man, short grey beard, brown corduroy jacket, reading glasses hanging on a cord
```

### 醒着的人（互助会群像）

```text
an elderly woman in a knitted red scarf, a nervous young man in a delivery jacket
```

## 道具

| 代号 | 英文描述 | 备注 |
|---|---|---|
| WATCH | `an antique brass pocket watch with a cracked crystal, hands stopped at 23:59, on a red silk ribbon` | 全片唯一的红色主题物 |
| CLOCK | `a vintage black flip clock on a bedside table` | 数字容易生成错，**生成空白翻页卡，剪辑时叠加数字** |
| SCREEN | `a giant blank LED screen on the side of a skyscraper` | 倒计时数字在剪辑里叠加 |
| RADIO | `an old silver transistor radio on a windowsill` | 06:00 播报声源 |

## 场景

| 代号 | 英文描述 |
|---|---|
| CITY | `a snow-covered northern city on New Year's Eve, old stone buildings mixed with glass towers, an elevated train line, a central square with a tall gothic clock tower` |
| APARTMENT | `a small dim apartment, cold blue dawn light through the window, an old TV, papers everywhere` |
| ALLEY | `a narrow brick alley in fresh snow, police lights pulsing red and blue` |
| BASEMENT | `a dim church basement, folding chairs in a circle, one bare bulb` |
| TOWER | `inside the clock tower: iron spiral stairs, giant turning gears, a huge translucent illuminated clock face` |

## 设定图生成提示词（AKOOL 图像生成）

> 注意：下面两条的风格不统一（Ada 是灰色影棚柔光，守时人是黑背景逆光），生成出来会像两套图。如果启用本方案，先按 [《第 47 号证物》人物与道具设定](exhibit-47-character-bible.md) 的"统一规则"改写：共用 SHEET-STYLE 等固定块，Ada 做风格母版，守时人图接母版参考。

**Ada 设定图（4 视图）**

```text
Character reference sheet, photorealistic, neutral grey studio background, soft even lighting. Four views of the same person side by side: front view, three-quarter view, side profile, and a close-up of the face. Detective Ada Lin, a 34-year-old East Asian woman, sharp tired eyes, a thin scar through her left eyebrow, shoulder-length black hair loosely tied back, dark olive-green wool field coat over a charcoal hoodie, silver wristwatch on her left wrist. Consistent identity across all views, natural skin texture, no text, no logo.
```

**守时人剪影设定图**

```text
Character reference sheet, photorealistic, dark studio background with strong backlight. Four views: back view, three-quarter back view, side silhouette, and a close-up of gloved hands holding an antique brass pocket watch on a red silk ribbon. A tall man in a long black wool overcoat and black leather gloves; his face is never visible, lost in shadow. No text, no logo.
```

## 相关笔记

- [风格锚](../prompts/style-anchor.md)：STYLE-A 和 NEG-A 要和本页的角色块一起使用。
- [提示词公式](../prompts/prompt-formula.md)：角色块放在公式里的位置。
- [AKOOL 制作流程](../production/akool-workflow.md)：设定图到图生视频的步骤。
- [分镜表](../production/untomorrow-shot-list.md)：所有镜头都引用本页的代号。
- [核心创意](untomorrow-concept.md)：角色背后的故事。
