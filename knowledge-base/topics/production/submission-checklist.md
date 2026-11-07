---
id: 20261106-submission-checklist
title: 提交检查清单
tags: [production, akool, copyright]
created: 2026-11-06
updated: 2026-11-07
related: [20261106-reference-sheet-reverse-prompts, 20261106-challenge-rules, 20261106-akool-workflow, 20261106-withholding-mystery, 20261106-meta-endings, 20261106-exhibit-47-shot-list, 20261107-exhibit-47-keyframes, 20261107-exhibit-47-video-clips]
summary: 发布和提交前逐项勾选：时长、原创性、AKOOL 标志、版权素材、平台发布与话题标签、提交表单说明、评分自查。
---

# 提交检查清单

> Summary: 发布和提交前逐项勾选：时长、原创性、AKOOL 标志、版权素材、平台发布与话题标签、提交表单说明、评分自查。

## 硬性要求（任何一项不满足都可能被拒）

- [ ] 已在官网再次确认**截止日期**（11-20 还是 12-20）和规则原文
- [ ] 时长在 **30–90 秒**之间（主版本 1:29，为 90 秒上限留 1 秒余量；导出后用播放器确认时长）
- [ ] 是**完整成片**，没有占位镜头或测试画面
- [ ] 电影概念是**原创**的：没有现有 IP 的角色、世界观、商标
- [ ] **AKOOL 标志**：片头标志卡 ✓，全片顶部小标志 ✓，清晰可见
- [ ] AKOOL 在制作中起了**有意义的作用**，有截图和制作日志为证
- [ ] 所有**音乐**是自己生成或演奏的，没有使用受版权保护的歌曲或录音
- [ ] 所有**字体**是可商用许可（如 Google Fonts 的 OFL）
- [ ] 没有使用**真人肖像**（名人、他人的脸）
- [ ] 使用的是有效的 AKOOL 账号（想拿 $100 参与奖需要 Premium）

## 发布

- [ ] 发布在 YouTube / TikTok / Instagram 至少一个平台，设为**公开**，并保持公开到比赛结束
- [ ] 话题标签：`#AKOOLClash #AKOOLFilmChallenge #AIVideo #AIFilm`
- [ ] @AKOOL
- [ ] 标题：`EXHIBIT 47 — Official Trailer (Coming Never) | #AKOOLFilmChallenge`
- [ ] 简介第一行钩子："12 officers went in. 1 came out. 13 cameras were recovered."
- [ ] 简介第二段放片里删掉的三张说明卡（v2 起不在成片里，见 [分镜表](exhibit-47-shot-list.md)）："Every shot in this film is evidence. The case is still open. The thirteenth appears in 4 shots. Watch again."
- [ ] 置顶评论提问："Did you find all 4 shots?"（第 4 次是一道疤，不是一个人）
- [ ] 简介注明虚构作品："A fictional trailer for the AKOOL AI Film Challenge. All characters, agencies and events are fictional."（证物型结尾必须有，见 [元结尾字卡库](../techniques/meta-endings.md)）

## 提交表单

- [ ] 作品链接
- [ ] 选择 **Coming Never** 赛道
- [ ] "如何使用 AKOOL"的说明，建议结构：
  1. 角色设定：**如实写工具**。目前三张设定图是 LibTV 生成、用 LibTV 视觉模型核对的（见 [学习记录](../prompts/reference-sheet-reverse-prompts.md)）；如果订阅后在 AKOOL 里重做了，就写 AKOOL
  2. 画面：**如实写工具**。现行关键帧是 v2：有人的镜头 23 张在 LibTV 生成，场景和道具 7 张在 AKOOL 生成（13 次，39 积分）；C2 首帧在本地擦掉了 AKOOL 自己加的字框。制作日志是 `previs/keyframes/v2/keyframes_v2.json`，见 [关键帧](exhibit-47-keyframes.md)。更早的 v1（53 次 AKOOL 生成）可以作为探索过程一并说明。图生视频全部在 AKOOL 里做：29 次生成（391 积分），主力是 Akool Premium，I4 用 Kling 3.0 Omni，B2 首尾帧试过 Seedance 1.0 Pro。日志是 `previs/clips/clips_v1.json`，见 [图生视频](exhibit-47-video-clips.md)。⚠️ 关键帧里 AKOOL 的比重降低了，所以**图生视频、口型同步、配音都要在 AKOOL 里做**，并且每一步截图，才能撑住 15% 的"Use of AKOOL"
  3. 对白：AKOOL 口型同步 / 配音
  4. 其他工具：剪辑软件、音乐工具（如实列出）
- [ ] 准备好补充材料（截图、制作日志），以备主办方索取

## 评分自查（找 3 个没看过剧本的人试看）

| 维度 | 自查问题 | 合格标准 |
|---|---|---|
| Story 30% | 看完能复述规则吗？ | 能说出"12 个人进去、1 个人出来、多了一台死人的记录仪" |
| Originality 20% | 有没有一个"没见过"的瞬间？ | 两个"十二"、12 格全黑后亮起的第 13 格 |
| Creative Execution 20% | 有没有明显的 AI 穿帮？ | 没有人提到"脸变了"或"手指怪" |
| Use of AKOOL 15% | 说明清楚吗？ | 有截图和制作日志 |
| I'd watch that 15% | 想看正片吗？ | 至少 2 / 3 的人问"第十三个人是谁"，或者主动重看找那 4 个画面 |

## 相关笔记

- [赛事规则](../brief/challenge-rules.md)：每一条的出处。
- [AKOOL 制作流程](akool-workflow.md)：留证方法和排期。
- [关键帧 v1 / v2](exhibit-47-keyframes.md)：关键帧的制作日志和任务号。
- [《第 47 号证物》分镜表](exhibit-47-shot-list.md)：主方案的时长与重看彩蛋。
- [留白与悬念营销](../techniques/withholding-mystery.md)：发布文案。
