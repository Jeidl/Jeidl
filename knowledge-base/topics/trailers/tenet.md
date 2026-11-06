---
id: 20261106-tenet
title: 《信条 Tenet》预告（2019 / 2020）
tags: [trailer, nolan, visual, time-loop]
created: 2026-11-06
updated: 2026-11-06
related: [20261106-visual-motifs, 20261106-inception, 20261106-edge-of-tomorrow, 20261106-untomorrow-shot-list, 20261106-shot-prompt-library]
summary: 子弹飞回枪膛、先有弹孔后有枪战、翻车再翻回来：用"倒放物理"制造奇观，用一句"别去理解它，去感受它"取代解释。
---

# 《信条 Tenet》预告（2019 / 2020）

> Summary: 子弹飞回枪膛、先有弹孔后有枪战、翻车再翻回来：用"倒放物理"制造奇观，用一句"别去理解它，去感受它"取代解释。

## 为什么值得学

- 标志性画面：**子弹飞回枪里**；人物查看一面布满弹孔的玻璃，而造成弹孔的枪战**还没有发生**；车祸后的车**倒着恢复原状**。
- 预告强调"逆转"（inversion）而不是"时间旅行"，用台词 "Don't try to understand it. Feel it."（别去理解它，去感受它）主动拒绝解释。
- 倒放只作用于局部物体或局部人物，因此概念"难以捉摸"，这种难以捉摸本身就是卖点。

## 关键片段拆解

| 段落 | 画面 / 声音 | 作用 |
|---|---|---|
| 规则暗示 | 一句"接住"子弹的台词 + 子弹回到枪中 | 一个镜头讲清"这个世界物理是反的" |
| 谜题 | 先有弹孔、后有枪战 | 制造"因果倒置"的思考 |
| 奇观 | 翻车再翻回来 | 动作片里加入新的视觉语法 |
| 拒绝解释 | "Don't try to understand it. Feel it." | 把困惑变成邀请 |

## 可复用技法

1. **局部倒放**：画面里只有一个物体在倒放，其余正常。比整段倒放更诡异。
2. **先果后因**：先拍结果（弹孔、尸体、停止的怀表），再暗示原因。
3. **用台词把"看不懂"变成卖点。**

## 迁移到《明日不来》

- Ada 开枪，子弹飞出后**停在半空**，和静止的雪花悬在一起：时间在午夜前冻结。
- 烟花在钟楼上方**倒着收回**成上升的火箭。
- AI 生成倒放镜头的技巧：**先生成正向动作，在剪辑软件里倒放**，比让模型直接生成"倒放"稳定得多。

## 提示词

```text
[STYLE-A] Close-up, 50mm lens, slight slow motion. [ADA-REF] fires her pistol in a snowy street at night; the bullet leaves the barrel with a flash — then stops dead in mid-air a meter in front of her, hanging motionless among frozen snowflakes, while her breath vapor is also frozen. Her eyes move; nothing else does. Sound: gunshot cut short into total silence. 5 seconds. [NEG-A]
```

```text
[STYLE-A] Wide shot, 24mm lens, static camera. Fireworks burst in a cold night sky above a gothic clock tower and a crowded snowy square, golden sparks blooming outward. Sound: deep firework booms, crowd cheering. 6 seconds. [NEG-A]
（剪辑时倒放，即得到"烟花倒收回火箭"）
```

## 来源

- [Yahoo：Tenet 的"逆转"到底是什么](https://www.yahoo.com/entertainment/tenet-exactly-time-inversion-thing-033207322.html)
- [Inverse：Tenet 第二支预告解读](https://www.inverse.com/entertainment/tenet-trailer-2-explained)
- [ScreenRant：Tenet 预告拆解](https://screenrant.com/tenet-movie-trailer-breakdown-story-reveals-questions/)

## 相关笔记

- [视觉母题](../techniques/visual-motifs.md)：倒放物理和冻结时间。
- [盗梦空间](inception.md)：同一导演"不解释奇观"的前作。
- [明日边缘](edge-of-tomorrow.md)：时间循环动作片。
- [分镜表](../production/untomorrow-shot-list.md)：子弹停滞镜头的位置。
- [镜头提示词库](../prompts/shot-prompt-library.md)：更多时间特效提示词。
