---
id: 20261106-exhibit-47-shot-prompts
title: 《第 47 号证物》镜头提示词库（按证物画面类型分组）
tags: [prompt, visual, sound, action]
created: 2026-11-06
updated: 2026-11-06
related: [20261106-exhibit-47-character-bible, 20261106-reference-sheet-reverse-prompts, 20261106-exhibit-47-scene-images, 20261106-exhibit-47-whitebox-previs, 20261106-exhibit-47-shot-list, 20261106-exhibit-47-story, 20261106-prompt-formula, 20261106-style-anchor, 20261106-music-sfx-prompts, 20261106-sound-design, 20261106-black-screen-text-cards, 20261106-cloverfield-teaser, 20261106-civil-war]
summary: 主方案预告的全部提示词：六种"证物画面"风格块（执法记录仪 / 监控 / 无人机 / 审讯室 / 旧录像 / 第 47 号证物视角）、23 个编号镜头、监控墙素材池、后期叠字规范，以及配乐、音效和配音提示词。
---

# 《第 47 号证物》镜头提示词库（按证物画面类型分组）

> Summary: 主方案预告的全部提示词：六种"证物画面"风格块（执法记录仪 / 监控 / 无人机 / 审讯室 / 旧录像 / 第 47 号证物视角）、23 个编号镜头、监控墙素材池、后期叠字规范，以及配乐、音效和配音提示词。

## 背景

结尾字卡写着"本片所有画面均为证物"，所以**预告里的每个镜头都必须是"被记录下来的"画面**：执法记录仪、监控、无人机、审讯室摄像头、取证录像。这个形式借鉴了 [科洛弗档案](../trailers/cloverfield-teaser.md) 的伪纪录手法，好处是低清、晃动的画面能掩盖 AI 的瑕疵。

- 占位符 `[NORA-REF]` `[WARD-HAND]` `[WARD-GLOVE]` `[THIRTEENTH-REF]` `[BRANDT-REF]` `[UNIT-REF]` `[OLD-HANDS]` 和 `LOC-*`：原文见 [人物与道具设定](../concept/exhibit-47-character-bible.md)。手和手套的细节以已通过的设定图为准，见那里的"已锁定的细节"。
- 提示词结构沿用 [提示词公式](prompt-formula.md)；风格锚换成下面的证物风格块，**不再使用 STYLE-A**。
- **做关键帧时的参考图**：[场景图](exhibit-47-scene-images.md)（空间）+ 设定图（人）+ [白模](../production/exhibit-47-whitebox-previs.md)里同一时间点的画面（构图和遮挡）。D1、C3、B8、C2、O1、I2、I4、E1 的提示词已按白模的发现改过，原因见白模笔记的"发现"一节。
- 所有屏幕文字（时间戳、编号、SIGNAL LOST、证物标签）**一律后期叠加**，见本页"后期叠字规范"。
- **设定图和镜头各用一套风格，不能混**。设定图统一用 SHEET-STYLE（灰色影棚、柔光、无调色，见 [人物与道具设定](../concept/exhibit-47-character-bible.md)），只负责"人长什么样"。镜头用下面的 S-* 块，负责"画面是什么风格"。所以镜头提示词里不要写 studio、grey backdrop 这类设定图的词；设定图里也不要写 S-* 块里的词。
- **台词建议后期配**：用 AKOOL 配音生成，再叠到画面上。只有 I2 需要口型同步。

## 风格块（每条提示词开头粘贴一个）

**S-BCAM 执法记录仪**
```text
Police body-worn camera footage, chest-mounted wide-angle fisheye lens, compressed 1080p video with digital noise and motion blur, auto-exposure pumping, infrared night mode in darkness rendering everything in monochrome grey-green, handheld walking shake, breath vapor and frost in the air, harsh cold flashlight beams, completely realistic, no on-screen text.
```

**S-CCTV 监控**
```text
Fixed high-angle security camera footage, wide-angle lens with slight barrel distortion, low frame rate, monochrome infrared, heavy compression noise, static camera, completely realistic, no on-screen text.
```

**S-DRONE 无人机**
```text
Aerial drone footage, straight top-down view, flat grey overcast dawn light, snow-covered ground, light digital noise, slow steady hover, completely realistic, no on-screen text.
```

**S-ROOM 审讯室 / 取证录像**
```text
Photorealistic footage from a police interview-room camera system, locked-off camera, clean digital image, cold flat fluorescent overhead light, muted grey-blue palette, slight wide-angle, deep shadows at the edges of the frame, grounded realism, restrained, no on-screen text.
```

**S-OLD 三年前的旧录像**
```text
Older-generation body camera footage recorded years earlier, low 720p resolution, warmer yellowish color cast, heavy compression blocks, brief digital glitches and dropped frames, handheld, completely realistic, no on-screen text.
```

**S-X47 第 47 号证物视角**：用 S-BCAM，但把 `handheld walking shake` 换成 `unnaturally smooth and steady movement, the wearer walks calmly`。所有人的画面都在晃，只有他的稳得可怕。

**NEG-47（负面词）**
```text
cartoon, anime, CGI look, video game graphics, cinematic color grading, clean movie look, on-screen text, subtitles, watermark, logo, real police insignia, readable badges, distorted hands, extra fingers, warped face, face morphing, gore, blood spray, visible wounds
```

暴力保持**非血腥**：只拍枪口火光、烟雾、倒下的剪影，不拍伤口。这样也更不容易被平台限流或被模型拒绝。

---

## 无人机（D）

**D1 独自走出冷库**（全片第一个画面）· Veo / Kling · 6 秒
```text
[S-DRONE] LOC-GATE. Directly overhead, a single small figure — [NORA-REF], NORA-DAWN — walks slowly away from the open shutter of the cold-storage plant across a vast field of perfectly untouched snow with no tyre tracks, leaving one long line of footprints behind her. No other people, no vehicles. Sound: wind, the faint hum of drone rotors. 6 seconds. [NEG-47]
```

## 执法记录仪（B）

**B1 破门** · Kling · 5 秒
```text
[S-BCAM] LOC-GATE at night. The camera wearer rushes forward behind two officers ([UNIT-REF]) who ram open a frosted steel door; flashlight beams cut into a pitch-black interior; freezing fog rolls out over the threshold. Sound: a heavy metallic bang, boots, ragged breathing behind masks. 5 seconds. [NEG-47]
```

**B2 报数**（**第十三人出场 #1**）· Kling · 6 秒
```text
[S-BCAM] LOC-STAIR, infrared. The camera faces a line of officers ([UNIT-REF]) stacked down a narrow dark stairwell, each one tapping the shoulder in front. Then the camera swings around toward the back of the line: at the very end of the stack, half-lost in darkness, one more officer — [THIRTEENTH-REF] — stands perfectly still, facing the camera. Hold for one second. Sound: whispered voices counting off, breathing, a drip of water. 6 seconds. [NEG-47]
```
报数的人声后期另配，见"配音"。

**B3 冷冻走廊**（不能出现第十三人）· Kling / Seedance · 6 秒
```text
[S-BCAM] LOC-FREEZER. The camera pushes through hanging plastic strip curtains into a long freezer corridor; rows of empty meat hooks sway slightly; flashlight beams catch frost glittering on the steel walls; two officers ([UNIT-REF]) ahead sweep their rifles left and right. Sound: curtains rustling, a radio squelch, a distant metallic creak. 6 seconds. [NEG-47]
```

**B4 摘面罩** · Kling · 5 秒
```text
[S-BCAM] LOC-FREEZER, chaotic. Officers ([UNIT-REF]) shove each other in a tight circle, ripping their balaclavas down and shining flashlights directly into each other's faces, breath steaming; [BRANDT-REF] grabs the camera wearer by the vest and yanks the camera close to his face. Violent shaking, flashlight flare. Sound: shouting, overlapping voices. 5 seconds. [NEG-47]
```

**B5 黑暗中的枪口火光** · Kling · 4 秒
```text
[S-BCAM] Total darkness in LOC-FREEZER. The only light comes from rapid muzzle flashes ahead, freezing the corridor in strobing orange-white bursts: silhouettes of officers, swinging hooks, drifting fog, then black again. No blood. Sound: deafening gunshots muffled by the cold room, shell casings ringing on ice. 4 seconds. [NEG-47]
```

**B6 氨气管道爆裂** · Kling · 4 秒
```text
[S-BCAM] LOC-FREEZER. A bullet punctures a frost-covered refrigeration pipe on the ceiling (PIPE); a violent jet of white gas sprays down and floods the corridor in seconds; an officer ([UNIT-REF]) staggers backward into the fog, coughing. Sound: high-pressure hiss, a shrill alarm, coughing. 4 seconds. [NEG-47]
```

**B7 "我们埋了你"** · Veo · 5 秒
```text
[S-BCAM] LOC-FREEZER, flashlight from below. [BRANDT-REF], mask ripped down, eyes wide with terror, screams into the darkness past the camera, spit and breath vapor flying: "We buried you!" His rifle light shakes wildly. Sound: his hoarse scream, echo, distant alarm. 5 seconds. [NEG-47]
```

**B8 冷冻门镜面倒影**（**第十三人出场 #2**）· Veo · 4 秒
```text
[S-BCAM] LOC-FREEZER, along the row of freezer-room doors. The camera wearer walks past the door of room 4, a mirror-polished steel panel in a dark steel frame with a heavy handle, and turns his body toward it as he passes; the panel clearly reflects the hook rails and columns behind the camera, and in it we see the reflection of the wearer, with a small glowing red recording light on his chest at exactly the height of this camera — a tactical officer whose helmet bears the white stenciled number 7-12, full black balaclava and goggles, face invisible. The reflection turns its head slightly toward the camera. Sound: footsteps on ice, a slow breath. 4 seconds. [NEG-47]
```
注意：这台是第 47 号证物的视角，后期叠字用 7-12。

**B9 隔着门帘误伤** · Kling · 4 秒
```text
[S-BCAM] LOC-FREEZER, near darkness. Through a hanging plastic strip curtain, the blurred silhouette of a figure with a flashlight moves on the other side; the camera wearer's rifle fires twice through the curtain; the silhouette drops and its flashlight clatters to the floor, rolling and shining back at the camera — it is a rifle-mounted light, one of their own. No blood. Sound: two gunshots, plastic snapping, a flashlight rolling on ice. 4 seconds. [NEG-47]
```

**B10 闪光弹** · Kling · 3 秒
```text
[S-BCAM] LOC-FREEZER. A flashbang detonates a few meters ahead; the image blows out to pure white, the sensor struggles, the exposure slowly crawls back revealing silhouettes of officers staggering in the fog. Sound: a deafening bang collapsing into a high-pitched ringing. 3 seconds. [NEG-47]
```

## 第 47 号证物视角（X）

**X1 平静穿过毒雾**（不能出现他的手）· Kling · 5 秒
```text
[S-BCAM, with unnaturally smooth and steady movement, the wearer walks calmly] LOC-FREEZER filled with white gas fog. The camera glides steadily forward at walking pace while officers ([UNIT-REF]) panic around it — one falls coughing, one fires blindly into the fog, flashlights whip in every direction — and the camera never hurries, never turns, never raises a weapon. Sound: muffled chaos, alarm, and the camera wearer's slow, calm breathing very close. 5 seconds. [NEG-47]
```

## 监控（C）

**C1 俯拍互射** · Kling · 4 秒
```text
[S-CCTV] High corner of LOC-FREEZER. In near-total darkness, muzzle flashes erupt from several points across the hall at once, briefly revealing officers ([UNIT-REF]) firing at each other between the rows of hooks; fog swirls; one silhouette falls. Low frame rate, choppy. No blood. Sound: distant crackle of gunfire through the camera's thin microphone. 4 seconds. [NEG-47]
```

**C2 拉住诺拉的手**（**第十三人出场 #3**）· Veo · 5 秒
```text
[S-CCTV] LOC-ROOM4, infrared. [NORA-REF], NORA-TAC, stumbles into the small freezer room, half-blind in the gas fog, and crosses the open doorway; out of the narrow gap between a tall stack of frosted crates and a pallet stack, a gloved right hand — [WARD-GLOVE] — reaches out sideways and grabs her vest, the back of the hand and its scar turned up toward the camera, and holds her for a moment; at that instant gunfire from the hall sparks off the steel door frame exactly where she was standing; then the hand pulls her down into cover behind the crates. No struggle, no choking: it could be an attack or a rescue. The figure attached to the hand stays in shadow. Sound: a whisper very close to her: "You're safe now, Kade." 5 seconds. [NEG-47]
```

**C3 警车抵达**（报警电话的画面）· Kling · 5 秒
```text
[S-CCTV] LOC-GATE at night, a camera mounted high on the facade beside the loading bay, looking across the empty snow yard to the gate about 20 meters away. Snow falls through the beam of a single dead floodlight; two dark unmarked police vans pull up at the rusted gate and stop; doors open and a stack of officers ([UNIT-REF]) climbs out silently. Low frame rate, grainy. Sound: tires on snow, the hum of the camera, faint radio chatter. 5 seconds. [NEG-47]
```

## 旧录像（O）

**O1 举起的双手**（闪帧和蒙太奇用）· Veo · 4 秒
```text
[S-OLD] LOC-FREEZER three years earlier, flashlight beam. [OLD-HANDS]. The older camera has a narrower view and is tilted up at the raised hands from about one meter away, so only the hands and sleeves are in frame; the face stays below the frame edge, in darkness. The hands tremble. The camera is steady on them. Then the image glitches. Sound: muffled shouting, a calm male voice off-camera says: "No. Mine stays on." 4 seconds. [NEG-47]
```

**O2 关掉的摄像机**（三年前）· Kling / Veo · 5 秒
```text
[S-OLD] LOC-FREEZER three years earlier, flashlight light. The camera faces a line of officers ([UNIT-REF]) standing with their backs half-turned; one after another, each reaches up to the small body camera on his own chest and switches it off — each tiny red recording light goes dark. The camera recording all this stays on. Sound: a series of small clicks, heavy breathing, a calm male voice off-camera: "No. Mine stays on." 5 seconds. [NEG-47]
```

## 审讯室（I）

**I1 诺拉在听**（沃德不入画）· Veo · 5 秒
```text
[S-ROOM] LOC-INTERVIEW, wide locked-off camera from a high corner. [NORA-REF], NORA-ROOM, sits alone on one side of the grey table, perfectly still, staring at the empty chair across from her; the edge of the frame where the investigator sits is cut off. Sound: fluorescent buzz, a man's calm voice off-screen: "Your unit had twelve officers, Kade." 5 seconds. [NEG-47]
```

**I2 "我们进去的时候，是十三个人"**（口型同步）· Veo · 5 秒
```text
[S-ROOM] LOC-INTERVIEW, close camera framing on her head and shoulders, 50mm equivalent; the dark one-way mirror behind her reflects only darkness. [NORA-REF], NORA-ROOM, looks straight past the lens, exhausted but certain, and says quietly: "There were thirteen of us." Sound: her voice, fluorescent buzz. 5 seconds. [NEG-47]
```

**I3 沃德的手**（**第十三人出场 #4**，按钮）· Veo · 5 秒
```text
[S-ROOM] LOC-INTERVIEW, close camera on the table surface. [WARD-HAND] slowly turns a cheap black ballpoint pen (PEN) end over end; the back of the hand faces the lens the whole time, and the burn scar, the same as the one on the gloved hand in the freezer, catches the fluorescent light. The man's face is never in frame. Sound: a calm, kind male voice says: "You're safe now, Kade." 5 seconds. [NEG-47]
```

**I4 诺拉抬眼**（先看手，再看脸，停住）· Veo · 5 秒
```text
[S-ROOM] LOC-INTERVIEW, close camera on her face; the dark one-way mirror behind her reflects only darkness. [NORA-REF], NORA-ROOM, is looking down at the man's hand on the table; she stares at it for a long moment, then slowly her eyes rise to his face, and she holds his look as her expression shifts from exhaustion to cold recognition. She does not speak. Sound: silence, a faint fluorescent buzz. 4 seconds. [NEG-47]
```

## 取证录像（E）

**E1 13 台记录仪** · Veo · 6 秒
```text
[S-ROOM] LOC-EVIDENCE, forensic documentation camera, slow push-in along the table from its far end towards the nearest bag. BAGS: twelve body cameras in a neat row with white tags, and at the near end a thirteenth, frost still melting on it, with a faded red tag. The push-in stops on the thirteenth. Sound: LED hum, a single electronic beep. 6 seconds. [NEG-47]
```

**E2 证物标签特写**（片名卡底图）· 任意 · 5 秒
```text
[S-ROOM] LOC-EVIDENCE, extreme macro close-up, harsh white LED light. EX47: frost melting on the scuffed black body camera, its small red recording light glowing steadily, the faded red cardboard evidence tag tied with white string fills the right side of frame, blank where text will be added. Shallow depth of field, black background. Sound: one soft electronic beep. 5 seconds. [NEG-47]
```

---

## 监控墙素材池（P）

监控墙（GRID）是 **4×3 共 12 格的多画面导出**，在剪辑软件里拼，不让 AI 生成。需要 6 段短素材，镜像、错时后填满 12 格，每格叠上编号 7-01 至 7-12。

| 代号 | 内容 |
|---|---|
| P1 | `[S-BCAM] walking down a dark freezer corridor, flashlight sweeping hooks` |
| P2 | `[S-BCAM] descending concrete stairs in infrared, an officer's back in front` |
| P3 | `[S-BCAM] pushing through plastic strip curtains` |
| P4 | `[S-BCAM] scanning a room of frosted crates, rifle light` |
| P5 | `[S-BCAM] standing still, officers' helmets in front, breath vapor` |
| P6 | `[S-BCAM] turning quickly toward a noise, motion blur` |

每段 5 秒，结尾加 `[NEG-47]`。B3、P1 至 P6 都**不能**出现第十三人。

## 后期叠字规范（全部在剪辑软件里做）

| 画面 | 叠字 | 位置 |
|---|---|---|
| 执法记录仪 | `BODY CAM 7-04` + `FEB 09  04:03:12` + 红色 `● REC` | 左上 / 右下 / 右上 |
| 第 47 号证物 | 与诺拉相同的 `BODY CAM 7-12`（**两台都写 7-12**） | 同上 |
| 监控墙第 13 格 | `UNKNOWN` + 红点（不写 7-12，避免被看成第 12 路重新连上） | 格子左上 |
| 证物登记表（字卡 18） | `47  BODY CAMERA · UNIT 7-12` + 红框 `LOST` | 文件卡 |
| 监控 | `CAM FRZ-03` + 时间戳 | 左上 |
| 无人机 | `DRONE 02` + `ALT 38M` + `FEB 09  07:40:16` | 底部 |
| 审讯室 | `INTERVIEW RM 3 · REC` + `FEB 10  09:14:55` | 左上 |
| 旧录像 | 旧款字体的 `UNIT 7-12` + 另一个日期，带花屏 | 左上 |
| 信号中断 | 黑格 + 白色小字 `SIGNAL LOST` | 格子中央 |
| 证物标签 | `EXHIBIT 47`（片名卡） | 标签上 |

- 字体：等宽字体，例如 Google Fonts 的 **Share Tech Mono** 或 **IBM Plex Mono**（OFL 许可，可商用）。
- **不要模仿任何真实执法记录仪品牌的界面。**
- 时间戳只写月日，不写年份。

---

## 声音提示词

### 配乐

**SC1 底层脉动**（全片）
```text
Cinematic thriller underscore built from an industrial freezer compressor hum: a slow sub-bass pulse at 50 BPM, low bowed double bass, faint radio static woven into the rhythm, distant metallic creaks; no melody; cold, oppressive, restrained. 75 seconds, instrumental.
```

**SC2 高潮升调**（第三幕蒙太奇）
```text
A 6-second cinematic riser: accelerating taiko and metallic percussion, distorted radio static and a rising string cluster, building to a peak and stopping dead on a hard cut to silence. Instrumental.
```

### 音效清单

| 代号 | 音效 | 提示词 / 做法 |
|---|---|---|
| FX1 | 录制提示音 | `a single short electronic body-camera beep` |
| FX2 | 信号中断 | `a digital signal drop-out tone followed by a soft burst of static` |
| FX3 | 无线电 | `police radio squelch and short static burst` |
| FX4 | 冷库压缩机 | `low steady industrial freezer compressor hum` |
| FX5 | 塑料门帘 | `heavy plastic strip curtains brushing past` |
| FX6 | 破门 | `heavy steel door forced open, metallic bang, echo` |
| FX7 | 冷库里的枪声 | `gunshots muffled and echoing in a cold concrete hall, shell casings ringing on ice` |
| FX8 | 氨气 | `high-pressure gas hiss with a shrill industrial alarm` |
| FX9 | 冰面脚步 | `boots on ice and frost, slow` |
| FX10 | 面罩呼吸 | `close breathing through a balaclava in freezing air` |
| FX11 | 转笔 | `a ballpoint pen tapping and turning on a metal table` |
| FX12 | 冲击重音 / BRAAAM | `deep cinematic impact with sub-bass` / `low brass BRAAAM, long tail` |

### 配音（AKOOL 配音工具）

| 代号 | 角色 | 台词 | 声音设定 |
|---|---|---|---|
| V1 | 诺拉 | "There were thirteen of us." | `young woman, low, quiet, exhausted but certain, no tremble` |
| V2 | 沃德 | "Your unit had twelve officers, Kade." | `calm, kind man in his fifties, soft-spoken, patient, warm` |
| V3 | 沃德（耳语） | "You're safe now, Kade." | **与 V2 同一个声音**，贴近麦克风的耳语 |
| V4 | 沃德 | "You're safe now, Kade." | **与 V2 同一个声音**，正常音量，审讯室混响 |
| V5 | 布兰特 | "Count off." / "Who said that?" / "Masks off! Now!" / "We buried you!" | `hoarse man in his forties, commanding, then terrified` |
| V6 | 报数组员 | "…Ten." "Eleven." | 3–4 个男声轮换 |
| V7 | 诺拉 | "Twelve." | 与 V1 同一个声音，压低 |
| V8 | 第十三人 | "Twelve." | **与 V2 同一个声音**，压低、平静 |
| V9 | 雷耶斯（旧录音） | "Seven-Twelve. Still recording." | `calm young man`；后期加电话带通滤波、失真、断续 |
| V10 | 雷耶斯（旧录像） | "No. Mine stays on." | 与 V9 同一个声音，较清晰 |
| V11 | 报警人 | "Northgate. Same as last time." / "Seven-Twelve." | **与 V2 同一个声音**，压低，后期加电话带通滤波 |
| V12 | 报警中心接线员 | "911, what's your emergency?" / "Sir, who is this?" | `professional female dispatcher, calm, slightly tired`；电话音质 |

**关键**：V2、V3、V4、V8、V11 必须用同一个声音模型生成。这是给仔细的观众留的听觉线索。

## 相关笔记

- [人物与道具设定](../concept/exhibit-47-character-bible.md)：所有占位符的原文。
- [设定图的图片转提示词学习记录](reference-sheet-reverse-prompts.md)：手套和疤的细节是怎么锁定的。
- [分镜表](../production/exhibit-47-shot-list.md)：每个编号用在哪一秒。
- [完整故事](../concept/exhibit-47-story.md)：画面背后的真相。
- [提示词公式](prompt-formula.md)、[风格锚](style-anchor.md)：通用规则。
- [音乐与音效提示词](music-sfx-prompts.md)、[声音设计](../techniques/sound-design.md)：声音方法。
- [黑屏与字卡](../techniques/black-screen-text-cards.md)：字卡排版。
- 参考拆解：[科洛弗档案](../trailers/cloverfield-teaser.md)（伪纪录）、[内战](../trailers/civil-war.md)（枪声与静默）。
