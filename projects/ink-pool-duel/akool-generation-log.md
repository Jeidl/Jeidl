# 《墨池》关键镜头 · AKOOL 生成记录

> 对应 `trailer-storyboard.md` 第 11 节的关键镜头。流程：先用文生图做每个镜头的首帧静帧（16:9，1080p），确认构图后再用图生视频。
> **注意**：AKOOL 返回的结果链接大约 7 天后失效，请及时下载保存到本地。

## 额度
| 时间点 | 余额 |
|---|---|
| 开始前 | 295.5 |
| 11 张静帧 + 4 张重做（每张 3） | 250.5 |
| Kling 3.0 Omni 测试 1 段（5 秒） | 150.5（**−100**） |
| Akool Basic 测试 1 段（5 秒，1080p） | 144.5（−6） |
| 第 3 次重做 085 静帧 | 141.5 |
| Akool Basic 其余 9 段 | 87.5（−54） |

## 第一步：首帧静帧（模型：AKOOL 文生图，flux-krea-dev-lora）
统一风格词：cinematic still from a Chinese wuxia film, ink-wash monochrome palette, desaturated, high contrast, cold drifting mist, overcast diffused light, 35mm film grain, photorealistic。
统一负面词：text, watermark, logo, cartoon, anime, illustration, oversaturated colors, modern objects, blurry（人物镜头另加 deformed hands, extra fingers）。

| 镜号 | 内容 | 图片任务 ID | 状态 | 图片链接 |
|---|---|---|---|---|
| 003 | 水珠悬在稠黑墨池上方 | 6af0337c97abb75cf0a4628f | 采用 | [静帧](https://d2qf6ukcym4kn9.cloudfront.net/1794126751316-06c26cae-7b09-4767-9642-771b00dc2cf3-6057.jpeg) |
| 011 | 黑曜石剑体内五色涡流 | 6af0337c51e26737e1c3d020 | 采用（剑格像日本刀镡，剪辑时裁掉；重做版 6af033e597abb75cf0a4672b 仍有刀镡，未用） | [静帧](https://d2qf6ukcym4kn9.cloudfront.net/1794126752263-6e9ddf60-4c00-454d-93dd-4dcc272994e0-4120.jpeg) |
| 022 | 积水下三道墨线 | 6af0337c97abb75cf0a46299 | 采用 | [静帧](https://d2qf6ukcym4kn9.cloudfront.net/1794126752991-3c48da4a-fd76-4d53-8bd5-fb678fe06296-8453.jpeg) |
| 025 | 沈墨舟翻腕，碎墨成弧 | 6af0337d97abb75cf0a462a3 | 采用（剑形偏锯齿，不像竹节） | [静帧](https://d2qf6ukcym4kn9.cloudfront.net/1794126753709-90541249-3e0a-4d94-a5d5-c067a3775ee6-6207.jpeg) |
| 039 | 腕上墨痕 | 6af0337d51e26737e1c3d02d | 重做版采用（初版像手绳和纹身） | [静帧](https://d2qf6ukcym4kn9.cloudfront.net/1794126842486-bfdbff45-a4d5-437d-b938-311704c0a8ee-6579.jpeg) |
| 045 | 墨池隆起（墨蟒将出） | 6af0337d97abb75cf0a462b1 | 采用 | [静帧](https://d2qf6ukcym4kn9.cloudfront.net/1794126755046-d139a214-23c3-4eee-87fb-0dde2228109c-5433.jpeg) |
| 062 | 墨龙缠住黎无相双臂 | 6af0337e51e26737e1c3d037 | 重做版采用（初版有漂浮的第二把剑）；龙仍带鳞片 | [静帧](https://d2qf6ukcym4kn9.cloudfront.net/1794126843214-21380afb-0ced-40e7-92cc-220c50ef3773-1478.jpeg) |
| 071 | 水墨画卷从石台升起 | 6af0337e51e26737e1c3d041 | 采用 | [静帧](https://d2qf6ukcym4kn9.cloudfront.net/1794126756468-9e6b6897-18d3-4cac-af82-a657ab24c622-3778.jpeg) |
| 073 | 竖剑凝混沌球 | 6af0337e97abb75cf0a462bb | 采用（混沌球偏玻璃球质感） | [静帧](https://d2qf6ukcym4kn9.cloudfront.net/1794126757205-daf1308b-f3e4-4d89-b2f1-01a852e2f290-7942.jpeg) |
| 085 | 断崖边碎石坠落 | 6af0337e51e26737e1c3d04b | 第 3 版采用（前两版分别是登山靴、运动鞋），改为不出现鞋 | [静帧](https://d2qf6ukcym4kn9.cloudfront.net/1794126901536-a9703da3-69ff-4026-be79-d38285957b82-3757.jpeg) |
| 094 | 五色油膜墨池，水珠将落 | 6af0337f97abb75cf0a462c5 | 采用 | [静帧](https://d2qf6ukcym4kn9.cloudfront.net/1794126758516-b3b27906-f5c3-4652-877b-9abef85cdc57-0359.jpeg) |

## 第二步：图生视频（全部 5 秒，24 fps，1920×1080）

| 镜号 | 模型 | 视频任务 ID | 额度 | 建议截取（秒） | 检查结论 | 视频链接 |
|---|---|---|---|---|---|---|
| 003 | Akool Basic | 6af0340251e26737e1c3d59a | 6 | 0.0–2.0 | 写实、好看；但水滴像普通水面一样起涟漪，"不溅水花、只压出凹痕"的设定没有体现 | [mp4](https://d2qf6ukcym4kn9.cloudfront.net/1794126970355-5751.mp4) |
| 011 | Akool Basic | 6af034bd97abb75cf0a46eb4 | 6 | 3.0–5.0 | 镜头沿剑身滑向剑尖，约 3.5 秒后刀镡出画；用后半段 | [mp4](https://d2qf6ukcym4kn9.cloudfront.net/1794127070841-7673.mp4) |
| 022 | Akool Basic | 6af034bd51e26737e1c3dc32 | 6 | 0.5–2.0 | 第 1 秒左右水花沿裂缝猛然炸起，正好是"爆"点 | [mp4](https://d2qf6ukcym4kn9.cloudfront.net/1794127071519-0066.mp4) |
| 025 | Akool Basic | 6af034be51e26737e1c3dc3f | 6 | 1.5–4.0 | 碎墨被牵成环绕人物的弧形墨幕，效果好 | [mp4](https://d2qf6ukcym4kn9.cloudfront.net/1794127141585-3508.mp4) |
| 039 | Akool Basic | 6af034be97abb75cf0a46ec5 | 6 | 1.0–2.5 | 墨痕缓慢向上分叉，略带一丝红色 | [mp4](https://d2qf6ukcym4kn9.cloudfront.net/1794127104090-2325.mp4) |
| 045 | Akool Basic | 6af034bf97abb75cf0a46ed0 | 6 | 1.0–3.0 | 三条墨蟒破池而出，人物立于池沿，最佳镜头之一 | [mp4](https://d2qf6ukcym4kn9.cloudfront.net/1794127104983-2297.mp4) |
| 062 | Akool Basic | 6af034bf51e26737e1c3dc4c | 6 | 1.0–2.25 | 墨龙缠身、人物吃力抵抗；龙带鳞片，不够"墨"感 | [mp4](https://d2qf6ukcym4kn9.cloudfront.net/1794127137622-3952.mp4) |
| 071 | Kling 3.0 Omni | 6af033f251e26737e1c3d4a0 | 100 | 2.5–4.5 | 推镜平稳、飞鸟迎面、云雾流动；墨山"生长"不明显 | [mp4](https://d2qf6ukcym4kn9.cloudfront.net/1794126991901-611c6f16-bcba-4564-b0e3-430d5b77f709-5740.mp4) |
| 073 | Akool Basic | 6af034bf97abb75cf0a46edd | 6 | 1.5–2.75（或 3.5–5.0 看裂纹） | 碎石绕球旋转、剑身裂纹蔓延；混沌球偏玻璃质感 | [mp4](https://d2qf6ukcym4kn9.cloudfront.net/1794127138610-6720.mp4) |
| 085 | Akool Basic | 6af034c051e26737e1c3dc57 | 6 | 1.5–2.5 | 碎石坠崖、衣摆狂舞、锈剑颤动 | [mp4](https://d2qf6ukcym4kn9.cloudfront.net/1794127170912-6259.mp4) |
| 094 | Akool Basic | 6af034c051e26737e1c3dc64 | 6 | 0.0–3.0 | 第 1 秒墨面留下一个未合拢的坑洞，适合做按钮镜头 | [mp4](https://d2qf6ukcym4kn9.cloudfront.net/1794127172030-9288.mp4) |

## 经验（写给下次）
- **价格差 16 倍**：Kling 3.0 Omni 5 秒 = 100 额度；Akool Basic 5 秒 1080p = 6 额度。Basic 的写实度和运动对本片已经够用，Kling 只值得留给 1–2 个最关键的镜头。
- 文生图把 "thick white sole" 理解成运动鞋，把 "sword" 默认画成日本刀；古装道具要写清 "straight double-edged Chinese jian"，并在负面词里排除 katana、tsuba、sneakers。
- 生成前先看静帧：11 张里有 4 张需要重做，每张只花 3 额度，比直接生成视频再返工便宜得多。
- 不同镜头里黎无相的长相不一致（062 与 073）。快剪里不明显，但如果要做人物特写，应先做角色参考图再用图生图。

## 剩余
余额 **87.5**。可用于：返工 003（不溅水花的黏稠落水）、062（无鳞片的墨龙），或补生成分镜表中的其他镜头（每个 6 额度）。
