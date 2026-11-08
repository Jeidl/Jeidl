# 武侠电影预告片知识库 — 索引

武侠风格电影预告片的**剪辑、分镜、时机、秒数、风格**知识库。共 9 个主题、42 篇原子笔记，每篇只讲一个主题，用 `id` 互相引用。

## 快速入口
| 我想…… | 打开 |
|---|---|
| 马上做一支 2 分钟预告 | `topics/structure/timeline-120s.md` → `topics/shots/storyboard-template.md` → `topics/workflow/production-workflow.md` |
| 知道每段该几秒、几帧 | `topics/structure/cutting-pace-and-frames.md` |
| 做 15 / 30 / 60 秒或竖版 | `topics/structure/timeline-short-forms.md` |
| 打斗怎么剪才有"武侠味" | `topics/editing/pause-burst-pause.md`、`topics/editing/hong-kong-constructive-editing.md` |
| 选配乐、做声音 | `topics/sound/music-structure.md`、`topics/sound/sound-design-palette.md` |
| 用 AI 生成预告素材 | `topics/workflow/ai-video-prompting.md` |

## 使用方法（给 AI 代理和读者）
1. 先读本索引，按描述挑 1–3 篇笔记打开，不要全量扫描。
2. 引用时注明笔记 `id`；涉及事实时，顺着笔记里的【S##】查 `topics/reference/sources.md`。
3. 内容标记：**【来源 S##】** 有外部来源支撑；**【经验法则】** 是根据来源和行业惯例综合出的可操作规则，不是实测数据，可以按项目调整。
4. 局限：本库的网络研究基于检索结果摘要（运行环境不允许直接打开网页），重要事实建议回原文核实。

## 更新规则（给 AI 代理）
- 新想法 → 新建原子笔记；同一想法有新信息 → 原地修改并更新 `updated`。
- 新建、改名、删除笔记时，必须在同一次修改中更新本注册表和对应主题的 `_topic.md`：运行 `python3 tools/build_index.py` 自动重建，再运行 `python3 tools/lint_kb.py` 检查 frontmatter、标签、链接、来源编号和孤立笔记。
- `id` 格式为 `YYYYMMDD-slug`，永不修改、永不复用；文件名与 slug 一致（小写 kebab-case）。
- 只使用下方受控标签；需要新标签时先在这里添加。
- 笔记之间用相对链接，并写明关系；每个链接目标都要列在 frontmatter 的 `related` 中。
- 拉片得到的新数据：按 `topics/workflow/trailer-breakdown-method.md` 写成新的案例笔记。

## 受控标签
`foundation`、`marketing`、`structure`、`timing`、`editing`、`rhythm`、`shots`、`camera`、`storyboard`、`sound`、`music`、`dialogue`、`color`、`typography`、`style`、`case-study`、`workflow`、`ai`、`reference`

## 注册表
格式：`id` — **标题** — `路径` — 一句话描述。

<!-- REGISTRY:START -->
### foundations — 基础
- `20261108-release-cadence` — **宣发节奏与版本矩阵** — `topics/foundations/release-cadence.md` — 预告片何时开始制作、拿到什么素材，以及从先导到终极预告的发布节奏（含《射雕》《镖人》两个春节档实例）。
- `20261108-trailer-types-and-lengths` — **预告片类型与时长** — `topics/foundations/trailer-types-and-lengths.md` — 先导/定档/正式/角色/终极预告、特辑、TV spot、竖版短视频各自的常见时长、目的与武侠片侧重点，以及 2分30秒上限惯例。
- `20261108-wuxia-trailer-essence` — **武侠预告片的核心气质** — `topics/foundations/wuxia-trailer-essence.md` — 武侠预告片与一般动作片预告的根本区别——卖"侠"与"江湖"而不只是打斗；以静衬动、清晰可读、奇观与"以武载道"的平衡。

### structure — 结构与时机
- `20261108-cold-open-and-button` — **冷开场与片尾按钮** — `topics/structure/cold-open-and-button.md` — 武侠预告的四种冷开场写法（极静远景、金句先行、动作截断、声音先行）和片名后按钮 / 彩蛋的类型与时长。
- `20261108-cutting-pace-and-frames` — **剪辑速度与帧数换算** — `topics/structure/cutting-pace-and-frames.md` — 24/25/30 fps 下秒与帧的换算表，各段落的平均镜长与每分钟剪辑数参考值，以及"快切也要可读"的下限。
- `20261108-three-act-structure` — **预告片三幕结构（武侠版）** — `topics/structure/three-act-structure.md` — 预告片三幕各占多少秒、各幕做什么，以及武侠片的"入江湖—风波起—决战"映射；先导预告的两幕变体。
- `20261108-timeline-120s` — **120 秒武侠预告逐秒时间轴模板** — `topics/structure/timeline-120s.md` — 可直接套用的 2 分钟武侠预告逐秒时间轴（段落、镜长、画面、声音、字幕卡），附 2分30秒扩展方案和镜头数估算。
- `20261108-timeline-short-forms` — **短版本时间轴：60 秒先导、30 秒、15 秒竖版、角色预告** — `topics/structure/timeline-short-forms.md` — 60 秒先导（两幕）、30 秒 spot、15 秒 9:16 竖版和 30–45 秒角色预告的逐秒模板，以及竖版构图与前 3 秒钩子的要点。

### editing — 剪辑
- `20261108-climax-montage` — **第三幕高潮蒙太奇** — `topics/editing/climax-montage.md` — 高潮蒙太奇的分组升级结构、BPM 与帧数对齐表、镜头交替规则和"人的镜头"配额，确保快而不空。
- `20261108-hong-kong-constructive-editing` — **香港建构式剪辑手法** — `topics/editing/hong-kong-constructive-editing.md` — 港式武侠"建构式剪辑"的八种手法（动作切、冲击点切、重叠剪辑、抽格、插入特写、视线衔接、省略、拼接轻功），以及分段拍摄和清晰可读原则在预告中的用法。
- `20261108-opera-percussion-rhythm` — **锣鼓经与剪辑点** — `topics/editing/opera-percussion-rhythm.md` — 京剧武打与锣鼓点如何影响港式武侠的节奏，以及把"亮相""急急风""撕边"等锣鼓概念类比为预告剪辑点的方法。
- `20261108-pause-burst-pause` — **停—爆—停（pause/burst/pause）节奏** — `topics/editing/pause-burst-pause.md` — Bordwell 提出的港式动作"停—爆—停"节奏是什么、它的局限，以及如何把它用到预告片的单个动作单元和整体结构上（含镜头、声音对照表）。
- `20261108-speed-ramp-and-slow-motion` — **变速（speed ramp）与慢镜头** — `topics/editing/speed-ramp-and-slow-motion.md` — 升格、降格、变速的定义与常用参数（100%→10–20% 约 0.5–1 秒），武侠慢镜该拍什么（介质被力量扰动），每支预告的慢镜数量与节拍对齐。
- `20261108-transitions` — **转场手法** — `topics/editing/transitions.md` — 武侠预告常用转场（硬切、黑场、闪白、刀光划屏、水墨晕染、匹配剪辑、J/L-cut、叠化、定格）的时长与适用位置。

### shots — 分镜与镜头语言
- `20261108-camera-movement` — **运镜与动作摄影** — `topics/shots/camera-movement.md` — 固定、推、拉、摇、移、升降、环绕、手持、威亚等运镜在武侠预告中的情绪含义和适用流派，以及长镜头与快切两种传统的对照。
- `20261108-shot-vocabulary` — **景别与武侠镜头词汇表** — `topics/shots/shot-vocabulary.md` — 景别、角度在武侠预告中的情绪用途，以及 12 个武侠"招牌镜头"（背影孤客、拔刀一寸、两端对峙、三镜轻功、边缘动作等）和它们适合放在哪一幕。
- `20261108-storyboard-template` — **预告片分镜表模板** — `topics/shots/storyboard-template.md` — 可复制的预告分镜表字段（镜号、时码、帧数、段落、景别、运镜、画面、停/爆、速度、声音、字幕卡、转场、备注），附一部原创示例片前 14 镜的填写示范。
- `20261108-visual-motifs` — **武侠意象库** — `topics/shots/visual-motifs.md` — 竹林、大漠、客栈、雨、雪、湖面、落叶、城头、棋局与琴、伞、马与镖车等武侠意象各自的情绪、代表作品、预告位置和配套声音。

### sound — 声音与音乐
- `20261108-chinese-instrument-roles` — **民乐乐器情绪分工** — `topics/sound/chinese-instrument-roles.md` — 箫、笛、古琴、琵琶、古筝、二胡、唢呐、大鼓、京剧锣鼓、编钟、人声，以及大提琴、弦乐、铜管等西洋乐器在武侠预告中的情绪与段落分工表。
- `20261108-dialogue-and-voiceover` — **台词与旁白** — `topics/sound/dialogue-and-voiceover.md` — 武侠预告用台词而少用旁白；2 分钟预告放 4–8 句台词，四类台词（世界观、冲突、主题、按钮）的位置，以及"放出来但不解释"和海外版字幕的做法。
- `20261108-music-structure` — **预告配乐结构** — `topics/sound/music-structure.md` — 预告配乐的三段式结构与 hit 布局、史诗混合配乐的常见 BPM（约 90–130）与配器，以及武侠配乐的 A/B/C 段写法、spotting 表和"侠味"提醒。
- `20261108-silence-and-hits` — **静默与重击** — `topics/sound/silence-and-hits.md` — 为什么静默能让下一记 hit 更响、一支预告放几个"真空点"、静默多长、hit 怎么分三级，以及台词与静默的配合。
- `20261108-sound-design-palette` — **武侠预告音效素材库** — `topics/sound/sound-design-palette.md` — 预告通用设计音（drone、riser、whoosh、hit、sub drop、braam）的定义与配合，以及武侠专属音效分类（兵器、身体、环境）和"拔刀 shing"等的分层方法。

### style — 视觉风格
- `20261108-color-grading` — **调色与色彩** — `topics/style/color-grading.md` — 武侠预告的六种色彩方案（水墨灰阶加一点红、主题色分章、大漠暖金、竹林冷青、雨夜冷蓝、自然古典），《英雄》《影》的色彩实例，以及预告整体调色的统一规则。
- `20261108-director-styles` — **导演 / 流派风格谱系与预告对策** — `topics/style/director-styles.md` — 胡金铨、张彻、徐克、程小东、李安、张艺谋、王家卫、侯孝贤、袁和平等九种武侠风格的特征，以及据此调整预告剪辑速度、配乐和色彩的对照表。
- `20261108-title-cards-typography` — **字幕卡与书法片名** — `topics/style/title-cards-typography.md` — 书法片名的作用和制作路径、字幕卡五种类型与停留时长、动效（墨迹、笔触、刀光、印章）、书体气质对照、文案写法和字体版权提醒。

### case-studies — 案例
- `20261108-case-a-touch-of-zen` — **案例：《侠女》（A Touch of Zen，胡金铨，1971）** — `topics/case-studies/case-a-touch-of-zen.md` — 《侠女》竹林之战如何用瞬间镜头和长镜交替、跨镜头"缝合"轻功，以及它对武侠预告"意境 + 快闪"写法的启示。
- `20261108-case-blades-of-the-guardians` — **案例：《镖人：风起大漠》（袁和平，2026）** — `topics/case-studies/case-blades-of-the-guardians.md` — 2026 春节档《镖人》"亮招！"版定档预告以大漠风光开场、再接近身搏斗、兵刃交锋和马上厮杀，以及影片后来的票房表现。
- `20261108-case-condor-heroes-2025` — **案例：《射雕英雄传：侠之大者》（徐克，2025）** — `topics/case-studies/case-condor-heroes-2025.md` — 2025 春节档《射雕》的多版预告（"高手"版、"铁血丹心"特别预告、第二支长预告）的内容侧重，以"侠之大者"为主题，以及学界对特效奇观压倒武侠美学的批评。
- `20261108-case-crouching-tiger` — **案例：《卧虎藏龙》（Crouching Tiger, Hidden Dragon，李安，2000）** — `topics/case-studies/case-crouching-tiger.md` — 《卧虎藏龙》的中西融合配乐、广角长镜的竹林戏，以及预告中用慢叠化标示情绪转换的做法。
- `20261108-case-flying-swords-dragon-gate` — **案例：《龙门飞甲》预告（Flying Swords of Dragon Gate，徐克，2011）** — `topics/case-studies/case-flying-swords-dragon-gate.md` — 影评人认为《龙门飞甲》预告大约 45 秒才"真正进入状态"，说明开场过慢的风险和冷开场钩子的必要。
- `20261108-case-hero` — **案例：《英雄》（Hero，张艺谋，2002）** — `topics/case-studies/case-hero.md` — 《英雄》的色彩分段结构和意象场景，以及北美版预告用"Quentin Tarantino Presents"开场、2004 年首周登顶的海外包装经验。
- `20261108-case-shadow` — **案例：《影》（Shadow，张艺谋，2018）** — `topics/case-studies/case-shadow.md` — 《影》用布景、服装和阴雨天实现水墨灰阶、只让血色与肤色透出红，是"灰阶 + 一点红"调色方案的范本。
- `20261108-case-the-assassin` — **案例：《刺客聂隐娘》（The Assassin，侯孝贤，2015）** — `topics/case-studies/case-the-assassin.md` — 《刺客聂隐娘》的极简长镜和边缘动作，以及艺术向武侠预告如何以静为主、用极少剪辑点卖"气质"。
- `20261108-case-the-blade` — **案例：《刀》（The Blade，徐克，1995）** — `topics/case-studies/case-the-blade.md` — 《刀》用竹子断裂声、钢铁相击声构成打斗节奏，说明声音设计如何决定武侠预告的冲击感。
- `20261108-case-the-grandmaster` — **案例：《一代宗师》（The Grandmaster，王家卫，2013）** — `topics/case-studies/case-the-grandmaster.md` — 《一代宗师》开场雨战的 1000fps 慢镜，以及评论对"重复慢镜"的批评，作为武侠预告慢镜配额的正反参照。

### workflow — 工作流
- `20261108-ai-video-prompting` — **用本知识库驱动 AI 视频生成** — `topics/workflow/ai-video-prompting.md` — 把分镜表转成 AI 视频生成提示词的公式（景别 + 主体 + 动作 + 环境 + 光线 + 运镜 + 速度 + 质感 + 时长），中英文示例，"停"镜与"爆"镜的生成策略和原创性提醒。
- `20261108-production-workflow` — **武侠预告制作工作流** — `topics/workflow/production-workflow.md` — 从拿到粗剪到交付多版本的 12 步流程：素材日志、定位、音乐先行、纸面时间轴、台词骨架、粗剪、卡点、变速、声音、调色字幕、衍生版本、质检。
- `20261108-qc-checklist` — **武侠预告质检清单** — `topics/workflow/qc-checklist.md` — 交付前逐项检查的清单：结构与时长、节奏可读性、声音混音、画面调色、字幕卡与片名、版权合规、多版本规格。
- `20261108-trailer-breakdown-method` — **拉片方法：如何拆解一支预告并补充本知识库** — `topics/workflow/trailer-breakdown-method.md` — 逐镜拆解（拉片）一支武侠预告的步骤、记录表字段和应计算的指标（各幕平均镜长、每分钟剪辑数、hit 数、静默数、慢镜数、字幕卡时长），以及把结果存为新案例笔记的方法。

### reference — 参考
- `20261108-glossary` — **中英术语表** — `topics/reference/glossary.md` — 预告片剪辑、港式动作、声音设计、分镜与宣发相关术语的中英对照和一句话释义。
- `20261108-sources` — **来源清单与可信度** — `topics/reference/sources.md` — 本知识库引用的全部外部来源（S01–S50）的 URL、内容和可信度等级（A 学术或一手 / B 媒体与评论 / C 博客、商品页、论坛），以及研究方法和局限说明。
<!-- REGISTRY:END -->
