---
id: 20261107-exhibit-47-video-clips
title: 《第 47 号证物》AKOOL 图生视频：Akool Premium 首轮、Seedance 升级、配音和口型同步，粗剪 v1 和 v2
tags: [production, akool, video, prompt]
created: 2026-11-07
updated: 2026-11-07
related: [20261107-exhibit-47-sound-mix, 20261107-exhibit-47-keyframes, 20261106-exhibit-47-shot-prompts, 20261106-exhibit-47-shot-list, 20261106-akool-workflow, 20261106-submission-checklist, 20261106-exhibit-47-whitebox-previs, 20261106-editing-rhythm]
summary: 全部在 AKOOL 里完成。首轮用 Akool Premium（8 积分/条）做了 29 条，拼成无声粗剪 v0。第二轮改用 Seedance 1.0 Pro Fast（25 积分/条）升级了 13 个镜头，其中 9 条胜出；C2 开场用 Seedance Lite 首尾帧；V1–V12 用 AKOOL 配音，I2 用 Talking Photo 做口型同步，拼成粗剪 v1。第三轮把剩下的镜头也用 Pro Fast 重做：8 条 720p（13 积分/条）里 6 条胜出，积分补充后又做了 3 条 1080p，胜出 1 条。加上 LibTV 生成的音乐和音效，拼成带完整声音的粗剪 v2。共 57 条视频，1035 积分。笔记记录了价格、每条取舍和 19 条教训。
---

# 《第 47 号证物》AKOOL 图生视频：Akool Premium 首轮、Seedance 升级、配音和口型同步，粗剪 v1 和 v2

> Summary: 全部在 AKOOL 里完成。首轮用 Akool Premium（8 积分/条）做了 29 条，拼成无声粗剪 v0。第二轮改用 Seedance 1.0 Pro Fast（25 积分/条）升级了 13 个镜头，其中 9 条胜出；C2 开场用 Seedance Lite 首尾帧；V1–V12 用 AKOOL 配音，I2 用 Talking Photo 做口型同步，拼成粗剪 v1。第三轮把剩下的镜头也用 Pro Fast 重做：8 条 720p（13 积分/条）里 6 条胜出，积分补充后又做了 3 条 1080p，胜出 1 条。加上 LibTV 生成的音乐和音效，拼成带完整声音的粗剪 v2。共 57 条视频，1035 积分。笔记记录了价格、每条取舍和 19 条教训。
>
> **现行版本是粗剪 v2**（`previs/clips/roughcut_v2_540p.mp4`，日志 `clips_v2.json`，声音见 [音乐、音效和混音](exhibit-47-sound-mix.md)）。下文先写首轮（v0），然后是“第二轮”（Seedance 升级、配音、口型同步，粗剪 v1）和“第三轮”（剩下的镜头改用 Pro Fast，粗剪 v2）。

## 背景

- 日期：2026-11-07。工具：**AKOOL 图生视频**（API，`video_image2video_create`）。
- 首帧：[关键帧 v2](exhibit-47-keyframes.md) 的 30 张。AKOOL 生成的帧直接用 AKOOL CDN 链接；LibTV 生成的帧直接用 LibTV 的原图链接（2736×1536 PNG），AKOOL 能读，不用转存。只有本地修过的 C2 首帧是用 `file_upload` 传上去的。
- 账户积分：开始时 970，首轮结束时 579。首轮图生视频一共生成 29 次，花了 **391 积分**。
- 接口状态：订阅前查询模型（`account_models`）返回 1009，现在已经能用，图生视频可以全部走 API，不用网页端。

## 模型和价格（实测，5 秒一条）

| 模型 | 积分 | 分辨率 | 尾帧 | 实际表现 |
|---|---|---|---|---|
| **Akool Premium**（AkoolImage2VideoHDV1） | **8** | 1080p | 不支持 | 大部分镜头都可用，40–90 秒出片。**主力** |
| Seedance 1.0 Pro | 75 | 1080p | 支持 | B2 没有落到尾帧：结尾的第十三人换了衣服，身后还多了人 |
| Kling 3.0 Omni | 100 | 只有 720p | 支持 | I4 首尾帧都很准，表情变化细腻 |
| **Seedance 1.0 Pro Fast** | **25** | 1080p | 不支持 | 第二轮主力。动作戏明显更好（B1、B4、B5），但会乱加东西（B3 挂肉、B10 换制服） |
| Seedance 1.0 Pro Fast 720p | 13 | 720p（实际 1248×704） | 不支持 | 第三轮主力。半价，画质在 540p / 720p 粗剪里看不出差别 |
| Seedance 1.0 Lite | 50 | 1080p | 支持 | C2 开场很好，但同样没有落到尾帧；B8 倒影没有改善 |
| Akool Basic、Hailuo 2.3、Sora 2 / 2 Pro | 没测 | — | — | 先不花这个钱 |

有尾帧的三个模型里（Seedance Pro、Seedance Lite、Kling），经 AKOOL 调用时只有 Kling 真正停在了尾帧上。

## 做法

**提示词只写动作和镜头运动**，画面内容已经在首帧里了。结构是三部分：

1. 机位和运动（"Locked-off security camera, no camera movement" / "Body-worn camera rushing forward…"）
2. 动作，写清谁在动、往哪个方向、动作有多大
3. 一句画质（"Keep the body-worn camera look: fisheye distortion, dark corners, heavy noise and compression, flashlight bloom."）

**负面词**：text, letters, numbers, timestamp, POLICE lettering, logo, watermark, visible blood, morphing bodies, extra limbs, cartoon, video game graphics。再按镜头加上不要的动作，例如 I3 加 "turning the hand over, scar disappearing"。

**B2 甩镜不用首尾帧**：首帧（队员下楼）和第十三人帧各生成一段，两段共 16 积分。第二段开头自带甩镜的运动模糊，剪辑时在模糊里切过去，看不出接缝。比 Seedance 首尾帧（75 积分、还失败了）便宜，也更稳。

## 首轮片段表（Akool Premium，粗剪 v0）

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

## 第二轮：Seedance 升级、配音和口型同步（2026-11-07）

用户要求改用 AKOOL 里的 Seedance，因为画质更好。开始时只剩 579 积分，所以先测了价格：Pro Fast 25、Lite 50、Pro 75。之后用 **Pro Fast** 重做了最重要、在屏幕上停留最久的镜头。

| 镜头 | Seedance 结果 | 粗剪 v1 用哪条 |
|---|---|---|
| B5 枪口火光 | 火光一阵接一阵，队员推进，镜头前冲；比 Akool 版只闪一次好得多 | **Seedance** |
| B1 破门 | 大锤连砸两下，门被砸开，队员冲进雾里 | **Seedance** |
| B4 布兰特 | 布兰特一路冲到镜头前嘶吼 | **Seedance** |
| O2 三年前 | 胸前红灯一个个熄灭，正是剧本要的动作 | **Seedance** |
| C3 监控 | 车边人员动作更多 | **Seedance** |
| I1、I3、B2 第一段 | 和 Akool 版差不多，画面更稳 | **Seedance** |
| X1、B6 | 慌乱和喷气更有力 | **Seedance** |
| B2 第二段 | 开头没有甩镜模糊 | Akool 版开头 0.5 秒的甩镜，接 Seedance 的静止段 |
| D1 | 她又走回冷库门口，方向错 | Akool |
| B3 | 穿过门帘后钩子上挂满带血的肉；冷库是废弃的，应该是空钩子 | Akool |
| B10 | 闪光后光线变成白天，队员换成土黄色制服 | Akool |
| B8 倒影（Lite） | 和 Akool 版几乎一样 | Akool |
| **C2 开场（Lite 首尾帧）** | 先在 LibTV 用抓人帧的同一个木箱间做了空房间首帧，再从空房间做到抓人帧：诺拉从门口踉跄着冲进毒气，很好；但结尾没有停在抓人帧上 | 进门 2.4 秒 → 2 帧监控丢帧 → Akool 抓人那条 |

**配音（AKOOL 配音，`audio_tts`）**：V1–V12 全部生成，每句只要 0.02–0.12 积分。选角按配音表的设定。台词试听文件所在的域名被网络策略挡住了，所以诺拉的声音是先让 4 个候选声音各念一遍台词，再测音高和语速选出来的。

| 角色 | 台词代号 | AKOOL 声音 | 说明 |
|---|---|---|---|
| 诺拉 | V1、V7 | Gentle Young Lady（en-IE） | 欧洲口音，0.85 倍速时最慢最沉；音高中位约 198 Hz |
| 沃德 | V2、V3、V4、V8、V11 | Majestic Brother（en-US，标签"平静、舒缓"） | **五处同一个声音**，这是留给观众的听觉线索 |
| 布兰特 | V5 | Dominant Brother（en-US） | 嘶吼要靠后期加失真和音量，配音念不出来 |
| 报数组员 | V6 | Steady Big Brother / Serious Big Brother | 两个不同的声音轮流 |
| 雷耶斯 | V9、V10 | Intellectual Young Man（en-NZ） | V9 后期加无线电滤波 |
| 接线员 | V12 | Efficient Lady（en-US） | 后期加电话音质 |

**口型同步**：I2 用 AKOOL Talking Photo，S1 I2 关键帧加 V1 音频，1080p，3.1 秒，15 积分。说话和嘴型自然、头部只有轻微动作，可以直接用。输出是 1136×640、25 fps，剪辑时放大。

**粗剪 v1**：画面换成上表选定的片段。对白按分镜表的时间码铺在轨道上，电话和无线电台词加了带通滤波，V3 加了"耳语"处理，蒙太奇里放了 I2 的口型片段。还没有音乐和音效。

## 第三轮：剩下的镜头改用 Pro Fast（2026-11-07）

用户决定**不重拍 B3 和 B10**，改为把还没用 Pro Fast 做过的镜头都用 Pro Fast 做一遍，再剪辑、加音效。当时只剩约 112 积分，1080p 做 11 条要 275，所以先实测了 720p：**13 积分，输出 1248×704**，于是 8 条用 720p 做。之后账户积分补充到 608.7，剩下 3 条（E3 登记簿、E3 标签、B8 首帧）用 1080p 做（75 积分）。

| 镜头 | Pro Fast 结果 | 粗剪 v2 用哪条 |
|---|---|---|
| E1 证物桌 | 沿着一排证物袋推进，稳 | **Pro Fast 720p** |
| B9 门帘 | 门帘后的人中弹倒下，手电落地还亮着；比 Akool 版完整 | **Pro Fast 720p**（取 1.4–2.4 秒） |
| C1 监控俯视 | 雾里多处火光和晃动的手电；但颜色变暖变亮 | **Pro Fast 720p**，剪辑里去饱和、压暗，调回灰色监控 |
| B7 布兰特 | 嘶吼，构图稳定 | **Pro Fast 720p** |
| B8 倒影 | 倒影静止，红灯常亮 | **Pro Fast 720p** |
| E2 片名 | 标签一直朝向镜头，适合压片名 | **Pro Fast 720p**（片名移到左边，避开标签） |
| O1 三年前 | 0.2 秒起男孩的头顶就升进画面，脸必须藏住 | Akool |
| C2 抓背心 | 诺拉的背心变成白色背心，门口还起了火 | Akool |
| E3 登记簿（1080p） | 完全静止、页面空白，和 Akool 版一样，也没有甩镜 | **Pro Fast**（甩镜仍在剪辑里做） |
| E3 标签（1080p） | 一直是远景，没有推向红灯 | Akool（Akool 版推得很近） |
| B8 首帧（1080p） | 1.5 秒起大厅里出现一个拿手电的人，大厅必须是空的 | Akool |

**粗剪 v2**：画面换成上表的选择；在 LibTV 生成了 18 个音效和配乐 SC1，用 `tools/soundmix.py` 混成对白、音乐、音效、底噪四轨（响度 -13.8 LUFS，两处全静音），详见 [音乐、音效和混音](exhibit-47-sound-mix.md)。混音时发现**粗剪 v1 的对白整体提前了约 3 秒**（ffmpeg 去静音滤镜丢了时间戳），v2 已修正。

## 19 条教训

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
11. **Seedance 里性价比最高的是 Pro Fast（25 积分）**，比 Lite（50）便宜，动作表现也更好。Lite 只在需要尾帧时才考虑，而它同样落不到尾帧。
12. **Seedance 会加首帧里没有的东西**：B3 的空钩子挂上了带血的肉，B10 闪光后换成白天和土黄色制服。负面词要写明 carcasses、meat、daylight、tan uniform，生成后逐条检查。
13. **Seedance 也会把方向演反**（D1 又走回了冷库），方向关键的镜头要写清楚"背对什么、朝哪里走"，并且准备好 Akool 版作后备。
14. **同一个镜头不同模型的片段可以拼**：B2 用 Seedance 的下楼、Akool 的甩镜模糊和 Seedance 的静止段；C2 用 Lite 的进门、2 帧丢帧和 Akool 的抓人。监控画面的丢帧正好遮住跳切。
15. **配音很便宜、口型同步也便宜**（TTS 每句约 0.1 积分，Talking Photo 每 5 秒 15 积分），积分应该优先留给视频生成。
16. **粗剪阶段用 720p 的 Pro Fast 就够了**：13 积分，是 1080p 的一半，540p / 720p 预览里看不出差别。定稿镜头再考虑 1080p。
17. **Pro Fast 也会往画面里加人**：B8 首帧的空大厅里出现了人，O1 的男孩抬起头露出了头顶。负面词写了也拦不住，要逐帧检查，并且准备好 Akool 版作后备。
18. **静止镜头换模型没有收益**：E3 登记簿两个模型的结果几乎一样，都不执行"最后甩镜"。这类镜头用最便宜的模型就行，甩镜在剪辑里做。
19. **Seedance 会把冷色画面调暖**（C1 从灰色监控变成暖黄）。监控画面在剪辑里统一去饱和，比重新生成便宜。

## 下一步（首轮时写的，部分已完成）

1. ~~**I2 口型同步和配音**~~（已完成，见上文第二轮）：用 AKOOL 配音生成诺拉的 "There were thirteen of us."，再用口型同步（或 talking photo）贴到 S1 I2 上。V1–V12 的配音也在 AKOOL 里做。
2. ~~**C2 的开头**~~（已完成：LibTV 空房间首帧 + Seedance Lite）：两种做法。一是在 LibTV 里，用抓人帧的同一个木箱间生成一张"空房间、气体刚涌进来"的首帧，再用 Akool Premium 生成（约 8 积分）。二是用 Kling 3.0 Omni，从这张空房间帧做首尾帧到抓人帧（100 积分）。
3. **重拍候选**（每条 8 积分）：B5（要更多连续火光）、B8 倒影（更像镜面）、O2（更旧的画质）。
4. **监控墙素材池 P1–P6** 还没有单独生成，现在的监控墙借用了其他镜头。
5. **剪辑**：AKOOL 官方标志、正式字卡和叠字（编号、时间戳、REC、标签文字）、调色、颗粒、声音设计和混音，按 [AKOOL 制作流程](akool-workflow.md) 的第 6–9 步来。
6. **积分**：第二轮结束后剩约 112。

**第二轮之后的下一步**（第三轮已经做完声音，重拍 B3、B10 按用户决定不做）：
1. **剪辑定稿**：换上 AKOOL 官方标志；正式字卡和叠字（编号、时间戳、REC、标签文字）；把 Seedance 片段和 Akool 片段调成同一套颜色和颗粒。
2. **声音**：音乐（SC1/SC2、BRAAAM）、音效（FX1–FX12）、布兰特嘶吼的失真、V3 真正的耳语（可以重新配，或者在后期压低、加气声）。
3. **重拍候选**（Seedance Pro Fast，每条 25 积分）：B3（负面词写明 carcasses）、B10（写明 daylight、tan uniform）。剩下的积分够 3–4 条。
4. **监控墙素材池 P1–P6**：现在借用其他镜头，可以继续借用。

**第三轮之后的下一步**：
1. **人耳试听**粗剪 v2，重点是对白清晰度和声音落点（混音只做了测量检查）。
2. **剪辑定稿**：AKOOL 官方标志、正式字卡和叠字、统一调色和颗粒（Seedance 和 Akool 片段、720p 和 1080p 片段放在一起）。
3. **积分**：第三轮结束后剩约 533.7。可以考虑把 6 条 720p 胜出镜头重做成 1080p（每条 25），或者重试 O1、B8 首帧。

## 文件

`previs/clips/`：

- `clips_v2.json`（**现行**）：57 条视频的完整日志，包括三轮生成和 Talking Photo。`used_in_cut_v1`、`used_in_cut_v2` 分别标出两版粗剪（含监控墙）用到的片段。
- `roughcut_v2_540p.mp4`（**现行**）：粗剪 v2，带对白、音乐和音效。
- `roughcut_v1_540p.mp4`：粗剪 v1，只有对白轨（对白整体提前约 3 秒，见第三轮）。
- `../audio/sfx/`、`../audio/music/`、`../audio/sfx_music.json`：LibTV 生成的音效和配乐，见 [音乐、音效和混音](exhibit-47-sound-mix.md)。
- `../audio/voice/` 和 `../audio/voice_lines.json`：全部配音文件，以及每句的声音、语速和 AKOOL 任务号。
- `clips_v1.json`：首轮 29 次生成的完整日志（保留作对照）。每条记了模型、分辨率、时长、积分、首帧和尾帧链接、提示词、负面词、AKOOL 任务号、视频链接、取舍，以及是否用在粗剪里（`selected`）。提交时它就是"如何使用 AKOOL"的制作日志。
- `strips/`：每条片段的 6 帧缩略图。
- `roughcut_v0_540p.mp4`：无声粗剪 v0。
- `tools/fetch_clips.py`：按 `clips_v2.json` 把粗剪 v2 要用的片段下载到本地（`--v1` 下载 v1 的，`--all` 下载全部）。
- `tools/roughcut.py`：重新拼粗剪 v2 的画面和对白轨。
- `tools/soundmix.py`：把对白、音乐、音效、底噪混到粗剪上。

视频原片（1920×1080 或 1248×704，24 fps）都在 AKOOL 的 CDN 上，链接见日志，仓库里不存原片。

## 相关笔记

- [音乐、音效和混音](exhibit-47-sound-mix.md)：粗剪 v2 的声音。
- [关键帧 v2](exhibit-47-keyframes.md)：这些片段的首帧。
- [镜头提示词库](../prompts/exhibit-47-shot-prompts.md)：每个镜头的完整描述和后期叠字规范。
- [分镜表](exhibit-47-shot-list.md)：粗剪用的时间码。
- [AKOOL 制作流程](akool-workflow.md)：图生视频在整个流程里的位置。
- [提交检查清单](submission-checklist.md)：`clips_v1.json` 是 AKOOL 使用记录的一部分。
- [剪辑节奏](../techniques/editing-rhythm.md)：甩镜、闪切这些在剪辑里怎么做。
