---
id: 20261106-black-screen-text-cards
title: 黑屏与字卡：用"黑"讲故事
tags: [text-card, editing]
created: 2026-11-06
updated: 2026-11-06
related: [20261106-text-card-copy, 20261106-trailer-structure, 20261106-sound-design, 20261106-inception, 20261106-sicario, 20261106-cloverfield-teaser, 20261106-oppenheimer-teaser, 20261106-fincher-cover-song-teasers, 20261106-longlegs-teasers]
summary: 黑屏的六种功能、字卡的七种类型、排版参数（字体 / 字号 / 字距 / 停留帧数）、免费可商用字体，以及为什么字卡绝不能让 AI 生成。
---

# 黑屏与字卡：用"黑"讲故事

> Summary: 黑屏的六种功能、字卡的七种类型、排版参数（字体 / 字号 / 字距 / 停留帧数）、免费可商用字体，以及为什么字卡绝不能让 AI 生成。

## 背景

黑底白字是犯罪惊悚类型的惯例：黑色代表危险和神秘，白色代表脆弱，两者的对比本身就在制造紧张。你要的"黑屏、引人思考"，在技术上就是**黑屏 + 字卡 + 静默**的组合。

## 黑屏的六种功能

1. **呼吸**：两段高能之间让观众缓一口气。
2. **提问**：黑屏 + 一句话 = 观众被迫思考这句话。
3. **标点**：台词之后黑一下，等于句号。
4. **期待**：黑屏越久，观众越想知道下一个画面。
5. **藏拙**：AI 镜头的开头和结尾最容易出问题，用黑屏切掉。
6. **省钱**：一张字卡顶一个镜头，零生成成本。

## 字卡的七种类型

| 类型 | 例子 | 来源 |
|---|---|---|
| 句子阶梯 | 一句话拆成 4–5 张卡，穿插在镜头之间 | 大片预告通用 |
| 定义句 | "In Mexico, 'sicario' means hitman." | [边境杀手](../trailers/sicario.md) |
| 标语 | "Your mind is the scene of the crime." | [盗梦空间](../trailers/inception.md) |
| 日期卡 | 只有 "1-18-08"，没有片名 | [科洛弗档案](../trailers/cloverfield-teaser.md) |
| 数字 / 倒计时 | 实时倒计时 | [奥本海默](../trailers/oppenheimer-teaser.md) |
| 密码 | 可被破解的符号 | [长腿](../trailers/longlegs-teasers.md) |
| 反讽卡 | 卡上的文字和画面相反 | 芬奇前导（[翻唱三部曲](../trailers/fincher-cover-song-teasers.md)） |

我们的文案见 [字卡文案库](../prompts/text-card-copy.md)。

## 排版参数（直接照抄）

| 参数 | 数值 |
|---|---|
| 背景 | 纯黑 `#000000`（或极深的冷蓝 `#05070A`） |
| 文字颜色 | 略带暖意的白 `#EDE8E0`。纯白显得刺眼、冷冰冰 |
| 字体 | 衬线大写（庄重）**或**窄无衬线大写（冷峻），全片只用一种 |
| 字号 | 约为画面高度的 3–4%（1080p 下约 36–44 px） |
| 字距 | +150 到 +250 |
| 位置 | 正中央，或在 2.39:1 遮幅画面的中线 |
| 入 | 6–8 帧淡入，或在重音上硬切出现 |
| 停留 | 每 3 个英文单词约 1 秒，最短 18 帧 |
| 出 | 硬切到下一个镜头（配声音重音），或 6 帧淡出 |
| 闪帧 | 字卡之间插 2–4 帧画面（见 [长腿](../trailers/longlegs-teasers.md)） |

## 免费可商用字体（Google Fonts，SIL OFL 许可）

| 字体 | 风格 | 适合 |
|---|---|---|
| **Cinzel** | 罗马碑文衬线 | 片名、西幻方案 |
| **Cormorant Garamond** | 优雅衬线 | 字卡正文（推荐） |
| Playfair Display | 高对比衬线 | 标语 |
| **Oswald** | 窄无衬线 | 冷峻科幻、日期卡（推荐） |
| Bebas Neue | 粗窄无衬线 | 动作片 |
| Noto Serif SC / 思源宋体 | 中文衬线 | 中文字卡 |

## ⚠️ 字卡绝不能让 AI 生成

AI 视频模型生成文字时，极易出现乱码、错字和闪烁。**所有字卡、日期、倒计时数字、片名都在剪辑软件里做**（Premiere / DaVinci / CapCut），AI 只负责生成画面。提示词里要加 `no text, no subtitles`。

## 黑屏时长

| 用法 | 时长 |
|---|---|
| 句子阶梯之间的黑 | 6–12 帧 |
| 带字卡的黑屏 | 1–1.5 秒 |
| **片名前的"大黑"**（倒数到 1 之后） | **1.5–2 秒，完全静音** |

## 来源

- [Type Network：ScreenFonts 2017 年 8 月](https://typenetwork.com/articles/screenfonts-august-2017)
- [Film Editing Pro：预告剪辑分析（日期卡与音乐切换）](https://www.filmeditingpro.com/?p=30353)
- [SlideShare：Se7en 预告分析（黑白对比的含义）](https://www.slideshare.net/slideshow/se7en-analysis-1/77172862)

## 相关笔记

- [字卡文案库](../prompts/text-card-copy.md)：可直接使用的文案。
- [预告结构](trailer-structure.md)：字卡放在哪一幕。
- [声音设计](sound-design.md)：字卡配什么声音。
- [盗梦空间](../trailers/inception.md)、[边境杀手](../trailers/sicario.md)、[科洛弗档案](../trailers/cloverfield-teaser.md)、[奥本海默](../trailers/oppenheimer-teaser.md)、[芬奇翻唱前导](../trailers/fincher-cover-song-teasers.md)、[长腿](../trailers/longlegs-teasers.md)：字卡样本。
