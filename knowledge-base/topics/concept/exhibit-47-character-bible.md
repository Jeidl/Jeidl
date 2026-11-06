---
id: 20261106-exhibit-47-character-bible
title: 《第 47 号证物》人物与道具设定（一致性锚点）
tags: [concept, prompt, production]
created: 2026-11-06
updated: 2026-11-06
related: [20261106-exhibit-47-story, 20261106-exhibit-47-shot-prompts, 20261106-exhibit-47-shot-list, 20261106-character-bible, 20261106-style-anchor, 20261106-prompt-formula, 20261106-akool-workflow, 20261106-longlegs-teasers]
summary: 主方案的人物设定（诺拉、沃德、第十三人、布兰特、特勤组、旧录像里的手）、可直接粘贴的英文角色块（NORA-REF 等）、道具与场景块、颜色规则，以及 AKOOL 设定图提示词；沃德在预告里只露手和声音。
---

# 《第 47 号证物》人物与道具设定（一致性锚点）

> Summary: 主方案的人物设定（诺拉、沃德、第十三人、布兰特、特勤组、旧录像里的手）、可直接粘贴的英文角色块（NORA-REF 等）、道具与场景块、颜色规则，以及 AKOOL 设定图提示词；沃德在预告里只露手和声音。

## 背景

故事见 [完整故事](exhibit-47-story.md)。用法与 [《明日不来》角色圣经](character-bible.md) 相同：先锁定一张参考图，之后每个镜头都用"参考图 + 下面的固定英文块"，**一字不改**。

## 预告片的三条铁律

1. **沃德不露脸**。预告里只出现他的**声音**和**右手**。这样既不会剧透，也省掉了一张需要保持一致的脸。
2. **第十三人恰好出现 4 次**，对应结尾字卡"第十三个人出现在 4 个画面里"：楼梯间队尾的剪影、冷冻门镜面里的头盔、拉住诺拉的手、审讯桌上沃德的手。其他镜头里**不能**出现他，具体位置见 [分镜表](../production/exhibit-47-shot-list.md)。
3. **特勤组全员戴面罩**，只有布兰特在"摘面罩"那场戏里露脸。需要保持一致的脸只有**诺拉**一个人。

## 人物与角色块

### NORA-REF：诺拉·凯德（主角，唯一的幸存者）

- **身份**：26 岁，第七特勤组新人，7-12 号；前军医。
- **性格**：安静、警惕、不哭。在审讯室里她不是在崩溃，而是在拼命回忆。
- **识别点**：**下巴上的旧伤疤**、灰色眼睛、短发。

```text
Officer Nora Kade, a 26-year-old woman with a short dark undercut, a thin healed scar along her chin, steady grey eyes, pale skin reddened by cold
```

服装块（按场景加在后面）：

| 代号 | 场景 | 英文 |
|---|---|---|
| NORA-TAC | 突袭 | `wearing black tactical gear and a ballistic helmet with a white stenciled number 7-12, black balaclava pulled down to her chin` |
| NORA-ROOM | 审讯室 | `wearing an oversized grey sweatshirt, a white hospital wristband, frost-reddened knuckles, hair still damp` |
| NORA-DAWN | 走出冷库 | `in black tactical gear covered in frost, carrying her helmet in one hand` |

### WARD-HAND：沃德的右手（预告里只出现这只手）

- **身份**：伊莱亚斯·沃德，54 岁，督察署调查官，也就是第十三个人。
- **声音**：低沉、温和、耐心。他越温柔越可怕。
- **识别点**：**右手背上一道发亮的旧烧伤疤**，从指节延伸到手腕。

```text
the right hand of a man in his fifties, resting on a grey metal table, an old shiny burn scar across the back of the hand from the knuckles to the wrist, the cuff of a charcoal suit jacket, a plain steel wristwatch
```

### THIRTEENTH-REF：第十三人（突袭时的沃德）

```text
a thirteenth tactical officer in identical black tactical gear, ballistic helmet with a white stenciled number 7-12, full black balaclava and dark goggles, face never visible; the glove on his right hand is torn open across the back, revealing an old shiny burn scar
```

- 注意：他的头盔编号**也是 7-12**，和诺拉一样。这是报数时出现两个"十二"的原因。
- 他**从不举枪**。在任何镜头里，他的姿态都是平静站立或缓慢行走。

### BRANDT-REF：科尔·布兰特（组长，只在"摘面罩"和"我们埋了你"两场露脸）

```text
Sergeant Cole Brandt, a 45-year-old man, heavy stubble, bloodshot eyes, balaclava ripped down, black tactical gear, ballistic helmet with a white stenciled number 7-01
```

### UNIT-REF：第七特勤组（群像）

```text
police tactical officers in identical black tactical gear, ballistic helmets with white stenciled numbers, black balaclavas and goggles, rifles with mounted flashlights, plain grey shoulder patches with no insignia
```

**不要出现任何真实警徽或真实机构标志。**

### OLD-HANDS：旧录像里举起的双手（三年前）

```text
the bare hands of a teenager raised high in surrender, the sleeves of a dark hoodie, frost-covered crates behind, harsh flashlight beam on the hands
```

只拍手，**不拍脸**，不出现血腥画面。

## 道具

| 代号 | 英文描述 | 备注 |
|---|---|---|
| EX47 | `a scuffed black police body camera covered in frost, a small glowing red recording light, a faded red cardboard evidence tag tied to it with white string` | **全片唯一的红色主题物**。标签上的字后期叠加 |
| BAGS | `thirteen black body cameras in clear plastic evidence bags laid in a single row on a steel forensic table, twelve with white tags, one with a red tag` | |
| PEN | `a cheap black ballpoint pen` | 按钮镜头里沃德转动它 |
| PIPE | `old refrigeration pipes thick with frost along the ceiling` | 被打穿后喷出白色氨气 |

## 场景

| 代号 | 英文描述 |
|---|---|
| LOC-GATE | `an abandoned harbor cold-storage plant, rusted loading docks and shutters, untouched snow, grey overcast dawn` |
| LOC-STAIR | `a narrow concrete stairwell in total darkness, frost on the railings, breath vapor` |
| LOC-FREEZER | `a vast abandoned freezer hall, rows of empty meat hooks on rails, hanging plastic strip curtains, frosted steel walls, freezing fog drifting at floor level` |
| LOC-ROOM4 | `a small freezer room stacked with frosted wooden crates, a single meat hook, a polished steel door` |
| LOC-INTERVIEW | `a bare police interview room, grey metal table, two chairs, cold flat fluorescent overhead light, a dark one-way mirror` |
| LOC-EVIDENCE | `a forensic evidence room, a long steel table under harsh white LED light, clear plastic evidence bags` |

## 颜色规则

- **唯一的红色属于证物**：EX47 的红色标签、红色录制灯。其他物体都不要出现大面积红色。
- 突袭画面以红外单色（灰绿）和手电冷白光为主；枪口火光是橙白色。
- 审讯室和证物室：冷蓝灰，日光灯。

## 设定图提示词（AKOOL 图像生成）

**诺拉 4 视图设定图**

```text
Character reference sheet, photorealistic, neutral grey studio background, soft even lighting. Four views of the same person side by side: front view, three-quarter view, side profile, and a close-up of the face. Officer Nora Kade, a 26-year-old woman with a short dark undercut, a thin healed scar along her chin, steady grey eyes, pale skin reddened by cold, wearing an oversized grey sweatshirt. Consistent identity across all views, natural skin texture, no text, no logo.
```

**沃德的手（参考图，保证两个镜头里的疤一致）**

```text
Reference sheet, photorealistic macro photography, neutral grey background. Three views of the same right hand of a man in his fifties: back of the hand flat on a table, the hand turning a ballpoint pen, and the same hand in a black tactical glove torn open across the back. An old shiny burn scar across the back of the hand from the knuckles to the wrist, identical in all three views. No text, no logo.
```

**第十三人剪影**

```text
Character reference sheet, photorealistic, dark background with a cold flashlight beam from the side. A tactical officer in black gear, ballistic helmet with a white stenciled number 7-12, full black balaclava and dark goggles, face never visible. Three views: front, side, back. The right glove is torn open across the back of the hand, revealing a burn scar. No text other than the helmet number, no logo.
```

（头盔编号如果生成乱码，就生成空白头盔，后期贴上 7-12。）

## 相关笔记

- [完整故事](exhibit-47-story.md)：人物背后的故事和秘密。
- [镜头提示词库](../prompts/exhibit-47-shot-prompts.md)：所有镜头都引用本页代号。
- [分镜表](../production/exhibit-47-shot-list.md)：第十三人的 4 次出场位置。
- [《明日不来》角色圣经](character-bible.md)：同样的方法，备选方案版本。
- [风格锚](../prompts/style-anchor.md)、[提示词公式](../prompts/prompt-formula.md)：提示词结构。
- [AKOOL 制作流程](../production/akool-workflow.md)：设定图到图生视频的步骤。
- [长腿](../trailers/longlegs-teasers.md)：反派不露脸的参考。
