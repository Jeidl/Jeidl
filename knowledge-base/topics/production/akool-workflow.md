---
id: 20261106-akool-workflow
title: AKOOL 制作流程与 14 天排期
tags: [production, akool]
created: 2026-11-06
updated: 2026-11-07
related: [20261106-reference-sheet-reverse-prompts, 20261106-exhibit-47-scene-images, 20261106-exhibit-47-whitebox-previs, 20261106-challenge-rules, 20261106-character-bible, 20261106-prompt-formula, 20261106-untomorrow-shot-list, 20261106-submission-checklist, 20261106-editing-rhythm, 20261106-black-screen-text-cards, 20261106-music-sfx-prompts, 20261106-sound-design, 20261106-exhibit-47-character-bible, 20261106-exhibit-47-shot-prompts, 20261106-exhibit-47-shot-list, 20261107-exhibit-47-keyframes, 20261107-exhibit-47-video-clips]
summary: 从角色设定图、动态分镜、图生视频、口型与配音，到剪辑、遮幅、AKOOL 标志、混音和导出的十步流程，按 11 月 20 日截止倒排的 14 天日程，以及"AKOOL 使用"的留证方法。
---

# AKOOL 制作流程与 14 天排期

> Summary: 从角色设定图、动态分镜、图生视频、口型与配音，到剪辑、遮幅、AKOOL 标志、混音和导出的十步流程，按 11 月 20 日截止倒排的 14 天日程，以及"AKOOL 使用"的留证方法。

> **主方案《第 47 号证物》**：人物设定见 [人物与道具设定](../concept/exhibit-47-character-bible.md)，镜头见 [镜头提示词库](../prompts/exhibit-47-shot-prompts.md)，分镜见 [分镜表](exhibit-47-shot-list.md)。和下文的区别：画幅用 16:9 证物画面加顶部标题栏（AKOOL 标志放在标题栏里），不加 2.39:1 遮幅；不用 STYLE-A，改用证物风格块。

## 背景

评分里 15% 是"Use of AKOOL"，规则也要求 AKOOL 起"有意义的作用"，提交时还要说明用法。所以：**能在 AKOOL 里做的，都在 AKOOL 里做，并且全程留证。** 具体功能和模型名称以账号内实际可用的为准。

## 《第 47 号证物》的 AKOOL 分工（2026-11-06 更新）

下面的十步流程是按备选方案《明日不来》写的，主方案照同样的步骤做。主方案的实际分工：

| 环节 | 工具 | 状态 |
|---|---|---|
| 设定图（诺拉、沃德的手、第十三人） | LibTV（`nebula-ultra`） | 已完成，见 [人物与道具设定](../concept/exhibit-47-character-bible.md) |
| 图片转提示词、设定图核对 | LibTV 视觉模型（GVLM 3.1、Qwen 3 VL Flash） | 已完成，见 [学习记录](../prompts/reference-sheet-reverse-prompts.md) |
| 场景图（6 个场景的环境参考） | **AKOOL** 图像生成（flux-krea-dev） | 已完成：8 张，24 积分，见 [场景图](../prompts/exhibit-47-scene-images.md) |
| 白模预演（构图、遮挡、动作时机） | Blender 5.2（Python 模块 bpy） | v1 已完成，见 [白模预演](exhibit-47-whitebox-previs.md) |
| 关键帧 v2 · 人物镜头（23 张，画面自带证物画质） | LibTV（Seedream 5.5，中文提示词 + v3 设定图 + 白模） | 已完成（2026-11-07），32 次生成，见 [关键帧](exhibit-47-keyframes.md) |
| 关键帧 v2 · 场景和道具（7 张） | **AKOOL** 图像生成（flux-krea / flux-kontext） | 已完成（2026-11-07）：13 次生成，39 积分 |
| 关键帧 v1（已被 v2 取代，保留作对照） | **AKOOL** 图像生成（flux-kontext-dev） | 已完成（2026-11-07）：30 张选用帧，53 次生成，159 积分，见 [关键帧](exhibit-47-keyframes.md) |
| 图生视频（全部镜头） | **AKOOL** 图生视频（首轮 Akool Premium；第二、三轮 Seedance 1.0 Pro Fast，含 720p；C2 开场 Seedance Lite；I4 用 Kling 3.0 Omni） | 已完成（2026-11-08）：61 条，1210 积分，拼成 85 秒粗剪 v3，见 [图生视频](exhibit-47-video-clips.md) 和 [第二次审片对照](exhibit-47-review-2.md) |
| 配音 V1–V12 | **AKOOL** 配音（`audio_tts`） | 已完成（2026-11-07）：21 句，共约 1.4 积分，选角见 [图生视频](exhibit-47-video-clips.md) |
| 口型同步（I2） | **AKOOL** Talking Photo | 已完成（2026-11-07）：1080p，3.1 秒，15 积分 |
| 音乐（SC1）和音效（18 个） | LibTV（ElevenMusic V3、Seed Audio 1.0）；AKOOL 没有音乐和音效生成 | 已完成（2026-11-07），见 [音乐、音效和混音](exhibit-47-sound-mix.md) |
| 混音（预览版） | 脚本 `previs/clips/tools/soundmix.py`（ffmpeg，按画面帧定位） | 粗剪 v3 已混好：-14.0 LUFS，待人耳试听 |
| 证据文字、屏显 | 脚本 `previs/clips/tools/overlays.py`、`track_plane.py`（后期合成，不靠生成） | 粗剪 v3 已做：登记簿、标签、各设备屏显 |
| 剪辑定稿、字卡、叠字、调色 | 剪辑软件 | 待做 |

**AKOOL 接口状态（2026-11-06）**：

- 订阅前：所有接口返回 `1213 Only subscribed users can use the API functions`。
- 订阅后：**图像生成可用**（场景图就是这样做的）。当时查询积分 `account_credit` 和查询模型 `account_models` 返回 `1009 Your current subscription plan does not support this API feature`。
- **2026-11-07 更新**：这两个接口和图生视频接口都已经能用。实测 5 秒片段的价格是 Akool Premium 8 积分、Seedance 1.0 Pro 75、Kling 3.0 Omni 100，详见 [图生视频](exhibit-47-video-clips.md)。

AKOOL 的图生图只能接一张源图（`source_image`，相似度 `similar` 0–1）。实际做法（2026-11-07）：大部分镜头用**白模同一时间点的灰模帧**做源图（相似度 0.45–0.5），诺拉近景用诺拉 v2 设定图（0.55–0.6），沃德的手用 AKOOL 底图加设定图合成。原因和 10 条教训见 [关键帧](exhibit-47-keyframes.md)。

## 十步流程

### 第 0 步：准备（第 1 天上午）

- 确认 AKOOL 账号等级（$100 参与奖仅限 Premium）。
- 在 AKOOL 视频生成器里确认可用的模型（Veo / Kling / Seedance / Wan 等）和每次生成消耗的额度。
- 建一个**制作日志**表格：`镜头编号 | 模型 | 提示词 | 参考图 | 版本 | 是否选用 | 截图`。这张表就是提交时"如何使用 AKOOL"的证据。

### 第 1 步：锁定角色（第 1 天）

- 用 AKOOL 图像生成，按 [角色圣经](../concept/character-bible.md) 的设定图提示词生成 Ada 设定图。生成 5–10 张，只选 1 张。
- 同样生成守时人的剪影设定图和 Sam 的设定图。
- **定下就不改。**

### 第 2 步：关键帧（第 2–3 天）

- 对 [分镜表](untomorrow-shot-list.md) 里的每个镜头，用参考图 + 提示词先生成一张**静态关键帧**。
- 把关键帧按时间码放进剪辑软件，配上临时音乐，做成**动态分镜**（animatic）。
- **在动态分镜上确认节奏和故事**，再花视频额度。这一步能省掉一半的浪费。

### 第 3 步：图生视频（第 4–8 天）

- 以关键帧为首帧，在 AKOOL 视频生成器里做图生视频。模型分工见 [提示词公式](../prompts/prompt-formula.md)。
- 每个镜头生成 3–4 个版本。文件命名：`S19b_D2_kling_v3.mp4`。
- 先做 P0 镜头，再做 P1、P2（优先级见分镜表）。
- 额度建议：约 60% 留给动作组（D）和时间特效组（E），它们最容易需要重做。

### 第 4 步：对白与口型（第 7–8 天）

- F1、F2 优先用带原生音频和口型同步的模型（如 Veo）直接生成。
- 如果口型不准：用 AKOOL 的配音工具生成台词音频，再用 AKOOL 的口型同步工具贴到画面上。

### 第 5 步：配音与画外音（第 8 天）

- 用 AKOOL 的配音 / 语音工具生成 R1、K1、K2、L3、O1，声音设定见 [音乐与音效提示词](../prompts/music-sfx-prompts.md)。
- 收音机声音：配音生成后加带通滤波。

### 第 6 步：剪辑（第 9–10 天）

- 软件：DaVinci Resolve（免费）、Premiere 或剪映 / CapCut。
- 时间线：1920×1080 或 3840×2160，**24 fps**。
- **2.39:1 遮幅**：1080p 下上下各约 138 像素黑边（1080 − 1920 ÷ 2.39 ≈ 277 像素）。
- 字卡全部在剪辑软件里做，参数见 [黑屏与字卡](../techniques/black-screen-text-cards.md)。
- 倒放镜头（D4、E3）、变速、闪帧都在这一步做，见 [剪辑节奏](../techniques/editing-rhythm.md)。

### 第 7 步：AKOOL 标志（第 10 天）

- 从 AKOOL 官方渠道获取标志文件，**不要自己重画**。
- **两处都放**：片头 2 秒标志卡 + 全片放在**顶部黑边里**的小标志（高度约为画面高度的 4%，白色，不透明度约 80%）。这样同时满足"顶部"和"开头"两种理解，也不会遮挡画面。

### 第 8 步：调色与质感（第 11 天）

- 所有镜头套同一个冷蓝 / 琥珀 LUT，逐个微调肤色。
- 统一叠加一层 35mm 胶片颗粒和轻微光晕。

### 第 9 步：声音与混音（第 11–12 天）

- 按 [声音设计](../techniques/sound-design.md) 的声音设计表铺声音层。
- 响度约 -14 LUFS，真峰值不超过 -1 dBTP。**用手机外放检查一遍。**

### 第 10 步：导出、发布、提交（第 13–14 天）

- 导出 H.264，1080p 或 4K，24 fps，码率 ≥ 20 Mbps。
- 另剪 9:16 竖屏版（改法见分镜表）。
- 按 [提交检查清单](submission-checklist.md) 逐项核对后发布、提交。

## 14 天排期（按 11 月 20 日截止倒排）

| 日期 | 天 | 任务 | 产出 |
|---|---|---|---|
| 11-07 | 1 | 准备 + 锁定角色 | 3 张设定图、制作日志 |
| 11-08–09 | 2–3 | 关键帧 + 动态分镜 | 约 25 张关键帧，75 秒动态分镜 |
| 11-10–14 | 4–8 | 图生视频（P0 → P1 → P2）+ 对白 | 约 80–100 个片段 |
| 11-15 | 9 | 配音 + 粗剪 | 粗剪版 |
| 11-16 | 10 | 精剪 + 字卡 + AKOOL 标志 | 精剪版 |
| 11-17 | 11 | 调色 + 声音设计 | 混音前版本 |
| 11-18 | 12 | 混音 + 找 3 个人试看 | 定稿 |
| 11-19 | 13 | 导出 + 竖屏版 + 发布 | 公开链接 |
| 11-20 | 14 | 提交表单（**留出余量，不要拖到最后一小时**） | 提交确认 |

如果官网确认截止日期是 12 月 20 日，就把第 4–8 天扩展成两周，多做几轮重生成和打磨。

## 留证清单（"Use of AKOOL"）

- AKOOL 界面截图：设定图生成、图生视频、口型同步、配音，每一步至少一张。
- 制作日志表格（提示词 + 模型 + 版本）。
- 一段 30–60 秒的幕后快剪（可选），也可以发到社交媒体增加曝光。

## 来源

- [AKOOL 视频生成器](https://akool.com/apps/video-generator)
- [AKOOL AI Film Challenge 官方页](https://www.akool.com/aifilmchallenge)
- [invideo：AI 角色一致性](https://invideo.io/blog/ai-character-consistency/)

## 相关笔记

- [赛事规则](../brief/challenge-rules.md)：标志与 AKOOL 使用要求。
- [角色与道具圣经](../concept/character-bible.md)：第 1 步的提示词。
- [提示词公式](../prompts/prompt-formula.md)：第 3 步的模型分工。
- [分镜表](untomorrow-shot-list.md)：要做的全部镜头。
- [提交检查清单](submission-checklist.md)：第 10 步。
- [剪辑节奏](../techniques/editing-rhythm.md)：第 6 步的剪法。
