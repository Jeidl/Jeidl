---
id: 20261106-exhibit-47-character-bible
title: 《第 47 号证物》人物与道具设定（一致性锚点）
tags: [concept, prompt, production]
created: 2026-11-06
updated: 2026-11-07
related: [20261106-exhibit-47-story, 20261106-exhibit-47-shot-prompts, 20261106-exhibit-47-shot-list, 20261106-character-bible, 20261106-style-anchor, 20261106-prompt-formula, 20261106-akool-workflow, 20261106-longlegs-teasers, 20261106-reference-sheet-reverse-prompts]
summary: 主方案的人物设定（诺拉、沃德、第十三人、布兰特、特勤组、旧录像里的手）、可直接粘贴的英文角色块（NORA-REF 等）、道具与场景块、颜色规则，以及统一风格的设定图提示词（SHEET-STYLE 等固定块 + 母版参考链）；沃德在预告里只露手和声音。
---

# 《第 47 号证物》人物与道具设定（一致性锚点）

> Summary: 主方案的人物设定（诺拉、沃德、第十三人、布兰特、特勤组、旧录像里的手）、可直接粘贴的英文角色块（NORA-REF 等）、道具与场景块、颜色规则，以及统一风格的设定图提示词（SHEET-STYLE 等固定块 + 母版参考链）；沃德在预告里只露手和声音。

## 背景

故事见 [完整故事](exhibit-47-story.md)。用法与 [《明日不来》角色圣经](character-bible.md) 相同：先锁定一张参考图，之后每个镜头都用"参考图 + 下面的固定英文块"，**一字不改**。

## 预告片的三条铁律

1. **沃德不露脸**。预告里只出现他的**声音**和**右手**。这样既不会剧透，也省掉了一张需要保持一致的脸。
2. **第十三人恰好出现 4 次**，对应结尾字卡"第十三个人出现在 4 个画面里"：楼梯间队尾的剪影、冷冻门镜面里的头盔、拉住诺拉的手、审讯桌上沃德的手。其他镜头里**不能**出现他，具体位置见 [分镜表](../production/exhibit-47-shot-list.md)。
3. **特勤组全员戴面罩**，只有布兰特在"摘面罩"那场戏里露脸。需要保持一致的脸只有**诺拉**一个人。

## 人物与角色块

### NORA-REF：诺拉·凯德（主角，唯一的幸存者）

- **身份**：26 岁，第七特勤组新人，7-12 号；前军医。
- **性格**：安静、警惕、不哭。在审讯室里她不是在崩溃，而是在拼命回忆。
- **识别点**：**下巴上的旧伤疤**、灰色眼睛、短发。

```text
Officer Nora Kade, a 26-year-old woman with a short dark undercut, a thin healed scar along her chin, steady grey eyes, pale skin reddened by cold
```

服装块（按场景加在后面）：

| 代号 | 场景 | 英文 |
|---|---|---|
| NORA-TAC | 突袭 | `wearing black tactical gear and a ballistic helmet with a white stenciled number 7-12, black balaclava pulled down to her chin` |
| NORA-ROOM | 审讯室 | `wearing an oversized grey sweatshirt, a white hospital wristband, frost-reddened knuckles, hair still damp` |
| NORA-DAWN | 走出冷库 | `in black tactical gear covered in frost, carrying her helmet in one hand` |

### WARD-HAND：沃德的右手（预告里只出现这只手）

- **身份**：伊莱亚斯·沃德，54 岁，督察署调查官，也就是第十三个人。
- **声音**：低沉、温和、耐心。他越温柔越可怕。
- **识别点**：**右手背上一道发亮的旧烧伤疤**，从指节延伸到手腕。

```text
the right hand of a man in his fifties, resting on a grey metal table, an old shiny burn scar across the back of the hand from the knuckles to the wrist, the cuff of a charcoal suit jacket, a plain steel wristwatch
```

### THIRTEENTH-REF：第十三人（突袭时的沃德）

```text
a thirteenth tactical officer in identical black tactical gear, ballistic helmet with a white stenciled number 7-12, full black balaclava and dark goggles, face never visible; the glove on his right hand is torn open across the back, revealing an old shiny burn scar
```

- 注意：他的头盔编号**也是 7-12**，和诺拉一样。这是报数时出现两个"十二"的原因。
- 他**从不举枪**。在任何镜头里，他的姿态都是平静站立或缓慢行走。

### BRANDT-REF：科尔·布兰特（组长，只在"摘面罩"和"我们埋了你"两场露脸）

```text
Sergeant Cole Brandt, a 45-year-old man, heavy stubble, bloodshot eyes, balaclava ripped down, black tactical gear, ballistic helmet with a white stenciled number 7-01
```

### UNIT-REF：第七特勤组（群像）

```text
police tactical officers in identical black tactical gear, ballistic helmets with white stenciled numbers, black balaclavas and goggles, rifles with mounted flashlights, plain grey shoulder patches with no insignia
```

**不要出现任何真实警徽或真实机构标志。**

### OLD-HANDS：旧录像里举起的双手（三年前）

```text
the bare hands of a teenager raised high in surrender, the sleeves of a dark hoodie, frost-covered crates behind, harsh flashlight beam on the hands
```

只拍手，**不拍脸**，不出现血腥画面。

## 道具

| 代号 | 英文描述 | 备注 |
|---|---|---|
| EX47 | `a scuffed black police body camera covered in frost, a small glowing red recording light, a faded red cardboard evidence tag tied to it with white string` | **全片唯一的红色主题物**。标签上的字后期叠加 |
| BAGS | `thirteen black body cameras in clear plastic evidence bags laid in a single row on a steel forensic table, twelve with white tags, one with a red tag` | |
| PEN | `a cheap black ballpoint pen` | 按钮镜头里沃德转动它 |
| PIPE | `old refrigeration pipes thick with frost along the ceiling` | 被打穿后喷出白色氨气 |

## 场景

| 代号 | 英文描述 |
|---|---|
| LOC-GATE | `an abandoned harbor cold-storage plant, rusted loading docks and shutters, untouched snow, grey overcast dawn` |
| LOC-STAIR | `a narrow concrete stairwell in total darkness, frost on the railings, breath vapor` |
| LOC-FREEZER | `a vast abandoned freezer hall, rows of empty meat hooks on rails, hanging plastic strip curtains, frosted steel walls, freezing fog drifting at floor level` |
| LOC-ROOM4 | `a small freezer room stacked with frosted wooden crates, a single meat hook, a polished steel door` |
| LOC-INTERVIEW | `a bare police interview room, grey metal table, two chairs, cold flat fluorescent overhead light, a dark one-way mirror` |
| LOC-EVIDENCE | `a forensic evidence room, a long steel table under harsh white LED light, clear plastic evidence bags` |

## 颜色规则

- **唯一的红色属于证物**：EX47 的红色标签、红色录制灯。其他物体都不要出现大面积红色。
- 突袭画面以红外单色（灰绿）和手电冷白光为主；枪口火光是橙白色。
- 审讯室和证物室：冷蓝灰，日光灯。

## 设定图提示词（统一风格 v2）

### 为什么 v1 的四视图和手部图风格不一样

v1 两条提示词只共用了 `photorealistic` 和 `neutral grey` 两个词，光线、镜头、调色、版式要么不一样，要么没写，留给模型自己猜：

| 项目 | 诺拉四视图 v1 | 沃德的手 v1 | 后果 |
|---|---|---|---|
| 品类词 | `Character reference sheet, photorealistic` | `Reference sheet, photorealistic macro photography` | "macro" 会让模型改拍**微距产品照**：浅景深、背景虚化、戏剧光 |
| 光线 | `soft even lighting` | 没写 | 手部图的光由模型自己决定 |
| 背景 | `neutral grey studio background` | `neutral grey background` + `flat on a table` | 桌子带进了材质和环境，不再是同一个影棚 |
| 镜头与景深 | 没写 | 没写（macro 暗示浅景深） | 清晰度和虚化程度不同 |
| 白平衡与调色 | 没写 | 没写 | 色温和反差各自随机 |
| 版式 | 4 格，side by side | 3 格，没写怎么排 | 版式不同 |
| 生成方式 | 文生图 | 文生图，互相独立 | 没有共同的参考图，两次都是随机结果 |

另外还有三处问题：

1. 手部图漏了 WARD-HAND 里的**西装袖口和钢表**，和镜头 I3 对不上。
2. 第十三人图用"黑背景 + 侧面手电光"，是**第三种风格**。
3. 两个疤都只写在文字里，没有专门的特写格，验收时很难看清。

### 统一规则

1. 每张设定图都由同一组块拼成：`[SHEET-STYLE] [SHEET-LAYOUT] + 主体段 + [SHEET-END]`。这些块**一字不改**。
2. 每张图都是 **4 格横排**：3 个角度 + 1 格识别点特写（诺拉的下巴疤、沃德的烧伤疤、第十三人撕开的手套）。
3. **诺拉四视图是风格母版**，最先生成。手部图和第十三人图生成时，把母版接进来当参考图，并在最前面加 `[SHEET-MATCH]`。如果母版不是 4 格（诺拉 v2 就是这种情况，见下方记录），就改用**已通过的 4 格设定图**（沃德的手 v2）做参考，否则参考图会把版式带偏。
4. 三张图用**同一个模型、同一画质、同一画幅**（LibTV：`nebula-ultra`、2K、16:9）。
5. 设定图里**不要把这些词当正面描述**：macro、cinematic、dramatic、moody、film、flashlight、dark background、backlight，以及 table、room 这类环境词。它们属于镜头提示词。设定图只负责"长什么样"，"画面是什么风格"交给镜头的 S-* 风格块。

### 固定块

**SHEET-STYLE**（每张设定图的开头）
```text
Photorealistic character reference sheet, clean studio photography. Shot on a full-frame digital camera with an 85mm lens at f/8, everything in sharp focus. Plain seamless mid-grey paper backdrop, the same flat grey in every panel. Soft, even, almost shadowless light from a large softbox in front of the subject and slightly above, with gentle fill from both sides; no rim light, no hard shadows, no spotlight, no vignette. Neutral daylight white balance, true-to-life colors, medium contrast, no color grading, no film grain.
```

**SHEET-LAYOUT**（v2.1：分隔线从 light-grey 改成 white。已通过的手部图实际出的是白线，见 [图片转提示词学习记录](../prompts/reference-sheet-reverse-prompts.md)）
```text
Layout: four equal vertical panels in one horizontal row, separated by thin straight white gutters about 1% of the image width; camera height, lighting and backdrop are identical in every panel; the subject is centered and fills each panel.
```

**SHEET-END**（每张设定图的结尾）
```text
The same subject in all four panels, with consistent identity and details. Natural skin and material texture, fine detail. No captions, no labels, no panel numbers, no watermark, no logo.
```

**SHEET-MATCH**（接了母版参考图时，放在最前面；`<母版>` 换成参考图的引用，LibTV 里写 `{{Node 节点ID}}`）
```text
Style reference: <母版>. Match it exactly in backdrop, lighting, white balance, contrast, lens look and four-panel layout. Take only the photographic style from it, not the person or the clothing.
```

**NEG-SHEET**（AKOOL 的 negative_prompt 框；没有负面词框的模型不用）
```text
macro photography, shallow depth of field, bokeh, dramatic lighting, rim light, spotlight, hard shadows, vignette, dark background, black background, cinematic color grading, color cast, film grain, table, room, environment, captions, labels, watermark, logo, extra fingers, distorted hands, different person in each panel
```

### 三张设定图

**① 诺拉四视图（风格母版，最先生成）**

`[SHEET-STYLE] [SHEET-LAYOUT]` + 下面这段 + `[SHEET-END]`
```text
Panel 1: front view, head and shoulders. Panel 2: three-quarter view, head and shoulders. Panel 3: side profile facing left, head and shoulders. Panel 4: close-up of the lower face and chin, showing the scar clearly. Subject: Officer Nora Kade, a 26-year-old woman with a short dark undercut, a thin healed scar along her chin, steady grey eyes, pale skin reddened by cold, wearing an oversized grey sweatshirt. Neutral expression, mouth closed.
```

**② 沃德的右手（接母版）**

`[SHEET-MATCH] [SHEET-STYLE] [SHEET-LAYOUT]` + 下面这段 + `[SHEET-END]`
```text
Panel 1: the back of the right hand resting flat on a matte grey surface that matches the backdrop, with the cuff of a charcoal suit jacket and a plain steel wristwatch at the wrist. Panel 2: close-up of the back of the same hand, showing the scar in detail. Panel 3: the same hand turning a cheap black ballpoint pen between its fingers. Panel 4: the same hand in a black tactical glove torn open across the back, revealing the same scar, with the sleeve of black tactical gear. Subject: the right hand of a man in his fifties, with an old shiny burn scar across the back of the hand from the knuckles to the wrist, the same shape, size and position in every panel. Normal anatomy with five fingers.
```

手放在和背景同色的哑光灰面上，不放金属桌。金属桌在镜头 I3 里由 LOC-INTERVIEW 提供。

**③ 第十三人（明确版，接沃德的手 v2）**

参考图只接**沃德的手 v2**：它是 4 格，背景、光线和母版一致，第 4 格就是要复制的手套和疤。下面是完整提示词，已经把固定块拼好，可以直接粘贴：

```text
Style and detail reference: <沃德的手 v2>. Match it exactly in backdrop, lighting, white balance, contrast, lens look, the thin white gutters and the four-panel layout. From its fourth panel, copy the black fingerless tactical glove with the wide velcro wrist strap, the hole torn open across the back of the hand, and the raised, shiny, pinkish-white burn scar showing through the hole. Take nothing else from it. [SHEET-STYLE] [SHEET-LAYOUT] Panel 1: front view, full body from the top of the helmet to the soles of the boots, standing upright and facing the camera, arms hanging relaxed at his sides, hands empty. Panel 2: three-quarter view, full body, turned halfway toward the right edge of the panel, same pose. Panel 3: right-side profile, full body, facing the right edge of the panel so that his right side and right hand are toward the camera, same pose. Panel 4: close-up of his right hand seen from directly above, back of the hand up, framed like the fourth panel of the reference, with the sleeve of a black combat shirt at the wrist. Subject: [THIRTEENTH-REF]. Gear details: matte black ballistic helmet with the white stenciled number 7-12 on the front; black balaclava covering the whole face and neck; dark tinted goggles over the eyes, so no skin and no eyes are visible; black plate-carrier vest with plain black pouches; plain grey shoulder patches with no insignia; black long-sleeve combat shirt; black cargo trousers; black knee pads; black tactical boots; black fingerless tactical gloves with wide velcro wrist straps on both hands. He stands perfectly still. No weapon, no rifle, no holster. No badges, no police insignia, no red anywhere, no text anywhere except the helmet number 7-12. No footer bar, no border. [SHEET-END]
```

"明确"体现在这几处，以后写设定图都照这个标准：

| 容易含糊的地方 | 明确写法 |
|---|---|
| 景别 | 写清从哪到哪：`full body from the top of the helmet to the soles of the boots` |
| 朝向 | 不写 left / right profile（模型常弄反），写"朝画面右边"，并说明哪一侧对着镜头 |
| 姿势 | 每格都写：站直、双手自然下垂、手里没东西 |
| 装备 | 逐件列出：头盔、面罩、护目镜、背心、口袋、臂章、上衣、裤子、护膝、靴子、手套 |
| 手套 | 写死成和沃德的手 v2 一样：半指、宽魔术贴腕带、手背破洞 |
| 文字 | 只允许头盔上的 7-12，其余一律禁止 |
| 红色 | 写明 `no red anywhere`（红色只属于证物） |
| 版式瑕疵 | 加 `No footer bar, no border`（反推时有一个模型在手部图底部看到了灰条） |

- 头盔编号如果生成乱码，就去掉 `with the white stenciled number 7-12 on the front`，生成空白头盔，后期贴上 7-12。
- 第十三人不拿武器，和"他从不举枪"一致。

### 已锁定的细节（以通过的 v2 为准）

这些细节来自对已通过设定图的图片转提示词反推（两个视觉模型交叉核对，见 [学习记录](../prompts/reference-sheet-reverse-prompts.md)）。之后的镜头提示词要和它们一致：

| 项目 | 锁定的样子 | 用在 |
|---|---|---|
| 背景 | 平整无缝的哑光中灰（约 130–140 / 255），无渐变、无投影 | 所有设定图 |
| 分隔线 | 白色细线，约为画面宽度的 1% | 所有设定图 |
| 烧伤疤 | 不规则长条，隆起、发亮，粉白色；沿手背纵向，从手腕一侧伸向中指，约占手背长度的 1/3 | I3、C2、第十三人 |
| 手套 | 黑色哑光**半指**战术手套，宽魔术贴腕带；手背中央一个椭圆形破洞，露出疤 | C2、第十三人 |
| 手表 | 银色金属链表带，白 / 银色表盘 | I3 |
| 袖口 | 炭灰色西装袖口 | I3 |

WARD-GLOVE（手套块，用在 C2 等镜头）：

```text
a black matte fingerless tactical glove with a wide velcro wrist strap, an oval hole torn open across the back of the hand revealing a raised, shiny, pinkish-white burn scar
```

### 在 AKOOL 里重做时

- 诺拉：文生图。正向提示词按上面拼好，NEG-SHEET 填进 `negative_prompt`。
- 手部图和第十三人：AKOOL 只能接**一张**源图（`source_image`），所以用诺拉母版做源图，`similar` 先设 **0.3** 左右试。数值太高会把诺拉的脸和衣服带进来，太低又会丢掉风格。这个数值是起点，要先小规模测试。
- 三张都用同一个分辨率和画幅，例如 1080p、16:9。
- ⚠️ 2026-11-06 实测：AKOOL 接口对当前账号返回 `1213 Only subscribed users can use the API functions`，连查询模型都不行。**账号订阅前，AKOOL 这一步做不了**，所以三张设定图都先在 LibTV 生成。AKOOL 的参与放在关键帧、图生视频、口型和配音上，分工见 [AKOOL 制作流程](../production/akool-workflow.md)。（同日更新：账号已订阅，图像生成接口可用。）

## 已生成的参考图（LibTV）

LibTV 项目"EXHIBIT 47 第47号证物"。模型：General image Pro（`nebula-ultra`），2K，16:9，每次 1 张。

| 参考图 | 状态 | 节点 |
|---|---|---|
| 诺拉四视图 v1 | **废弃**：和手部图风格不统一（原因见上表） | `i-kKd0eUq6g4` |
| 沃德右手 v1 | **废弃**：微距产品照风格，缺袖口和钢表 | `i-AEP7votex7` |
| 诺拉四视图 v2（风格母版） | **已通过**。⚠️ 两个视觉模型都判断它只有 1 格正面胸像，不是四视图；如果确实只有一格，建议补一张四视图（侧脸和下巴特写对镜头 I2、I4 有用） | `i-3tleSMYSCV` |
| 沃德右手 v2 | **已通过**。⚠️ 有一个模型说第 1 格是左手，请再确认 | `i-ogNrWvlqro` |
| 第十三人 v2 | 以沃德的手 v2 为参考图生成。头盔编号出错（01 / 1-12）、有底部条、臂章是黑色，**不用** | `i-5bwnmb06HT` |
| 第十三人 v2.1（空白头盔） | 在 v2 上局部修改：无文字、臂章浅灰。底部条还在；一个模型说有枪套。**待人工验收** | `i-OM9iRyuQJu` |

v2 的提示词就是本页的固定块拼起来的结果，节点里能看到完整原文。

**验收标准**（不合格就重新生成，不要将就）：

- **风格一致**（先查这一项）：把诺拉 v2 和手部 v2 并排放，检查背景灰度、光的方向和软硬、色温、清晰度，以及 4 格的宽度和分隔线。有任何一项不同，就只重做手部图，**母版不动**。
- 诺拉：四格是**同一个人**；第 4 格能看清下巴上的伤疤；短发；没有文字或标志。
- 沃德的手：四格里**烧伤疤的形状和位置一致**；第 1 格有西装袖口和钢表；第 4 格的手套从手背撕开、露出疤；手指数量正常。
- 第十三人：4 格；完全不露脸和眼睛；手里、身上没有武器；头盔空白（7-12 后期贴）；臂章浅灰、无图案；第 4 格的手套和疤与沃德的手 v2 第 4 格一致；背景、光线、分隔线和另两张一致。

注意：这些图是在 LibTV 生成的。比赛要求 AKOOL 在制作中起"有意义的作用"，所以后面的镜头生成要放在 AKOOL 里做，或者按上面的方法在 AKOOL 里重做设定图，并保留制作记录。

## v3 设定图：中文提示词 + 真人实拍标准（2026-11-07，取代 v2）

用户的要求：**人物和手在 LibTV 里用中文提示词生成**，这样更真实；整体按"真人演员实拍的电影画面"标准（全文见 [镜头提示词库](../prompts/exhibit-47-shot-prompts.md) 的"整体视觉标准"）。另外指出 v2 的手**比例不对，中间三根手指不够长**。

- 模型：**Seedream 5.5**（`doubao-seedream-5-5`，和即梦同一系列，中文理解好、人像自然），2K，16:9，每次 1 张。
- 写法：人物描述照用户给的中文范例写（年龄、国籍、发型、眼睛、肤色、疤、服装、表情，再加"真人摄影，未经磨皮，自然皮肤纹理，柔和侧光，灰色背景，角色三视图"），后面接两段固定中文块：

**LIVE-CN**（真人实拍标准，每张设定图都加）
```text
整体视觉标准：真人演员实拍的电影画面，人物是现实中真实存在的普通演员。真实人体比例，自然的面部不对称，符合年龄的皮肤纹理，保留适量毛孔、细小绒毛、轻微肤色差异和自然眼下阴影；眼睛湿润但不过度明亮；头发有真实发根、碎发和自然成束关系。皮肤不能像蜡、塑料或经过磨皮的美容照片，也不要为了表现真实而过度增加皱纹、毛孔和污渍。衣服具有真实的织物纹理、厚度、重量和受力褶皱，脚底与地面有自然接触阴影。
光线与摄影：画面左侧柔和侧光，纯灰色无缝背景，各格的光线方向和色温一致，保留柔和的明暗、自然反射光和暗部细节；真实镜头拍摄的透视，主体清晰；自然曝光，克制的调色，保留肤色层次与高光过渡。
```

**EXCL-CN**（排除）
```text
排除：插画、动漫、游戏立绘、游戏过场动画、三维角色渲染、数字人展示、塑料皮肤、蜡像感、美颜磨皮、商业美容精修、夸张轮廓光、过度HDR、过度锐化；画面中不要出现任何文字、标注、编号和水印。
```

**手的比例（v3 起写死）**
```text
手指修长、比例正常：中指最长，长度约为手掌长度的八成；食指和无名指稍短、长度接近；小指最短，指尖约到无名指最末一个指节；拇指从手掌下半部伸出。每一格都是正常的五根手指。
```
手部图要**从正上方俯拍、五指伸直**，侧角度会把手指拍短，看不出比例。

### 各张的人物描述（接在"角色三视图，真人摄影。……"之后）

| 设定图 | 人物描述（中文） |
|---|---|
| 诺拉 面部三视图（**身份母版**） | 26岁欧洲女性，深棕色短发，两侧铲青，灰色眼睛，浅肤色，脸颊轻微冻红，下巴一道细淡的旧疤（已愈合多年的浅白色细线，正面和侧面都能看清），素颜，灰色宽松卫衣，冷静表情。正面、四分之三侧面、正侧面头肩特写，85毫米镜头，眼睛清晰对焦 |
| 诺拉 全身三视图 | 以面部三视图为参考图："人物必须和参考图完全是同一个人"；服装加深灰色工装裤、黑色短靴，身高约170厘米，身材匀称偏瘦 |
| 布兰特 全身三视图 | 45岁欧洲男性，特勤组组长，身材结实，浓密深色胡茬，眼睛布满血丝、神情疲惫紧绷，短发略带灰白；黑色哑光防弹头盔（无任何文字、数字和标志）；黑色头套拉到下巴下面露出整张脸；黑色战术背心（口袋素面）、素面灰色臂章、黑色作战服、护膝、作战靴、战术手套；不持武器，没有枪套 |
| 第十三人 全身三视图 | 身形高大的特勤队员，全身黑色战术装备；黑色哑光头盔完全空白；黑色头套完全遮住脸和脖子，深色护目镜，看不到任何皮肤和眼睛；胸前左侧一台小型黑色执法记录仪亮着一颗很小的红色录制灯；素面浅灰臂章；双手黑色半指战术手套，右手手套手背撕开椭圆形破洞露出陈旧的粉白色烧伤疤；不持任何武器，没有枪套 |
| 沃德 右手 四格 | 54岁欧洲男性的右手，皮肤偏白略粗糙，手背有青筋、细汗毛、轻微色斑；手背一道陈旧烧伤疤，从手腕一侧沿中指掌骨方向延伸到手背中部，约占手背长度三分之一，微微隆起、发亮、粉白色，边缘有细小褶皱。第1格俯拍平放在灰色金属桌面、炭灰色西装袖口、银色钢带手表；第2格俯拍疤特写；第3格捏着廉价黑色圆珠笔；第4格戴黑色半指战术手套，手背破洞露出同一道疤 + 上面的"手的比例"块 |

### 生成记录

| 设定图 | 节点 | 结果 |
|---|---|---|
| 诺拉 全身三视图 v3 | `i-hyub3RW93j` | 很真实，但脸和面部三视图不是同一个人 → 用 v3.1 |
| 诺拉 面部三视图 v3 | `i-MD7YKluRZe` | ✅ **身份母版**：毛孔、轻微冻红、灰色眼睛、下巴淡疤都在 |
| 诺拉 全身三视图 v3.1 | `i-njSJDbbUQp` | ✅ 以面部三视图为参考，和母版是同一个人 |
| 布兰特 全身三视图 v3 | `i-p1NfLIjZ1z` | ✅ 头套拉下、露脸，无文字和标志 |
| 第十三人 全身三视图 v3 | `i-VY7LiNcMQJ` | 右前臂袖子破口像新伤、大腿有枪套 → 改 v3.1 |
| 第十三人 全身三视图 v3.1 | `i-wJRp6J96fF` | ✅ 在 v3 上局部修改：袖子完好、去掉枪套 |
| 沃德 右手 v3 | `i-in09FOHpdA` | 出了 5 格；第 1 格的疤和第 2 格不一致；侧角度看不出手指长度 → 重做 |
| 沃德 右手 v3.1 | `i-qnl6CDgiNc` | 4 格；第 2 格俯拍、五指伸直，比例正常（中指最长）；第 1 格仍是旧的侧角度 → 只改第 1 格 |
| 沃德 右手 v3.2 | `i-5gXgTj8gA5` | 第 1 格改成俯拍 + 袖口 + 手表 ✅；但第 1 格的疤仍是手腕附近一条短横线 → 只改疤 |
| 沃德 右手 v3.3 | `i-oNdWbdYl6b` | ✅ **手部母版**：4 格，第 1、2、4 格俯拍、五指伸直，中指最长、比例正常；第 1 格的疤改成和第 2 格一样的斜向长条疤 |

文件：`previs/character_refs_v3/`（1920 宽的副本，原图在 LibTV 节点里）。

**v3 的用法**：做关键帧时，诺拉的近景以面部三视图为参考图，全景以全身三视图为参考；第十三人、布兰特各用自己的三视图；I3、C2 的手都以沃德右手 v3.3 为参考（疤的细节以第 2 格为准），保证两处是同一道疤、同样的手指比例。

## 相关笔记

- [完整故事](exhibit-47-story.md)：人物背后的故事和秘密。
- [镜头提示词库](../prompts/exhibit-47-shot-prompts.md)：所有镜头都引用本页代号。
- [分镜表](../production/exhibit-47-shot-list.md)：第十三人的 4 次出场位置。
- [《明日不来》角色圣经](character-bible.md)：同样的方法，备选方案版本。
- [风格锚](../prompts/style-anchor.md)、[提示词公式](../prompts/prompt-formula.md)：提示词结构。
- [AKOOL 制作流程](../production/akool-workflow.md)：设定图到图生视频的步骤。
- [长腿](../trailers/longlegs-teasers.md)：反派不露脸的参考。
