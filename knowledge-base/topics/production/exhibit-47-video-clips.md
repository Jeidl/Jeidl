---
id: 20261107-exhibit-47-video-clips
title: 《第 47 号证物》AKOOL 图生视频 v1：29 条片段、模型价格对比和无声粗剪 v0
tags: [production, akool, video, prompt]
created: 2026-11-07
updated: 2026-11-07
related: [20261107-exhibit-47-keyframes, 20261106-exhibit-47-shot-prompts, 20261106-exhibit-47-shot-list, 20261106-akool-workflow, 20261106-submission-checklist, 20261106-exhibit-47-whitebox-previs, 20261106-editing-rhythm]
summary: 以 v2 关键帧为首帧，在 AKOOL 里生成了 29 条图生视频（391 积分）。实测 5 秒片段的价格：Akool Premium 8 积分、Seedance 1.0 Pro 75、Kling 3.0 Omni 100。所以主力用 Akool Premium，Kling 只用在 I4 这种需要首尾帧都准的镜头上。B2 的甩镜改为分两段生成、在运动模糊里切过去。全部片段按分镜表拼成了 88 秒的无声粗剪 v0。笔记里有每条的取舍、10 条教训和下一步。
---

# 《第 47 号证物》AKOOL 图生视频 v1：29 条片段、模型价格对比和无声粗剪 v0

> Summary: 以 v2 关键帧为首帧，在 AKOOL 里生成了 29 条图生视频（391 积分）。实测 5 秒片段的价格：Akool Premium 8 积分、Seedance 1.0 Pro 75、Kling 3.0 Omni 100。所以主力用 Akool Premium，Kling 只用在 I4 这种需要首尾帧都准的镜头上。B2 的甩镜改为分两段生成、在运动模糊里切过去。全部片段按分镜表拼成了 88 秒的无声粗剪 v0。笔记里有每条的取舍、10 条教训和下一步。

## 背景

- 日期：2026-11-07。工具：**AKOOL 图生视频**（API，`video_image2video_create`）。
- 首帧：[关键帧 v2](exhibit-47-keyframes.md) 的 30 张。AKOOL 生成的帧直接用 AKOOL CDN 链接；LibTV 生成的帧直接用 LibTV 的原图链接（2736×1536 PNG），AKOOL 能读，不用转存。只有本地修过的 C2 首帧是用 `file_upload` 传上去的。
- 账户积分：开始时 970，现在 579。图生视频一共生成 29 次，花了 **391 积分**。
- 接口状态：订阅前查询模型（`account_models`）返回 1009，现在已经能用，图生视频可以全部走 API，不用网页端。

## 模型和价格（实测，5 秒一条）

| 模型 | 积分 | 分辨率 | 尾帧 | 实际表现 |
|---|---|---|---|---|
| **Akool Premium**（AkoolImage2VideoHDV1） | **8** | 1080p | 不支持 | 大部分镜头都可用，40–90 秒出片。**主力** |
| Seedance 1.0 Pro | 75 | 1080p | 支持 | B2 没有落到尾帧：结尾的第十三人换了衣服，身后还多了人 |
| Kling 3.0 Omni | 100 | 只有 720p | 支持 | I4 首尾帧都很准，表情变化细腻 |
| Akool Basic、Seedance Lite、Hailuo 2.3、Sora 2 / 2 Pro | 没测 | — | Seedance Lite 支持 | 先不花这个钱 |

有尾帧的三个模型里，经 AKOOL 调用时只有 Kling 真正停在了尾帧上。

## 做法

**提示词只写动作和镜头运动**，画面内容已经在首帧里了。结构是三部分：

1. 机位和运动（"Locked-off security camera, no camera movement" / "Body-worn camera rushing forward…"）
2. 动作，写清谁在动、往哪个方向、动作有多大
3. 一句画质（"Keep the body-worn camera look: fisheye distortion, dark corners, heavy noise and compression, flashlight bloom."）

**负面词**：text, letters, numbers, timestamp, POLICE lettering, logo, watermark, visible blood, morphing bodies, extra limbs, cartoon, video game graphics。再按镜头加上不要的动作，例如 I3 加 "turning the hand over, scar disappearing"。

**B2 甩镜不用首尾帧**：首帧（队员下楼）和第十三人帧各生成一段，两段共 16 积分。第二段开头自带甩镜的运动模糊，剪辑时在模糊里切过去，看不出接缝。比 Seedance 首尾帧（75 积分、还失败了）便宜，也更稳。

## 片段表

| 镜头 | 模型 | 结果 | 粗剪用 |
|---|---|---|---|
| D1 | Akool Premium | 无人机缓慢升高，她走离冷库，脚印在身后 ✅ | ✅ |
| C3 | Akool Premium | 监控固定，人从车里下来，雪，院子没有脚印 ✅ | ✅ |
| B1 | Akool Premium | 门被撞开，强光和冷雾涌出，队员冲进去 ✅ | ✅ |
| I1 | Akool Premium | 她一动不动；机位有轻微漂移，剪辑时稳定一下 ✅ | ✅ |
| E1 | Akool Premium | 沿桌面推到最近的证物袋 ✅ | ✅ |
| B2 | Seedance 1.0 Pro（首尾帧） | 前 2.5 秒对，结尾没落到尾帧 ❌ | — |
| B2 第一段 | Akool Premium | 队员下楼；最后没有甩镜，甩镜用下一段补 ✅ | ✅ |
| B2 第二段 | Akool Premium | 从甩镜模糊里停到一动不动的第十三人，胸前红灯 ✅ | ✅ |
| B3 | Akool Premium | 穿过门帘，两名队员背对镜头走进雾里 ✅ | ✅ |
| B4 | Akool Premium | 队员互相用手电照，布兰特冲向镜头嘶吼 ✅ | ✅ |
| O2 | Akool Premium | 队员伸手按胸前的记录仪；偏黄的旧录像感比关键帧弱 ✅ | ✅ |
| E3 登记簿 | Akool Premium | 画面稳定，但没有甩镜，甩镜在剪辑里做 ✅ | ✅ |
| E3 标签 | Akool Premium | 推向红灯 ✅ | ✅ |
| B5 | Akool Premium | 开头一次橙色枪口火光，之后偏蓝；只用第一秒 ⚠️ | ✅ |
| B9 | Akool Premium | 门帘后的人倒下，手电掉地 ✅ | ✅ |
| C1 | Akool Premium | 监控俯视，雾里几处火光 ✅ | ✅ |
| B10 | Akool Premium | 闪光弹烧白，曝光恢复后是两个剪影 ✅ | ✅ |
| B6 | Akool Premium | 管道喷气灌满走廊，队员踉跄 ✅ | ✅ |
| B7 | Akool Premium | 布兰特嘶吼，向镜头逼近 ✅ | ✅ |
| X1 | Akool Premium | 镜头平稳前进，四周慌乱 ✅ | ✅ |
| B8 首帧 | Akool Premium | 走过大厅、转向镜面门板，没有人 ✅ | ✅ |
| B8 倒影 | Akool Premium | 第十三人静止，红灯亮着；有点像隔着玻璃门，后期加镜面反光 ⚠️ | ✅ |
| C2 首帧 | Akool Premium | 气体从门口涌进来，效果好；但它是 AKOOL 做的托盘间，和抓人那条的木箱间不是同一个布景 ⚠️ | 只放进监控墙 |
| C2 抓背心 | Akool Premium | 手抓住她，门框闪光，把她拉进箱子后面 ✅ | ✅（4.5 秒全用这一条） |
| I3 第一条 | Akool Premium | 手拿起笔翻过来，1 秒后疤就看不见了 ❌ | — |
| I3 重拍 | Akool Premium | 手一直平放，疤始终朝着镜头，只有手指在滚笔 ✅ | ✅ |
| I4 | Kling 3.0 Omni（首尾帧） | 先低头，再慢慢抬眼认出他，和首尾帧完全吻合 ✅ | ✅ |
| E2 | Akool Premium | 证物袋轻晃，标签转动，红灯常亮；标签最后转成侧面，用前 3 秒 ✅ | ✅ |
| O1 | Akool Premium | 举起的双手在手电光里发抖 ✅ | ✅ |

**第十三人**：B2 第二段、B8 倒影、C2 抓人里都看不到脸；I3 的疤从头到尾都看得见。

## 粗剪 v0（无声）

按 [分镜表](exhibit-47-shot-list.md) 的时间码，把上面的片段拼成了 **88.0 秒**的无声粗剪：

- **字卡**：用的是占位字体，AKOOL 卡也是占位，要换成官方标志。
- **监控墙**：用 12 条片段拼成 4×3，按分镜表逐格变成 SIGNAL LOST。
- **闪切蒙太奇**：用关键帧静帧加片段拼成。
- **I2**：先用静帧占位，等口型同步做完再换。

文件是 `previs/clips/roughcut_v0_540p.mp4`，可以用 `tools/roughcut.py` 重新生成。它只用来看节奏和衔接，还没有调色、叠字和声音。

## 10 条教训

1. **先测价格再铺量**：同样 5 秒，Akool Premium 8 积分，Seedance 1.0 Pro 75，Kling 3.0 Omni 100。先各跑一条，看 `deduction_credit`，再定主力模型。
2. **经 AKOOL 调用的 Seedance Pro 不保证落到尾帧**；Kling 3.0 Omni 落得准。首尾帧镜头只给 Kling，或者改成两段拼接。
3. **甩镜、转场用两段拼接**：各生成一段，在运动模糊里切，便宜也稳（B2）。
4. **Akool Premium 基本不执行"最后一秒做某个动作"这种时间点指令**（B2 第一段、E3 登记簿都没有甩镜）。这类动作留给剪辑。
5. **手部特写把动作写小**：写"手平放不动，只有指尖动，手背和疤始终朝向镜头"；否则手会翻过来，疤就丢了（I3）。
6. **"固定机位"仍然会轻微漂移**（I1、E1）。监控画面在剪辑里稳定一下或轻微放大裁切。
7. **同一个镜头的首帧必须是同一个布景**：C2 首帧（AKOOL 托盘间）和抓人帧（LibTV 木箱间）接不上。不同工具做的帧要先放在一起对一遍。
8. **关键帧里的画质在视频里会变弱**（O2 的偏黄和噪点变轻）。调色时统一补一层颗粒和压缩感，不用重新生成。
9. **主体单一、动作明确的镜头效果最好**（B4、B7、B10、C2 抓人）；"同时发生好几件事"的镜头（B5 连续枪口火光）只能做出一部分。
10. **LibTV 原图链接可以直接当首帧**，省掉转存和上传；但本地修过的图要用 `file_upload` 传到 AKOOL。

## 下一步

1. **I2 口型同步和配音**：用 AKOOL 配音生成诺拉的 "There were thirteen of us."，再用口型同步（或 talking photo）贴到 S1 I2 上。V1–V12 的配音也在 AKOOL 里做。
2. **C2 的开头**：两种做法。一是在 LibTV 里，用抓人帧的同一个木箱间生成一张"空房间、气体刚涌进来"的首帧，再用 Akool Premium 生成（约 8 积分）。二是用 Kling 3.0 Omni，从这张空房间帧做首尾帧到抓人帧（100 积分）。
3. **重拍候选**（每条 8 积分）：B5（要更多连续火光）、B8 倒影（更像镜面）、O2（更旧的画质）。
4. **监控墙素材池 P1–P6** 还没有单独生成，现在的监控墙借用了其他镜头。
5. **剪辑**：AKOOL 官方标志、正式字卡和叠字（编号、时间戳、REC、标签文字）、调色、颗粒、声音设计和混音，按 [AKOOL 制作流程](akool-workflow.md) 的第 6–9 步来。
6. **积分**：剩 579。上面 1–4 全做完约需 50–150 积分，用不用 Kling 决定是哪一头。

## 文件

`previs/clips/`：

- `clips_v1.json`：29 次生成的完整日志。每条记了模型、分辨率、时长、积分、首帧和尾帧链接、提示词、负面词、AKOOL 任务号、视频链接、取舍，以及是否用在粗剪里（`selected`）。提交时它就是"如何使用 AKOOL"的制作日志。
- `strips/`：每条片段的 6 帧缩略图。
- `roughcut_v0_540p.mp4`：无声粗剪 v0。
- `tools/fetch_clips.py`：按日志把片段下载到本地。
- `tools/roughcut.py`：重新拼粗剪。

视频原片（1920×1080，24 fps）都在 AKOOL 的 CDN 上，链接见日志，仓库里不存原片。

## 相关笔记

- [关键帧 v2](exhibit-47-keyframes.md)：这些片段的首帧。
- [镜头提示词库](../prompts/exhibit-47-shot-prompts.md)：每个镜头的完整描述和后期叠字规范。
- [分镜表](exhibit-47-shot-list.md)：粗剪用的时间码。
- [AKOOL 制作流程](akool-workflow.md)：图生视频在整个流程里的位置。
- [提交检查清单](submission-checklist.md)：`clips_v1.json` 是 AKOOL 使用记录的一部分。
- [剪辑节奏](../techniques/editing-rhythm.md)：甩镜、闪切这些在剪辑里怎么做。
