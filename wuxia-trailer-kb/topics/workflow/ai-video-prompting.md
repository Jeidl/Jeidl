---
id: 20261108-ai-video-prompting
title: 用本知识库驱动 AI 视频生成
tags: [ai, workflow, shots]
created: 2026-11-08
updated: 2026-11-08
related: [20261108-storyboard-template, 20261108-shot-vocabulary, 20261108-speed-ramp-and-slow-motion, 20261108-color-grading, 20261108-visual-motifs]
summary: 把分镜表转成 AI 视频生成提示词的公式（景别 + 主体 + 动作 + 环境 + 光线 + 运镜 + 速度 + 质感 + 时长），中英文示例，"停"镜与"爆"镜的生成策略和原创性提醒。
---

# 用本知识库驱动 AI 视频生成

> Summary: 一行分镜 = 一条提示词；"停"的镜头生成长一点再截取，"爆"的镜头生成多条备选再快切。

## Context
用 AI 视频工具生成预告素材时使用。各模型支持的单段时长、比例和参数不同，以所用模型的说明为准。

## 提示词公式
`[景别] + [主体 / 人物] + [动作（停或爆）] + [环境 / 意象] + [光线 / 天气] + [运镜] + [速度（常速 / 慢镜）] + [色彩 / 质感] + [时长 / 比例]`

## 示例（原创场景）
**停 · 冷开场**
> 极远景，雪原上一座孤城，城门前一名披斗篷的剑客背对镜头静立，风卷起雪粒，天色阴沉，固定机位，低饱和水墨灰调、胶片颗粒，5 秒，16:9。

**爆 · 冲击点**
> 大特写，两柄长剑在雨中相交，火花迸出，雨滴被震开成环状，超慢动作，冷蓝夜色中一点暖光，3 秒。

**English (same shot)**
> Extreme close-up, two long swords clash in the rain, sparks burst, raindrops blasted outward in a ring, ultra slow motion, cold blue night with a single warm light, 3 seconds.

参考：有 AI 提示词以胡金铨风格为参照，写成"极远景竹林浓雾、背影静止 → 手部特写 → 侧向跟拍长镜头"，体现先静后动【S43】；兵刃相接的瞬间切到超慢动作、雨水被刀劲震开也是常见写法【S43】。

## 生成策略【经验法则】
1. **"停"镜**：生成较长片段（如 5 秒以上），剪辑时截取最稳定的 2–4 秒。
2. **"爆"镜**：每个冲击点生成 3–5 条备选，各截取 0.3–1 秒快切；同一招从不同角度生成，可以做重叠剪辑。
3. **慢镜**：直接在提示词里写"超慢动作 / slow motion"，或生成常速再用补帧放慢。
4. **一致性**：主角固定参考图、固定服装描述；同一场景固定光线和色彩词。
5. **留白**：片名卡和字幕卡的位置在提示词里预留（如"画面右侧大面积留白"）。
6. **竖版**：竖版单独生成 9:16，不要只靠裁切。
7. **声音**：画面生成后按 sound-design-palette 补兵器和环境声，不要依赖模型自带音频来卡点。

## 原创性提醒
可以参考某种风格（色彩、节奏、构图），但不要复刻具体影片的角色、场景或画面；示例中的场景都是原创。

## Related
- [分镜表模板](../shots/storyboard-template.md) — 每行对应一条提示词。
- [镜头词汇表](../shots/shot-vocabulary.md) — 景别与招牌镜头。
- [变速与慢镜头](../editing/speed-ramp-and-slow-motion.md) — 慢镜内容。
- [调色与色彩](../style/color-grading.md) — 色彩风格词。
- [武侠意象库](../shots/visual-motifs.md) — 环境词。
