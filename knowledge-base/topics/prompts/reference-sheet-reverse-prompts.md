---
id: 20261106-reference-sheet-reverse-prompts
title: 设定图的图片转提示词学习记录（反推、交叉核对与即梦搜图清单）
tags: [prompt, visual, akool, copyright]
created: 2026-11-06
updated: 2026-11-06
related: [20261106-exhibit-47-character-bible, 20261106-exhibit-47-shot-prompts, 20261106-prompt-formula, 20261106-akool-workflow, 20261106-challenge-rules, 20261106-submission-checklist]
summary: 用 LibTV 的两个视觉模型（GVLM 3.1、Qwen 3 VL Flash）对已通过的设定图做"图片转提示词"，交叉核对后锁定背景、分隔线、手套、疤等细节；记录反推提问模板、四条经验、第十三人设定图的验收结果、即梦搜图的手动清单，以及比赛规则（原创、AKOOL 参与）的注意事项。
---

# 设定图的图片转提示词学习记录（反推、交叉核对与即梦搜图清单）

> Summary: 用 LibTV 的两个视觉模型（GVLM 3.1、Qwen 3 VL Flash）对已通过的设定图做"图片转提示词"，交叉核对后锁定背景、分隔线、手套、疤等细节；记录反推提问模板、四条经验、第十三人设定图的验收结果、即梦搜图的手动清单，以及比赛规则（原创、AKOOL 参与）的注意事项。

## 背景

诺拉 v2 和沃德的手 v2 通过验收后，要做第十三人设定图，要求是"提示词必须明确"。原计划是去即梦 AI 搜相关图片，用图片转提示词学习写法。

实际情况：

- **即梦打不开**：本次云端会话的网络策略拦截了 `jimeng.jianying.com`；而且即梦的搜索要登录抖音 / 即梦账号，代理不能替你登录。所以即梦部分改成手动清单，见下文。
- **改用 LibTV 画布里的视觉模型**做图片转提示词：把已通过的设定图接进文本节点，让模型反推。对第十三人图来说，这比学别人的图更直接：要对齐的就是这两张。

## 方法：两个模型交叉核对

| 节点 | 模型 | 用途 |
|---|---|---|
| `t-ECZnOgZgl0` | GVLM 3.1（`aurora-3-prime`） | 风格反推：共同风格、逐格描述、疤和手套细节、可复用的风格提示词、词汇表 |
| `t-W75ItSgh23` | Qwen 3 VL Flash（`qwen-3-vl-flash`） | 逐项问答复核：格数、分隔线、底部条、白平衡、手套指型、笔、疤、手表 |
| `t-7rosh1s9EH` | Qwen 3 VL Flash | 第十三人 v2 验收复核（和沃德的手 v2 对比） |
| `t-N6UehWuJvr` | GVLM 3.1 | 第十三人 v2 二次复核：头盔编号、底部条、臂章 |
| `t-ecOnJbteWC` | Qwen 3 VL Flash | 第十三人 v2.1 验收（和沃德的手 v2 对比） |
| `t-9D7AbfMWGa` | GVLM 3.1 | 第十三人 v2.1 验收：文字、底部条、臂章、武器 |

都在 LibTV 项目"EXHIBIT 47 第47号证物"里，节点里有完整的提问原文和回答。

**反推提问模板**（可复用，`<图>` 换成参考图的引用）：

```text
<图> is attached. Answer each question in English with a short factual answer based only on what you can see. If you cannot tell, write "unclear".
1. How many separate panels does it contain? Describe each panel in one line (view angle, crop, which way the subject faces).
2. Gutters: colour and width. Is there any bar, border, footer, caption or text?
3. Background: colour and estimated grey value 0-255, texture, gradient.
4. Light: direction, softness, shadows on the backdrop. White balance: warm, neutral or cool?
5. Describe every identifying detail precisely (scar, glove, watch, clothing): shape, size, position, colour, texture.
6. Any extra or missing fingers, distorted limbs, or the subject changing between panels?
```

规则：**用"问答式"，不要只让模型"写一段提示词"**。问答能逼模型逐项看图；只让它写提示词，它会套用常见词，例如下面的 macro photography。

## 反推结果

| 项目 | GVLM 3.1 | Qwen 3 VL Flash | 结论 |
|---|---|---|---|
| 诺拉 v2 格数 | 1 格，正面胸像 | 1 格，正面胸像 | ⚠️ 两个模型一致：**不是四视图**。人工已验收通过，但请再确认一次 |
| 手部 v2 格数 | 4 格 | 4 格 | 一致 |
| 背景 | 平整、无缝、哑光中灰，约 140 / 255 | 中灰，约 128–140 | 一致 |
| 分隔线 | 白色，约 1% 宽 | 白色细线 | 一致。提示词写的是 light-grey，模型实际出的是白色 → SHEET-LAYOUT 改为 white |
| 底部条 | 手部图底部有灰色条 | 没有 | 不一致 → 提示词加 `No footer bar, no border` |
| 光线 | 正前上方柔光，阴影很少 | 左前方柔光，背景无投影 | 基本一致 |
| 白平衡 | 手部图偏暖 | 两张一致，中性 | 不一致 → 继续写 neutral daylight |
| 手套 | 黑色哑光半指，粗魔术贴腕带；手背椭圆破洞，边缘毛糙 | 半指，宽魔术贴腕带；指节处椭圆开口，边缘整齐 | 半指 + 腕带一致 → 锁定；破口边缘以人工看为准 |
| 烧伤疤 | 不规则长条，约 5–6 cm × 1 cm，沿中指掌骨，粉白斑驳，隆起发亮 | 不规则长条，约占手背 1/3，从手腕伸向中指，粉白，隆起发亮 | 基本一致 → 锁定 |
| 手表 | 银色金属链表带 | 银色链带，白 / 银色表盘 | 一致 |
| 笔 | 透明塑料 | 黑色 | 不一致，以人工看为准（设定是黑色 PEN） |
| 第 1 格是哪只手 | 没说 | 说是左手 | ⚠️ 待人工确认（俯拍时模型常把左右手弄反） |

锁定后的细节写进了 [人物与道具设定](../concept/exhibit-47-character-bible.md) 的"已锁定的细节"和 WARD-GLOVE 块。

## 第十三人 v2 的验收结果（节点 `i-5bwnmb06HT`）

参考图：沃德的手 v2。提示词：人物设定里的"③ 第十三人（明确版）"。

| 检查项 | 结果 |
|---|---|
| 4 格：正面全身 / 四分之三 / 右侧轮廓 / 手套特写 | ✅ |
| 背景、光线、白平衡、清晰度和手部图一致 | ✅（Qwen 判断一致） |
| 脸、皮肤、眼睛完全不露 | ✅ |
| 不拿武器、没有枪套 | ✅ |
| 没有徽章、标志、红色 | ✅ |
| 手套和疤与手部图第 4 格一致 | ✅（Qwen 判断"相同"） |
| 手指和肢体正常、四格是同一个人 | ✅ |
| 头盔编号是 7-12 | ❌ Qwen 读出正面是 "01"，GVLM 读出侧面是 "1-12"。01 是布兰特的编号，不能用 |
| 没有底部条 | ❌ 两个模型都看到底部有一条灰色横条（约 10% 高） |
| 臂章是浅灰色、无图案 | ❌ 两个模型都说是黑色 |

**修正：v2.1（节点 `i-OM9iRyuQJu`）**。以 v2 为参考图做一次局部修改：去掉头盔上所有文字，按人物设定里的预案改成空白头盔，后期贴 7-12；臂章改成浅灰；去掉底部条。结果：

| 检查项 | Qwen 3 VL Flash | GVLM 3.1 | 结论 |
|---|---|---|---|
| 头盔和画面里没有任何文字 | 没有 | 没有 | ✅ |
| 臂章 | 浅灰，有隐约的方形，无可读内容 | 浅灰 / 银色，无图案 | ✅ |
| 底部条 | 还在，浅灰，约 5–8% 高 | 还在，浅灰，约 13% 高 | ❌ 没去掉。可能是背景纸的地面弧度；后期裁掉或保留都行，**裁之前先确认不会切到靴子** |
| 武器 / 枪套 | 右大腿有枪套 | 没有武器 | ⚠️ 不一致，**请人工看**；如果只是腿包，可以接受 |
| 脸、眼睛 | 不露 | 只有第 4 格手上露出皮肤 | ✅ |
| 红色 | 没有 | 没有 | ✅ |
| 手套和疤与手部图一致 | 一致 | — | ✅ |
| 和手部图的背景、光线、白平衡、分隔线 | 一致 | — | ✅ |

到这一步不再盲改：剩下的两项要人眼判断。如果需要重做，只改有问题的那一项，其他句子不动。

## 四条经验

1. **反推是第二双眼睛**。它能发现人眼验收漏掉的问题：格数不对、左右手、底部条、头盔编号。但单个模型会看错，**至少用两个模型**；结论不一致的项，人工再看。
2. **模型会自由发挥你没写死的细节**。分隔线写浅灰出了白色；手套没写指型，出了半指。所以"明确"的意思是：每个可能被自由发挥的细节都写成一个确定值。写法标准见人物设定里的"明确写法"表。
3. **反推出来的提示词不能直接粘贴**。GVLM 反推的风格句里出现了 `macro photography`，这正是 v1 风格不统一的原因。反推结果要先过一遍禁用词。
4. **文字类细节最不可靠**。头盔编号要求 7-12，生成出了别的数字。凡是要读得出来的文字，都按"空白头盔 + 后期贴字"处理，不要指望模型写对。

## 即梦搜图清单（需要你登录后手动做）

如果想补充学习，可以在即梦里按下面的关键词搜，把好的提示词写法记到本页：

| 学什么 | 搜索词 |
|---|---|
| 战术人物全身设定 | `特警 全身 三视图 灰色背景`、`战术装备 角色设定图 写实` |
| 面罩和护目镜 | `战术面罩 护目镜 头盔 写实 摄影` |
| 半指手套 | `半指战术手套 魔术贴 特写` |
| 手背烧伤疤 | `手背 烧伤疤痕 特写 写实` |
| 设定图版式 | `角色四视图 摄影棚 灰色背景 写实` |

步骤：

1. 挑和我们风格一致的图：灰色无缝背景、正面柔光、全清晰、不调色。
2. 如果作品页显示了原提示词，就记下来；否则用任意图片转提示词工具（或 LibTV 的 GVLM 3.1 文本节点）配合上面的反推提问模板。
3. 只把**措辞**记到本页，标明来自即梦。

## 比赛规则注意

- **原创**：即梦上的图是别人的作品。**只学措辞，不要下载它们当参考图、首帧或成片素材**。我们的参考图只用自己生成的设定图。
- **AKOOL 必须起"有意义的作用"**：2026-11-06 实测，AKOOL 接口对当前账号返回 `1213 Only subscribed users can use the API functions`，所以三张设定图都在 LibTV 生成。规则允许同时用其他 AI 工具，但 AKOOL 要承担主要的制作环节。订阅之后，关键帧、图生视频、口型和配音都放到 AKOOL 里做，分工见 [AKOOL 制作流程](../production/akool-workflow.md)。$100 参与奖也只限 Premium 账号。
- **留证**：提交时如实写明设定图用 LibTV 生成、图片转提示词用 LibTV 的视觉模型，见 [提交检查清单](../production/submission-checklist.md)。

## 相关笔记

- [人物与道具设定](../concept/exhibit-47-character-bible.md)：固定块、三张设定图的提示词、已锁定的细节。
- [镜头提示词库](exhibit-47-shot-prompts.md)：C2 等镜头用 WARD-GLOVE 块。
- [提示词公式](prompt-formula.md)：通用写法。
- [AKOOL 制作流程](../production/akool-workflow.md)、[赛事规则](../brief/challenge-rules.md)、[提交检查清单](../production/submission-checklist.md)：AKOOL 参与和留证。
