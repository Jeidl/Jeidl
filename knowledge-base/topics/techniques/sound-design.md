---
id: 20261106-sound-design
title: 声音设计：BRAAAM、静默、滴答与声音押韵
tags: [sound, editing]
created: 2026-11-06
updated: 2026-11-06
related: [20261106-music-strategy, 20261106-music-sfx-prompts, 20261106-inception, 20261106-a-quiet-place, 20261106-civil-war, 20261106-godzilla-2014, 20261106-sicario, 20261106-10-cloverfield-lane]
summary: 预告常用的八种声音武器（BRAAAM、Ping、升调、抽空、倒放、次低频、声音押韵、有源音乐变调）的用法，以及《明日不来》的声音设计表。
---

# 声音设计：BRAAAM、静默、滴答与声音押韵

> Summary: 预告常用的八种声音武器（BRAAAM、Ping、升调、抽空、倒放、次低频、声音押韵、有源音乐变调）的用法，以及《明日不来》的声音设计表。

## 背景

预告的"高级感"一半来自声音。AI 生成的画面再好，配上平庸的声音也会显得廉价。声音也是最便宜的升级手段。

## 八种声音武器

| 武器 | 是什么 | 怎么用 | 样本 |
|---|---|---|---|
| **BRAAAM** | 低沉的铜管 / 合成器轰鸣 | 一句关键台词之后立刻接上，打标点 | [盗梦空间](../trailers/inception.md) |
| **Ping** | 一个钢琴单音 | 安静段落的"心跳"，和 BRAAAM 是同一思路的高频版 | Rareform Audio 的分析 |
| **升调（Riser）** | 越来越高、越来越密的音 | 推向高潮，结尾突然断掉 | 倒数段 |
| **抽空（Suck-out）** | 所有声音瞬间消失 | 高潮前或"时间停止"的瞬间 | [寂静之地](../trailers/a-quiet-place.md) |
| **倒放（Reverse）** | 声音倒着播放 | 转场、超自然时刻 | 守时人出场 |
| **次低频脉动** | 30–60 Hz 的持续脉动 | 悬疑段的底色，"来自地下" | [边境杀手](../trailers/sicario.md) |
| **声音押韵** | 不同声源在剪辑点上对位 | 快门 = 上膛 = 灯亮 | [内战](../trailers/civil-war.md) |
| **有源音乐变调** | 画内的音乐减速走调 | 转折点 | [科洛弗道10号](../trailers/10-cloverfield-lane.md) |

注意：BRAAAM 已经被用得很多（连 Hans Zimmer 都说听到被滥用会难受），**全片最多用 2 次**。

## 静默的规则

- 静默之前必须**足够响**，否则静默没有冲击力。
- 静默不等于完全无声。时间停止的段落只留一种声音（脚步 / 心跳 / 滴答），而片名之前的"大黑"要**完全无声**。
- 静默结束时用一个**小**声音（一声滴答），比用大声音更吓人。
- [哥斯拉](../trailers/godzilla-2014.md)：近乎寂静之后的那声吼叫才格外有力。

## 《明日不来》声音设计表

| 时段 | 声音层 | 说明 |
|---|---|---|
| 全片底层 | 约 54 BPM 的钟表滴答 | 比 60 BPM 慢一点，制造不适感 |
| 第一幕 | 收音机人声、八音盒《友谊地久天长》、环境风声 | 温暖但不对劲 |
| 字卡 "AND ONE OF US" 之前 | **BRAAAM #1** | 第一次 |
| 守时人出场 | 滴答倒放 + 耳语 | 他的声音标志 |
| 动作段 | 打击乐重拍，每个剪辑点一下；枪声 = 滴答 | 声音押韵 |
| 冻结人群 | **抽空**，只剩脚步声 | 静默 #1 |
| 倒数段 | 人群齐喊 10→1 作为有源升调，叠加合唱 | 有源音乐变成升调 |
| "1" 之后 | **完全无声 1.5–2 秒** | 静默 #2，全片最响的"声音" |
| 片名 | **BRAAAM #2** 或一个钢琴低音 | 第二次 |
| 日期卡 | 数字倒回的机械声 + 滴答恢复 | 循环继续 |
| 按钮 | 06:00 翻页钟的咔嗒声 + 收音机第三次播报 | 回到开头 |

## 混音参数（YouTube）

- 整体响度约 -14 LUFS，真峰值不超过 -1 dBTP。
- 对白和画外音要比音乐高 6–10 dB。
- 次低频要在手机扬声器上测试：手机放不出 40 Hz，所以要叠加 80–120 Hz 的谐波。

## 来源

- [Wikipedia：BRAAAM](https://en.wikipedia.org/wiki/BRAAAM)
- [Rareform Audio：好莱坞预告的声音设计](https://www.rareformaudio.com/blog/sound-design-in-film-trailers)
- [The Playlist：Hans Zimmer 谈 BRAAAM 被滥用](https://theplaylist.net/?p=92087)
- [Quartz：寂静之地的声音设计](https://qz.com/quartzy/1246604/how-the-sound-designers-of-a-quiet-place-created-primal-terror-out-of-total-silence)
- [Trailaurality：Civil War 预告声音分析](https://trailaurality.squarespace.com/blog/2024/2/6/civil-war)

## 相关笔记

- [音乐策略](music-strategy.md)：配乐层。
- [音乐与音效提示词](../prompts/music-sfx-prompts.md)：可生成的音效清单。
- [盗梦空间](../trailers/inception.md)、[寂静之地](../trailers/a-quiet-place.md)、[内战](../trailers/civil-war.md)、[哥斯拉](../trailers/godzilla-2014.md)、[边境杀手](../trailers/sicario.md)、[科洛弗道10号](../trailers/10-cloverfield-lane.md)：声音样本。
