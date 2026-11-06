---
id: 20261106-exhibit-47-scene-images
title: 《第 47 号证物》场景图（AKOOL 生成）：风格块、提示词、选用版本与问题
tags: [prompt, visual, akool]
created: 2026-11-06
updated: 2026-11-06
related: [20261106-exhibit-47-whitebox-previs, 20261106-exhibit-47-shot-prompts, 20261106-exhibit-47-character-bible, 20261106-akool-workflow, 20261106-reference-sheet-reverse-prompts]
summary: 用 AKOOL 图像生成（flux-krea-dev）为 6 个场景各出一张环境参考图：统一的 SCENE-STYLE 风格块和 NEG-SCENE 负面词、6 条场景提示词、实际选用的版本和 AKOOL 任务号、每张图和设定不一致的地方，以及用户整理的即梦搜索词。白模按这些图搭建。
---

# 《第 47 号证物》场景图（AKOOL 生成）：风格块、提示词、选用版本与问题

> Summary: 用 AKOOL 图像生成（flux-krea-dev）为 6 个场景各出一张环境参考图：统一的 SCENE-STYLE 风格块和 NEG-SCENE 负面词、6 条场景提示词、实际选用的版本和 AKOOL 任务号、每张图和设定不一致的地方，以及用户整理的即梦搜索词。白模按这些图搭建。

## 背景

搭白模之前，先给每个场景定一张"长什么样"的环境参考图。白模的纵深、建筑密度和房间比例都按这些图来定，见 [白模预演](../production/exhibit-47-whitebox-previs.md)。

- 生成工具：**AKOOL 图像生成**（接口 `image_create`，模型 `wavespeed-ai/flux-krea-dev-lora`；图生图走 `flux-kontext-dev`），1080p，16:9，每张 3 积分。共生成 8 张，用了 24 积分。
- 账号已订阅。**图像生成接口可用**；查询积分、查询模型列表这两个接口仍返回 `1009 Your current subscription plan does not support this API feature`。
- 图片已存进仓库：`previs/scene_refs/`。

## SCENE-STYLE（每张场景图的开头，一字不改）

```text
Photorealistic location photograph for film production design, an empty real place with no people. Shot on a full-frame camera with a 24mm lens at f/8, deep focus, sharp from foreground to background. Motivated natural light only, true-to-life colors in a cold steel-blue and grey palette, medium contrast, no color grading, no film grain, rich surface detail. Clear depth layers: a distinct foreground, middle ground and background.
```

结尾统一加：`No people, no text, no readable signs, no logos, no watermark.`（审讯室和证物室再加 `no police insignia`。）

**NEG-SCENE**（AKOOL 的 `negative_prompt`）

```text
people, person, figure, text, letters, signage, logo, watermark, cartoon, anime, illustration, 3D render, CGI look, video game, oversaturated colors, fisheye distortion, blurry, low resolution
```

场景图和设定图（SHEET-STYLE）一样，**只管空间长什么样**；画面风格交给镜头的 S-* 风格块。

## 6 张场景图

| 场景 | 文件 | AKOOL 任务号 | 主体段要点 | 结果 |
|---|---|---|---|---|
| LOC-GATE 外景 | `ext_v1.jpg` | `6aed945907a5c75b64e82f94` | 无人机高位俯视、近处锈门和铁丝网、约 35 m 雪地、冷库正面、两侧仓库和集装箱、远处海和吊车 | ✅ 选用。⚠️ 雪地上有从门口到装卸口的**车辙**（D1 要求"未踩过的雪"）；建筑比设定小（约 35 m 宽），只有 1 个敞开的装卸口和 2 个卷帘门 |
| LOC-GATE 外景 v2 | — | `6aed95202bee4c1ef42949f7` | 以 v1 为源图做图生图（相似度 0.55），要求去掉车辙 | ❌ 弃用：车辙还在，天空出现噪点 |
| LOC-STAIR 楼梯间 | `stair_v1.jpg` | `6aed94712bee4c1ef42943b7` | 顶部平台往下看、窄楼梯、结霜扶手、左墙高窗 | ✅ 选用。直跑约 12 级后向右转 |
| LOC-FREEZER 冷冻大厅 | `hall_v1.jpg` | `6aed947107a5c75b64e830a0` | 站立视角看长厅、两排肉钩、柱子、管道、左侧门帘、右侧冷冻间门、地面冷雾 | ✅ 选用。左墙是挂着透明帘的大窗（不是门帘入口） |
| LOC-ROOM4 4 号冷冻间 | `room4_v1.jpg` | `6aed94712bee4c1ef42943c1` | 高角、结霜木箱、中间矮一点的箱堆、单个肉钩、镜面推拉门 | ✅ 选用。视角几乎就是 C2 的监控机位 |
| LOC-INTERVIEW 审讯室 | `interview_v1.jpg` | `6aed947107a5c75b64e830aa` | 高角、灰色金属桌和两把椅子、左墙单向玻璃、右侧门、日光灯 | ✅ 选用。桌子是**纵向**摆的，两把椅子隔桌相对，单向玻璃在左侧椅子背后 |
| LOC-EVIDENCE 证物室 v1 | — | `6aed94722bee4c1ef42943cd` | 沿长桌看一排证物袋 | ❌ 弃用：袋子里是**单反相机**，不是执法记录仪；红标签位置也不对 |
| LOC-EVIDENCE 证物室 v2 | `evidence_v2.jpg` | `6aed952007a5c75b64e83613` | 同上，把"执法记录仪"写成"小黑盒、一个小圆镜头、背夹，不是相机"，负面词加 DSLR | ✅ 选用。⚠️ 红标签在**离镜头最近**的那一袋，不在最远处 |

## 学到的写法

1. **道具要描述形状，不要只写名字**。只写 `police body cameras`，模型会画成单反；写成"小黑盒、一个圆镜头、背夹、不是相机"并在负面词里加 `DSLR camera, photo camera` 才对。
2. **"第几个"这种顺序关系模型守不住**。"最后一袋是红标签"两次都没做对。需要靠白模和剪辑解决（E1 改成从远端往近端推），或者以后用图生图局部修改。
3. **图生图去不掉大面积的东西**。flux-kontext 在相似度 0.55 下没能去掉车辙。要改就降低相似度重出，或者在镜头提示词里写死 `untouched snow`。
4. **数量和尺寸会被模型"缩小"**。写了 60 m 宽、6 个卷帘门，出来是约 35 m、3 个开口。白模按图做，不按文字做。

## 即梦搜索词（用户整理，需要时再搜）

| 场景 | 英文 | 中文 |
|---|---|---|
| 冷库外景 | `harbor warehouse loading dock snow night`、`rusted roller shutter loading dock` | 港口仓库 雪夜、废弃仓库 卷帘门 卸货平台 |
| 楼梯间 | `dark concrete stairwell abandoned`、`SWAT team stack stairwell` | 废弃楼梯间、特警 楼梯 战术队形 |
| 审讯室 | `police interview room fluorescent`、`interrogation room one-way mirror` | 审讯室 日光灯、询问室 单向玻璃 |
| 证物室 | `body camera in evidence bag`、`forensic evidence table` | 证物袋 执法记录仪、证物室 |
| 画面质感 | `body camera footage night vision`、`CCTV infrared warehouse` | 执法记录仪 画面、监控 红外 夜视 |

搜到的图**只学措辞**，不当参考图、首帧或成片素材（见 [图片转提示词学习记录](reference-sheet-reverse-prompts.md)）。

## 相关笔记

- [白模预演](../production/exhibit-47-whitebox-previs.md)：按这 6 张图搭的白模、机位和发现的问题。
- [镜头提示词库](exhibit-47-shot-prompts.md)：做关键帧时，场景图和设定图一起当参考。
- [人物与道具设定](../concept/exhibit-47-character-bible.md)：SHEET-STYLE 和场景图的分工。
- [AKOOL 制作流程](../production/akool-workflow.md)：这批图是 AKOOL 参与制作的第一批留证。
- [图片转提示词学习记录](reference-sheet-reverse-prompts.md)：即梦搜图的规则。
