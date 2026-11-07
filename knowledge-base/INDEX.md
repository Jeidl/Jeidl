# Coming Never 知识库 — 总索引

AKOOL AI Film Challenge「Coming Never」赛道参赛项目《第 47 号证物 EXHIBIT 47》（备选：《明日不来 UNTOMORROW》）的知识库：赛事规则、风格与故事决策、28 篇预告片拆解（覆盖 30 部作品）、技法库、AI 提示词库和制作方案。

## 快速入口（人类读者）

| 我想… | 打开 |
|---|---|
| 看主方案的完整故事 | [《第 47 号证物》完整故事](topics/concept/exhibit-47-story.md) |
| 5 分钟了解全部决策 | [风格定向](topics/brief/style-decision.md) → [动作悬疑方案](topics/concept/action-mystery-concepts.md) → [《第 47 号证物》](topics/concept/exhibit-47-story.md) |
| 直接开始生成画面 | [人物与道具设定](topics/concept/exhibit-47-character-bible.md) → [《第 47 号证物》镜头提示词库](topics/prompts/exhibit-47-shot-prompts.md) |
| 看设定图是怎么核对、锁定细节的 | [设定图的图片转提示词学习记录](topics/prompts/reference-sheet-reverse-prompts.md) |
| 看场景长什么样、镜头怎么摆 | [场景图](topics/prompts/exhibit-47-scene-images.md) → [白模预演](topics/production/exhibit-47-whitebox-previs.md)（含 89 秒动态预演） |
| 看每个镜头的关键帧 | [关键帧 v2](topics/production/exhibit-47-keyframes.md)（30 张：人物在 LibTV，场景在 AKOOL，画面自带证物画质） |
| 看图生视频片段和粗剪 | [AKOOL 图生视频](topics/production/exhibit-47-video-clips.md)（57 条片段、Seedance 升级、配音和口型同步，带完整声音的粗剪 v2） |
| 看音乐、音效和混音 | [音乐、音效和混音](topics/production/exhibit-47-sound-mix.md)（LibTV 生成的配乐和 18 个音效、放置时间表、混音参数） |
| 知道每一秒放什么 | [《第 47 号证物》90 秒档分镜表](topics/production/exhibit-47-shot-list.md)（v2，实际 88 秒） |
| 安排两周的工作 | [AKOOL 制作流程与 14 天排期](topics/production/akool-workflow.md) |
| 提交前自查 | [提交检查清单](topics/production/submission-checklist.md) |

## How to use this KB (for agents)

1. 先读本索引，按描述挑选笔记，只打开需要的那几篇（通常 1–3 篇）。
2. 提示词里的 `[STYLE-A] [NEG-A] [ADA-REF] [KEEPER-REF] [SAM-REF]` 是占位符，原文在 `20261106-style-anchor` 和 `20261106-character-bible`。
3. 预告片拆解里的段落顺序是概述，不是逐帧时间码。事实来源列在每篇笔记的「来源」一节。
4. 引用信息时注明笔记的 `id`。

## How to update this KB (for agents)

- 新想法 → 新建一篇原子笔记。同一想法有变化 → 原地修改，并更新 `updated`。
- 任何新建、重命名、删除，都必须在同一次修改里同步更新本索引和对应主题的 `_topic.md`。
- 只使用下面受控列表里的标签；需要新标签时，先加进列表。
- 笔记正文里的每个笔记链接，都要同时写进 frontmatter 的 `related`。

## Controlled tags

- 类型：`brief` `concept` `production` `prompt` `trailer`
- 创作：`style` `story` `time-loop` `fantasy`
- 作者系：`nolan` `villeneuve` `fincher` `peele`
- 手法：`sound` `music` `editing` `text-card` `visual` `action` `mystery-marketing`
- 赛事：`akool` `copyright`

## Registry

### 赛事与定向 brief
- `20261106-challenge-rules` — **AKOOL「Coming Never」赛道规则与评分** — `topics/brief/challenge-rules.md` — AKOOL AI Film Challenge 的 Coming Never 赛道硬性要求（30–90 秒、原创、顶部 AKOOL 标志）、评分权重、奖金和有冲突的截止日期。
- `20261106-story-direction` — **故事定向：悬疑 + 动作 + 无限流（时间循环）** — `topics/brief/story-direction.md` — 在打斗 / 武侠 / 无限流中选择"悬疑 + 动作 + 时间循环（无限流）"，以及它为什么同时满足故事分、原创分和 AI 制作的限制。
- `20261106-style-decision` — **风格定向：选「电影级冷峻写实」** — `topics/brief/style-decision.md` — 对比写实 / 猫和老鼠 / 西幻写实 / 玄幻四种风格后，选定"诺兰-维伦纽瓦式冷峻写实"，并说明为什么不用猫和老鼠。

### 核心创意 concept
- `20261106-action-mystery-concepts` — **动作悬疑 × 元结尾：4 个备选故事** — `topics/concept/action-mystery-concepts.md` — 以动作和悬疑为主、结尾字卡解释"这部电影为什么永不上映"的四个写实方案：《第 47 号证物》《████（涂黑）》《第二张脸》《最后一镜》，含谜题、动作戏、反转、元结尾、撞车检查和打分；首推《第 47 号证物》。
- `20261106-alternative-concepts` — **备选创意（同风格换故事 4 个 + 换风格 3 个）** — `topics/concept/alternative-concepts.md` — 除《明日不来》外的七个早期备选（动作悬疑新方案另见 action-mystery-concepts）：同为写实悬疑动作的《末日悬停》《永不降落》《禁映》《黑暗七分钟》，以及换风格的西幻、玄幻、卡通方案；附打分对比、撞车风险和选择建议。
- `20261106-character-bible` — **角色与道具圣经（一致性锚点）** — `topics/concept/character-bible.md` — 女主 Ada、守时人、搭档 Sam 和关键道具 / 场景的固定英文描述块（ADA-REF 等），以及角色设定图的生成提示词，保证跨镜头一致。
- `20261106-exhibit-47-character-bible` — **《第 47 号证物》人物与道具设定（一致性锚点）** — `topics/concept/exhibit-47-character-bible.md` — 主方案的人物设定（诺拉、沃德、第十三人、布兰特、特勤组、旧录像里的手）、可直接粘贴的英文角色块（NORA-REF 等）、道具与场景块、颜色规则，以及统一风格的设定图提示词（SHEET-STYLE 等固定块 + 母版参考链）；沃德在预告里只露手和声音。
- `20261106-exhibit-47-story` — **《第 47 号证物 EXHIBIT 47》完整故事** — `topics/concept/exhibit-47-story.md` — 主方案的完整故事：片名的三层含义、世界设定、人物、真相时间线、三幕情节、逻辑问答、公平推理线索表、主题与结局，以及预告片能说什么、不能说什么。
- `20261106-untomorrow-concept` — **《明日不来 UNTOMORROW》核心创意** — `topics/concept/untomorrow-concept.md` — 预告片主创意：城市被困在 12 月 31 日，每晚午夜重来，一个只露背影的"守时人"在猎杀记得循环的人；包含 logline、世界规则、主题、反转和片名备选。

### 预告片拆解 trailers
- `20261106-10-cloverfield-lane` — **《科洛弗道10号 10 Cloverfield Lane》预告（2016）** — `topics/trailers/10-cloverfield-lane.md` — 欢快的 60 年代老歌在片中播放，温馨的地堡日常逐渐变味，唱片减速走调，情绪从温暖翻成恐惧，是"有源音乐变调"的教科书。
- `20261106-a-quiet-place` — **《寂静之地 A Quiet Place》预告（2018）** — `topics/trailers/a-quiet-place.md` — 把"寂静"本身做成卖点：一句"它们听不见你，就猎不到你"讲清规则，大段沉默中偶发的声音比任何配乐都吓人。
- `20261106-arrival` — **《降临 Arrival》预告与配乐（2016）** — `topics/trailers/arrival.md` — 悬浮在草原雾气上的巨大"贝壳"、墨环一样的外星文字：用宁静的尺度感代替爆炸；Max Richter 弦乐的情感力量与被滥用的教训。
- `20261106-black-myth-wukong` — **《黑神话：悟空》首曝预告（2020）** — `topics/trailers/black-myth-wukong.md` — 玄幻写实的标杆：篝火噼啪声 + 中文画外音开场，西游记的暗黑写实化；24 小时 B 站约千万播放，"文化熟悉 × 视觉陌生"是爆点。
- `20261106-blade-runner-2049` — **《银翼杀手 2049 Blade Runner 2049》预告（2017）** — `topics/trailers/blade-runner-2049.md` — 整座城市被橙色浓雾笼罩、对称构图、长交叉淡化：用"单色世界 + 对称"建立辨识度极高的视觉风格。
- `20261106-civil-war` — **《美国内战 Civil War》预告（2023 / 2024，A24）** — `topics/trailers/civil-war.md` — 相机快门声与枪械上膛声对位剪辑，照明灯开启卡在上膛声上；震耳的枪声与突然的死寂交替，"声音押韵"是低成本高级感的来源。
- `20261106-cloverfield-teaser` — **《科洛弗档案 Cloverfield》无片名前导（2007）** — `topics/trailers/cloverfield-teaser.md` — 没有片名、只有日期 1-18-08 的前导：伪纪录手持派对 → 爆炸 → 自由女神像的头砸在街上；"只给日期"成为悬疑营销的经典。
- `20261106-dune-2020` — **《沙丘 Dune》首支预告（2020）** — `topics/trailers/dune-2020.md` — Hans Zimmer 重编 Pink Floyd《Eclipse》加 32 人合唱，配合渺小人类与无垠沙漠的尺度对比，是"史诗感"的标准答案。
- `20261106-edge-of-tomorrow` — **《明日边缘 Edge of Tomorrow》预告与 Live. Die. Repeat.（2013 / 2014）** — `topics/trailers/edge-of-tomorrow.md` — 时间循环大片的营销样板：三个词的标语"Live. Die. Repeat."讲清全部规则，强到发行方在家庭影碟版上把标语放大、片名缩小。
- `20261106-fincher-cover-song-teasers` — **芬奇的翻唱前导三部曲：《社交网络》《龙纹身的女孩》《消失的爱人》** — `topics/trailers/fincher-cover-song-teasers.md` — 童声合唱版 Creep、170 刀卡点的 Immigrant Song、反讽情歌 She：用"熟悉旋律的陌生化"制造不安，开启了慢速翻唱预告潮。
- `20261106-godzilla-2014` — **《哥斯拉 Godzilla》预告 HALO 跳伞段（2013 / 2014）** — `topics/trailers/godzilla-2014.md` — 士兵拖着红色信号烟从高空坠入烟雾弥漫的废墟，配 Ligeti《安魂曲》的诡异合唱，几乎无声，最后一声怒吼收尾：用"错位的音乐"制造宗教般的恐惧。
- `20261106-got-crypts-of-winterfell` — **《权力的游戏》第八季前导「临冬城墓穴」（2019）** — `topics/trailers/got-crypts-of-winterfell.md` — 西幻写实的参考样本：烛光墓穴中缓慢行走、亡者的画外音、雕像暗示角色命运；专门为预告拍摄，也提醒我们"预告可以合法地误导"。
- `20261106-inception` — **《盗梦空间 Inception》前导预告 + 终极预告（2009 / 2010）** — `topics/trailers/inception.md` — BRAAAM 音效的起源；"台词 → 重音"的现代预告句法；前导预告只用一个物件（陀螺）和一句标语建立悬念。
- `20261106-interstellar-teaser` — **《星际穿越 Interstellar》前导预告（2013）** — `topics/trailers/interstellar-teaser.md` — 几乎不用正片画面：历史太空影像 + 主角沉郁的画外音 + 少量玉米地镜头，只卖"情绪和主题"不卖剧情。
- `20261106-joker-2019-teaser` — **《小丑 Joker》前导预告（2019）** — `topics/trailers/joker-2019-teaser.md` — Jimmy Durante 的《Smile》+"妈妈总让我微笑"的开场台词 + 阶梯意象：用温柔的老歌讲一个人的堕落。
- `20261106-longlegs-teasers` — **《长腿 Longlegs》系列前导（2024）** — `topics/trailers/longlegs-teasers.md` — NEON 的"反着来"营销：黑白闪帧、结尾的密码符号、只露一双眼睛的反派；不给好看的部分，逼观众主动去解码。
- `20261106-mission-impossible-fallout` — **《碟中谍6：全面瓦解 Mission: Impossible – Fallout》预告（2018）** — `topics/trailers/mission-impossible-fallout.md` — 黄昏时分的 HALO 跳伞：每天只有约 3 分钟光线、只能拍一条的真实特技；动作预告靠"一个大到不可能的瞬间"取胜，而不是密集打斗。
- `20261106-nope` — **《不 Nope》预告（2022）** — `topics/trailers/nope.md` — 一朵不会动的云：把威胁藏在最普通的东西里；超级碗预告几乎不交代剧情，"坏的奇迹"一词成为悬念核心。
- `20261106-oppenheimer-teaser` — **《奥本海默 Oppenheimer》前导预告与倒计时（2022）** — `topics/trailers/oppenheimer-teaser.md` — 火焰与烟雾 + 黑白人物镜头 + 一个实时运行的倒计时：把"倒计时"本身做成悬念装置。
- `20261106-prisoners` — **《囚徒 Prisoners》预告（2013）** — `topics/trailers/prisoners.md` — 冷峻写实悬疑的样板：一句"每个父母最可怕的噩梦"就交代全部动机，湿冷的天气和克制的镜头制造压迫感；也是"预告把电影卖窄了"的反面教材。
- `20261106-severance` — **《人生切割术 Severance》预告与无尽走廊（2022 / 2024）** — `topics/trailers/severance.md` — 对称、狭长、无尽的白色走廊：特效团队把走廊加长、收窄，制造"永远走不出去"的感觉，适合表现循环与困局。
- `20261106-shutter-island` — **《禁闭岛 Shutter Island》预告（2009 / 2010）** — `topics/trailers/shutter-island.md` — 淡入淡出串起的短镜头制造不确定感，剪辑速度逐步加快、中段短暂放缓，剪辑点配白闪；灯塔是"必须去揭开的问题"。
- `20261106-sicario` — **《边境杀手 Sicario》预告（2015）** — `topics/trailers/sicario.md` — 开场字卡"在墨西哥，sicario 的意思是杀手"一句话定调；配乐像"来自地下的脉动"，是低频压迫感的范本。
- `20261106-squid-game` — **《鱿鱼游戏 Squid Game》预告与巨型娃娃（2021）** — `topics/trailers/squid-game.md` — 明亮童趣的色彩 × 致命的游戏：巨型娃娃转头的一瞬间接一串枪声；把童年符号变成死亡装置，是最强的反差公式。
- `20261106-tenet` — **《信条 Tenet》预告（2019 / 2020）** — `topics/trailers/tenet.md` — 子弹飞回枪膛、先有弹孔后有枪战、翻车再翻回来：用"倒放物理"制造奇观，用一句"别去理解它，去感受它"取代解释。
- `20261106-the-batman-teaser` — **《新蝙蝠侠 The Batman》前导预告（2020 DC FanDome）** — `topics/trailers/the-batman-teaser.md` — Nirvana《Something in the Way》的阴郁吟唱 + 雨夜、红色信号弹、黑色电影质感；导演写剧本时就在听这首歌，音乐与人物同源。
- `20261106-the-dark-knight` — **《蝙蝠侠：黑暗骑士 The Dark Knight》预告与 Why So Serious 营销（2008）** — `topics/trailers/the-dark-knight.md` — 用反派的画外音串起全片、镜头时长由约 4 秒逐步缩短的加速剪辑，以及围绕一句台词的 15 个月 ARG 营销。
- `20261106-us` — **《我们 Us》预告与 Tethered Mix（2018 / 2019）** — `topics/trailers/us.md` — 同一首歌先放原版、再放恐怖弦乐版（Tethered Mix），音乐本身就讲了"镜像分身"的故事；车道上手牵手的红衣一家是全片最强画面。

### 技法库 techniques
- `20261106-black-screen-text-cards` — **黑屏与字卡：用"黑"讲故事** — `topics/techniques/black-screen-text-cards.md` — 黑屏的六种功能、字卡的七种类型、排版参数（字体 / 字号 / 字距 / 停留帧数）、免费可商用字体，以及为什么字卡绝不能让 AI 生成。
- `20261106-editing-rhythm` — **剪辑节奏：镜头时长、卡点、闪帧与 AI 素材的剪法** — `topics/techniques/editing-rhythm.md` — 各幕的镜头时长参考值、十种剪辑手法（卡点、闪帧、匹配剪辑、J/L 剪辑、变速等），以及"生成 5–10 秒、只用最好的 1–2 秒"的 AI 素材剪辑原则。
- `20261106-meta-endings` — **元结尾字卡库：让"永不上映"成为最后一个反转** — `topics/techniques/meta-endings.md` — 12 种"这部电影为什么永远不会上映"的元结尾字卡（证物、拒绝授权、重看、泄露、涂黑、寻人、诅咒、未完成、AI、遗忘、日期回滚、审查），附中英文案、故事需要提供什么、适配方案，以及三条设计规则和合规注意。
- `20261106-music-strategy` — **音乐策略：熟悉旋律的陌生化（以及如何避开版权）** — `topics/techniques/music-strategy.md` — 预告配乐的五种策略，以及为什么比赛里不能用热门翻唱；用公有领域的《友谊地久天长》做双版本变奏，同时满足"熟悉感"和版权安全。
- `20261106-sound-design` — **声音设计：BRAAAM、静默、滴答与声音押韵** — `topics/techniques/sound-design.md` — 预告常用的八种声音武器（BRAAAM、Ping、升调、抽空、倒放、次低频、声音押韵、有源音乐变调）的用法，以及《明日不来》的声音设计表。
- `20261106-trailer-structure` — **预告片结构：三幕 + 按钮 + 能量曲线** — `topics/techniques/trailer-structure.md` — 预告的三幕微缩结构（提问 → 升级 → 转折 + 片名 + 按钮）、"永不解决"原则、能量曲线，以及 30 / 60 / 90 秒三种时长的时间分配表。
- `20261106-visual-motifs` — **视觉母题库：12 种让人记住的画面** — `topics/techniques/visual-motifs.md` — 从 30 部作品的预告中提炼的 12 种视觉母题（尺度对比、对称、单色世界、黑暗中的红、倒放物理、冻结时间、不露脸的反派等），每种都附上在《明日不来》中的用法和提示词关键词。
- `20261106-withholding-mystery` — **留白与悬念营销：少给，让观众自己去找** — `topics/techniques/withholding-mystery.md` — 八种"少给信息"的手法（只给日期、密码彩蛋、ARG、倒计时、突袭发布、藏起怪物、合法误导、线下装置），以及如何用它们拉高评分里的"想看度"。

### 提示词库 prompts
- `20261106-exhibit-47-scene-images` — **《第 47 号证物》场景图（AKOOL 生成）：风格块、提示词、选用版本与问题** — `topics/prompts/exhibit-47-scene-images.md` — 用 AKOOL 图像生成（flux-krea-dev）为 6 个场景各出一张环境参考图：统一的 SCENE-STYLE 风格块和 NEG-SCENE 负面词、6 条场景提示词、实际选用的版本和 AKOOL 任务号、每张图和设定不一致的地方，以及用户整理的即梦搜索词。白模按这些图搭建。
- `20261106-exhibit-47-shot-prompts` — **《第 47 号证物》镜头提示词库（按证物画面类型分组）** — `topics/prompts/exhibit-47-shot-prompts.md` — 主方案预告的全部提示词：六种"证物画面"风格块（执法记录仪 / 监控 / 无人机 / 审讯室 / 旧录像 / 第 47 号证物视角）、23 个编号镜头、监控墙素材池、后期叠字规范，以及配乐、音效和配音提示词。
- `20261106-music-sfx-prompts` — **音乐、音效与配音提示词** — `topics/prompts/music-sfx-prompts.md` — 《友谊地久天长》温暖版 / 扭曲版配乐、悬疑垫底音、16 种音效清单，以及每个角色的配音声音设定提示词。
- `20261106-prompt-formula` — **AI 视频提示词公式与模型选择（AKOOL 上的 Veo / Kling / Seedance / Wan）** — `topics/prompts/prompt-formula.md` — 九段式通用提示词公式、六条硬规则、各模型在 AKOOL 上的长处与分工、镜头和运镜词汇表、多镜头写法，以及常见翻车的修法。
- `20261106-reference-sheet-reverse-prompts` — **设定图的图片转提示词学习记录（反推、交叉核对与即梦搜图清单）** — `topics/prompts/reference-sheet-reverse-prompts.md` — 用 LibTV 的两个视觉模型（GVLM 3.1、Qwen 3 VL Flash）对已通过的设定图做"图片转提示词"，交叉核对后锁定背景、分隔线、手套、疤等细节；记录反推提问模板、四条经验、第十三人设定图的验收结果、即梦搜图的手动清单，以及比赛规则（原创、AKOOL 参与）的注意事项。
- `20261106-shot-prompt-library` — **镜头提示词库（按功能分组，编号 A1–G4）** — `topics/prompts/shot-prompt-library.md` — 《明日不来》全部可用镜头的完整英文提示词，分为开场钩子 / 世界 / 悬疑 / 动作 / 时间特效 / 对白 / 结尾按钮七组，每条都有编号（A1–G4）、推荐模型和时长。
- `20261106-style-anchor` — **风格锚 STYLE-A / 负面词 NEG-A / 场景色彩块** — `topics/prompts/style-anchor.md` — 每条提示词都要原样粘贴的英文 / 中文风格锚、负面词，以及每个场景的固定色彩光线块，保证全片质感统一。
- `20261106-text-card-copy` — **字卡、标语与台词文案库（中英双语）** — `topics/prompts/text-card-copy.md` — 《明日不来》的句子阶梯字卡、定义句、三词标语、片名卡、日期卡、结尾卡，以及全部台词和画外音（含语气说明），可直接放进剪辑软件。

### 制作方案 production
- `20261106-akool-workflow` — **AKOOL 制作流程与 14 天排期** — `topics/production/akool-workflow.md` — 从角色设定图、动态分镜、图生视频、口型与配音，到剪辑、遮幅、AKOOL 标志、混音和导出的十步流程，按 11 月 20 日截止倒排的 14 天日程，以及"AKOOL 使用"的留证方法。
- `20261106-exhibit-47-whitebox-previs` — **《第 47 号证物》白模预演（Blender）：6 个场景、23 个机位、遮挡检测与 9 条发现** — `topics/production/exhibit-47-whitebox-previs.md` — 按 AKOOL 场景图用 Blender 搭的全方块白模：6 个场景各一套（附与场景图对齐的参考机位），每个镜头摆好人物、按 89 秒分镜表的时间码让摄影机走一遍，用射线检测核对谁在画面里、谁被挡住；记录每个镜头的机位、动作时间、可见性结果，以及由此发现并已改进提示词的 9 个问题。
- `20261107-exhibit-47-keyframes` — **《第 47 号证物》关键帧：v1（AKOOL 白模引导）与 v2（LibTV 人物 + AKOOL 场景，画面自带证物画质）** — `topics/production/exhibit-47-keyframes.md` — 现行是 v2，共 30 张：有人的镜头 23 张在 LibTV 生成（中文提示词，参考 v3 设定图和白模），场景和道具 7 张在 AKOOL 生成；执法记录仪、监控、红外和旧录像的画质直接生成在画面里，只有屏幕文字留到后期。笔记里有每张的做法和取舍、45 次生成的日志，以及 v1、v2 各 10 条教训。
- `20261107-exhibit-47-video-clips` — **《第 47 号证物》AKOOL 图生视频：Akool Premium 首轮、Seedance 升级、配音和口型同步，粗剪 v1 和 v2** — `topics/production/exhibit-47-video-clips.md` — 全部在 AKOOL 里完成。首轮 Akool Premium 29 条；第二轮 Seedance 1.0 Pro Fast 升级 13 个镜头，9 条胜出，C2 开场用 Seedance Lite；V1–V12 用 AKOOL 配音，I2 用 Talking Photo。第三轮把剩下的镜头用 Pro Fast 重做（8 条 720p、3 条 1080p，7 条胜出），拼成带完整声音的 88 秒粗剪 v2。共 57 条视频，1035 积分。
- `20261107-exhibit-47-sound-mix` — **《第 47 号证物》音乐、音效和混音（粗剪 v2）** — `topics/production/exhibit-47-sound-mix.md` — AKOOL 不做声音，所以 18 个音效用 LibTV Seed Audio 1.0、配乐 SC1 用 LibTV ElevenMusic V3 生成。配乐剪成 4 段，音效放了 49 处，四轨混成 -13.8 LUFS，两处全静音落在黑场上。附提示词、对齐方法和 10 条教训；还没有人耳试听。
- `20261106-exhibit-47-shot-list` — **《第 47 号证物》90 秒档分镜表（逐镜头时间码）** — `topics/production/exhibit-47-shot-list.md` — 主方案参赛版分镜（v2，审片后修订），总长 88 秒：时间码、提示词编号、字卡、台词和声音；"只配发 12 台 + 第 47 号证物遗失"的不可能证据链；两只手同一道疤的线索；第十三人 4 次出场（第 4 次是身份线索）；预告刻意不交代的内容；以及 30 秒前导版和 9:16 竖屏版的改法。
- `20261106-submission-checklist` — **提交检查清单** — `topics/production/submission-checklist.md` — 发布和提交前逐项勾选：时长、原创性、AKOOL 标志、版权素材、平台发布与话题标签、提交表单说明、评分自查。
- `20261106-untomorrow-shot-list` — **《明日不来》75 秒分镜表（逐镜头时间码）** — `topics/production/untomorrow-shot-list.md` — 参赛主版本的 27 个镜头，每个镜头都有时间码、时长、提示词编号、字卡、声音和台词，以及 30 秒社交前导版和 9:16 竖屏版的改法。
