---
name: short-drama-visual-pipeline
description: 面向 AI 短剧承制团队的生产力工具。将文学剧本自动拆解为结构化分镜脚本，生成高精度文生图 prompt（含镜头语言、光影参数），并通过全局角色特征库确保跨场次角色视觉一致性。当用户提到"短剧分镜"、"剧本拆解"、"分镜脚本"、"视觉脚本"、"AI短剧"、"剧本转prompt"、"故事板生成"、"分镜设计"、"分镜图"、"画面设计"、"AI出图"、"视觉开发"等意图时使用此技能。
---

# 短剧视觉流水线

将文学剧本转化为可直接用于 AI 图像生成的结构化分镜脚本，输出高精度文生图 prompt，确保跨场次角色视觉一致性。

## 工作流程

### Step 1: 剧本接收与预处理

接收用户上传的剧本文本（直接粘贴或上传文件）。如剧本过长（超过 5000 字），先展示场次拆分方案让用户确认后再逐段处理。

### Step 2: 全局视觉风格确认

**在开始分析前**，先与用户确认全局视觉风格：

展示 6 种预设风格供选择：
- **电影写实** — cinematic, photorealistic, film grain, 8K
- **国风工笔** — Chinese ink painting, gongbi style, elegant color palette
- **赛博朋克** — cyberpunk, neon-lit, rain-slicked streets, futuristic
- **日系动漫** — anime style, cel shading, vibrant colors, studio ghibli quality
- **暗黑哥特** — dark gothic, moody atmosphere, high contrast, dramatic shadows
- **清新治愈** — soft pastel, warm sunlight, gentle atmosphere, watercolor texture

用户选择后，记录对应的风格参数，后续所有 prompt 统一追加。用户也可自定义风格关键词。

如用户不想选择，默认使用「电影写实」。

### Step 3: 剧本结构化分析

对每个场次提取结构化数据。采用少样本提示（Few-Shot Prompting）策略，确保输出格式一致。

**场次 JSON 结构：**

```json
{
  "scene_id": "场次_03",
  "scene_number": 3,
  "environment": "室内 / 废弃中式高层宫阙 / 薄雾笼罩 / 穹顶破败",
  "time_of_day": "白天",
  "weather": "无（室内薄雾）",
  "characters": [
    {
      "name": "李骁",
      "emotion": "警惕",
      "action": "手持长剑缓步前行",
      "dialogue": ""
    }
  ],
  "lighting": "体积感极强的丁达尔效应，阳光从破败穹顶倾泻，光柱穿透薄雾",
  "key_objects": ["古老铜镜碎片", "断裂石柱"],
  "mood": "压抑、紧张、悬疑",
  "camera_hint": "中景低角度，突出人物与环境的空间压迫感"
}
```

**分析规则：**
- 环境描述必须具体可视化：禁止"一个房间"，必须"一间堆满古籍的中式书房，木桌上摊开着泛黄的卷轴"
- 光线描述必须可执行：禁止"氛围感强"，必须"暖色侧光从窗户45度角打入，形成明显的明暗分割"
- 情绪必须转化为视觉元素：如"紧张"→"低角度镜头、浅景深、暗色调"
- 无明显场次标记时，按场景/角色/时间变化自动拆分，标注 [自动拆分]

### Step 4: 角色特征库建立

每个角色首次出场时，建立视觉特征档案。这是保证跨场次一致性的核心。

**角色档案结构：**

```json
{
  "character_id": "char_001_李骁",
  "name": "李骁",
  "gender": "男",
  "age_range": "25-30",
  "face_features": "棱角分明的下颌线，剑眉星目，鼻梁高挺，左眉尾一道淡疤",
  "body_type": "身高182cm，精瘦有力，宽肩窄腰",
  "hair": "黑色长发高束马尾，额前碎发",
  "default_outfit": "玄色暗纹劲装，腰间佩古铜长剑，腕缠黑色皮护腕",
  "distinguishing_features": "左眉尾淡疤，眼神锐利",
  "outfit_changes": [
    {"scene_id": "场次_05", "reason": "赴宴", "outfit": "月白色锦袍，腰系玉带"}
  ]
}
```

**一致性规则：**
- 建立角色后，后续所有场次中该角色的外貌描述必须完全复用档案内容
- 服装变化必须在 `outfit_changes` 中记录原因和新描述
- 为每个角色生成**三视图 prompt**（正面/侧面/背面），用于生成角色设定参考图，后续场景 prompt 中引用该角色时复用 seed_description

**角色三视图 Prompt 生成规则：**

每个角色生成 3 条独立的 prompt，用于产出角色设定三视图（Character Turnaround Sheet）：

1. **正面视图（Front View）**：
```
[角色 seed_description], front view, facing camera directly, full body from head to toe, standing in neutral T-pose or relaxed pose, arms slightly away from body, clean white background, character reference sheet, full body shot, even studio lighting, no shadows, photorealistic, 8K, masterpiece --ar 2:3 --s 200 --q 2
```

2. **侧面视图（Side View）**：
```
[角色 seed_description], side profile view, facing right, full body from head to toe, standing in neutral pose, clean white background, character reference sheet, full body shot, even studio lighting, no shadows, photorealistic, 8K, masterpiece --ar 2:3 --s 200 --q 2
```

3. **背面视图（Back View）**：
```
[角色 seed_description], back view, facing away from camera, full body from head to toe, showing back of outfit and hair details, clean white background, character reference sheet, full body shot, even studio lighting, no shadows, photorealistic, 8K, masterpiece --ar 2:3 --s 200 --q 2
```

4. **三视图总汇（Turnaround Sheet）** — 一张图同时展示正面/侧面/背面三个角度
```
character turnaround reference sheet of [角色 seed_description], three full-body views arranged horizontally side by side on clean white background, left: front view facing camera, center: side profile view facing right, right: back view facing away, all three views showing full body from head to toe in identical neutral pose with arms slightly away from body, even studio lighting with no shadows, consistent appearance across all three views, character design sheet, photorealistic, 8K, masterpiece --ar 16:9 --s 200 --q 2
```

**关键要求：**
- 纯白背景（white background），确保角色孤立无干扰
- 全身入画（full body from head to toe），头到脚完整可见
- 均匀打光（even studio lighting），避免阴影干扰角色细节
- 中性姿态（neutral pose），便于后续作为 --cref 参考图
- 三视图的 seed_description 必须完全一致，仅改变视角关键词
- 总汇 prompt 使用 `--ar 16:9` 宽幅画面容纳三个视角横向排列

### Step 5: 场景四视图 Prompt 生成

为每个场次的**场景环境**生成 4 条不同角度的场景设定图 prompt，用于建立完整的场景空间感。注意：场景四视图聚焦于环境本身，不含角色人物。角色表演分镜 prompt 在 Step 6 单独生成。

**场景四视图定义：**

每个场次生成 4 条场景 prompt，分别对应 4 个观察角度：

1. **正面全景（Front Wide Shot）** — 场景主视角，建立空间基调
```
[环境完整描述], [光线描述], front view, wide establishing shot, eye-level angle, showing the full space from the main entrance perspective, [风格参数], [画质参数] --ar 16:9 --s 250 --q 2
```

2. **侧面视角（Side Angle）** — 展示场景纵深和侧面空间关系
```
[环境完整描述], [光线描述], side angle view, 90-degree rotated perspective from the right side, showing depth and spatial layers, [风格参数], [画质参数] --ar 16:9 --s 250 --q 2
```

3. **俯瞰视角（Top-down / Bird's Eye View）** — 展示场景平面布局和空间结构
```
[环境完整描述], [光线描述], overhead bird's eye view, top-down angle looking straight down, showing floor plan layout and spatial structure, [风格参数], [画质参数] --ar 16:9 --s 250 --q 2
```

4. **反打视角（Reverse Angle）** — 从场景内部反方向看向入口/主视角方向，展示角色面对的视觉
```
[环境完整描述], [光线描述], reverse angle view, looking back toward the main entrance from the deepest point of the space, showing what characters face when entering, [风格参数], [画质参数] --ar 16:9 --s 250 --q 2
```

5. **四视图总汇（Scene 4-Angle Sheet）** — 一张图同时展示正面/侧面/俯瞰/反打四个角度
```
scene environment reference sheet of [环境完整描述], [光线描述], four views arranged in a 2x2 grid layout on a single image, top-left: front view wide establishing shot from entrance perspective, top-right: side angle view 90-degree rotated from right side, bottom-left: overhead bird's eye view looking straight down showing floor plan, bottom-right: reverse angle view looking back toward entrance from deepest point, all four views showing the same environment with identical objects and lighting but different camera angles, no people in any view, cinematic photorealistic 8K film grain, masterpiece best quality ultra-detailed --ar 16:9 --s 250 --q 2
```

**关键要求：**
- 场景四视图**不含人物**，纯粹展示环境空间
- 4 条独立 prompt 中的环境描述、光线、物件必须完全一致，仅改变观察角度关键词
- 关键道具和物件在 4 个角度中保持位置关系一致（空间连续性）
- 如场景有明确入口方向，正面全景从入口方向取景
- 总汇 prompt 使用 2x2 网格布局（左上/右上/左下/右下），`--ar 16:9` 宽幅画面

### Step 6: 角色表演分镜 Prompt

在场景四视图基础上，为每个场次的关键表演时刻生成带角色的构图 prompt。

**Prompt 结构（严格按此顺序）：**

```
[角色 seed_description], [动作/姿态], [场景环境简述], [光线描述], [镜头参数], [风格参数], [画质参数]
```

**镜头语言自动映射表：**

| 情绪/场景类型 | 自动追加镜头参数 |
|---|---|
| 紧张/对峙/压迫 | medium close-up, low angle, dramatic lighting, shallow DOF |
| 回忆/闪回/梦境 | soft focus, warm color grading, vignette, slight overexposure |
| 宏大/史诗/战斗 | wide shot or aerial view, epic scale, deep DOF |
| 私密/对话/情感 | over-the-shoulder or two-shot, shallow DOF, intimate framing |
| 动作/追逐/打斗 | dynamic angle, motion blur, high shutter speed, Dutch angle |
| 孤独/沉思/远望 | wide shot, negative space, silhouette, rim lighting |
| 恐怖/悬疑/诡异 | high contrast, deep shadows, dutch angle, desaturated tones |

**Midjourney 默认参数：**
- 场景/全景：`--ar 16:9`
- 人物特写：`--ar 2:3`
- 风格化强度：`--s 250`
- 质量：`--q 2`

**Negative Prompt（统一追加）：**
```
blurry, deformed, ugly, low quality, watermark, extra limbs, bad anatomy, modern elements, text, logo, signature, cropped, out of frame, duplicate
```

### Step 7: 输出交付

最终输出以下五个部分，保存为 Markdown 文件交付：

**Part 1 — 分镜脚本总表**

| 场次 | 环境 | 出场角色 | 情绪 | 镜头建议 |
|------|------|----------|------|----------|
| 场次_01 | ... | 李骁、苏瑶 | 紧张 | 中景低角度 |

**Part 2 — 角色特征库 + 三视图 Prompt**

每个角色输出：
- 完整视觉特征档案（JSON 格式）
- seed_description（英文，供场景 prompt 引用）
- **三视图 Prompt**：正面/侧面/背面各 1 条（共 3 条独立 prompt）+ **三视图总汇** 1 条（一张图出三个角度，共 4 条）

**Part 3 — 场景四视图 Prompt 清单**

每个场次输出 4 条纯场景独立 prompt（正面全景/侧面/俯瞰/反打）+ **四视图总汇** 1 条（一张图 2x2 网格出四个角度，共 5 条），不含人物

**Part 4 — 角色表演分镜 Prompt**

每个场次的关键表演时刻 prompt（含角色 + 动作 + 场景）

**Part 5 — 一致性追踪表**

| 角色 | 首次出场 | 服装变化记录 | 特征锚点 |
|------|----------|-------------|----------|
| 李骁 | 场次_01 | 场次_05 换装赴宴 | 左眉尾淡疤、玄色劲装 |

## 异常处理

- **剧本格式不规范**：无明显场次标记时，按场景/角色/时间变化自动拆分，标注 [自动拆分]
- **角色信息不完整**：首次出场缺外貌描写时，基于身份/职业/性格生成合理默认值，标注 [自动补全] 让用户确认
- **Prompt 自检**：每条 prompt 生成后检查是否包含主体+环境+光线+镜头+风格五要素，缺项则补全
- **长剧本分批处理**：超过 10 个场次时，每 5 场一批输出，避免上下文过长导致质量下降

## 输出示例

### 输入

```
第三场：废弃宫阙
李骁手持长剑，警惕地走入薄雾笼罩的大殿。殿内石柱断裂，地上散落着古老的铜镜碎片。
阳光从破败的穹顶倾泻而下，形成强烈的丁达尔效应。
```

### 输出

**结构化数据：**
```json
{
  "scene_id": "场次_03",
  "environment": "室内 / 废弃中式高层宫阙 / 薄雾笼罩 / 穹顶破败",
  "time_of_day": "白天",
  "characters": [{"name": "李骁", "emotion": "警惕", "action": "手持长剑缓步前行"}],
  "lighting": "体积感极强的丁达尔效应，阳光从破败穹顶倾泻，光柱穿透薄雾",
  "key_objects": ["古老铜镜碎片", "断裂石柱"],
  "mood": "压抑紧张"
}
```

**角色三视图 Prompt（李骁）：**

正面：
```
a young Chinese warrior male, sharp jawline, sword-like eyebrows, high nose bridge, a faint scar above left eyebrow, 182cm tall lean muscular build, black hair in high ponytail with loose strands over forehead, wearing dark patterned combat outfit with ancient bronze sword at waist and black leather wrist guards, front view, facing camera directly, full body from head to toe, standing in neutral relaxed pose, arms slightly away from body, clean white background, character reference sheet, full body shot, even studio lighting, no shadows, photorealistic, 8K, masterpiece --ar 2:3 --s 200 --q 2
```

侧面：
```
a young Chinese warrior male, sharp jawline, sword-like eyebrows, high nose bridge, a faint scar above left eyebrow, 182cm tall lean muscular build, black hair in high ponytail with loose strands over forehead, wearing dark patterned combat outfit with ancient bronze sword at waist and black leather wrist guards, side profile view, facing right, full body from head to toe, standing in neutral pose, clean white background, character reference sheet, full body shot, even studio lighting, no shadows, photorealistic, 8K, masterpiece --ar 2:3 --s 200 --q 2
```

背面：
```
a young Chinese warrior male, sharp jawline, sword-like eyebrows, high nose bridge, a faint scar above left eyebrow, 182cm tall lean muscular build, black hair in high ponytail with loose strands over forehead, wearing dark patterned combat outfit with ancient bronze sword at waist and black leather wrist guards, back view, facing away from camera, full body from head to toe, showing back of outfit and hair details, clean white background, character reference sheet, full body shot, even studio lighting, no shadows, photorealistic, 8K, masterpiece --ar 2:3 --s 200 --q 2
```

三视图总汇：
```
character turnaround reference sheet of a young Chinese warrior male, sharp jawline, sword-like eyebrows, high nose bridge, a faint scar above left eyebrow, 182cm tall lean muscular build, black hair in high ponytail with loose strands over forehead, wearing dark patterned combat outfit with ancient bronze sword at waist and black leather wrist guards, three full-body views arranged horizontally side by side on clean white background, left: front view facing camera, center: side profile view facing right, right: back view facing away, all three views showing full body from head to toe in identical neutral pose with arms slightly away from body, even studio lighting with no shadows, consistent appearance across all three views, character design sheet, photorealistic, 8K, masterpiece --ar 16:9 --s 200 --q 2
```

**场景四视图 Prompt（废弃宫阙）：**

正面全景：
```
interior of a ruined ancient Chinese palace hall at grand scale, collapsed dome with broken edges, massive broken stone pillars scattered across the floor, ancient bronze mirror fragments glinting on the ground, thin mist filling the space at ground level, dramatic volumetric Tyndall effect lighting with sunbeams streaming through the collapsed dome illuminating dust particles, front view, wide establishing shot, eye-level angle, showing the full space from the main entrance perspective, cinematic photorealistic 8K film grain, masterpiece best quality ultra-detailed --ar 16:9 --s 250 --q 2
```

侧面视角：
```
interior of a ruined ancient Chinese palace hall at grand scale, collapsed dome with broken edges, massive broken stone pillars scattered across the floor, ancient bronze mirror fragments glinting on the ground, thin mist filling the space at ground level, dramatic volumetric Tyndall effect lighting with sunbeams streaming through the collapsed dome illuminating dust particles, side angle view, 90-degree rotated perspective from the right side, showing depth and spatial layers between broken pillars, cinematic photorealistic 8K film grain, masterpiece best quality ultra-detailed --ar 16:9 --s 250 --q 2
```

俯瞰视角：
```
interior of a ruined ancient Chinese palace hall at grand scale, collapsed dome with broken edges, massive broken stone pillars scattered across the floor, ancient bronze mirror fragments glinting on the ground, thin mist filling the space at ground level, dramatic volumetric Tyndall effect lighting with sunbeams streaming through the collapsed dome illuminating dust particles, overhead bird's eye view, top-down angle looking straight down, showing floor plan layout and spatial structure with pillar positions, cinematic photorealistic 8K film grain, masterpiece best quality ultra-detailed --ar 16:9 --s 250 --q 2
```

反打视角：
```
interior of a ruined ancient Chinese palace hall at grand scale, collapsed dome with broken edges, massive broken stone pillars scattered across the floor, ancient bronze mirror fragments glinting on the ground, thin mist filling the space at ground level, dramatic volumetric Tyndall effect lighting with sunbeams streaming through the collapsed dome illuminating dust particles, reverse angle view, looking back toward the main entrance from the deepest point of the hall, showing what characters face when entering, cinematic photorealistic 8K film grain, masterpiece best quality ultra-detailed --ar 16:9 --s 250 --q 2
```

四视图总汇：
```
scene environment reference sheet of interior of a ruined ancient Chinese palace hall at grand scale, collapsed dome with broken edges, massive broken stone pillars scattered across the floor, ancient bronze mirror fragments glinting on the ground, thin mist filling the space at ground level, dramatic volumetric Tyndall effect lighting with sunbeams streaming through the collapsed dome illuminating dust particles, four views arranged in a 2x2 grid layout on a single image, top-left: front view wide establishing shot from entrance perspective, top-right: side angle view 90-degree rotated from right side, bottom-left: overhead bird's eye view looking straight down showing floor plan, bottom-right: reverse angle view looking back toward entrance from deepest point, all four views showing the same environment with identical objects and lighting but different camera angles, no people in any view, cinematic photorealistic 8K film grain, masterpiece best quality ultra-detailed --ar 16:9 --s 250 --q 2
```

**角色表演分镜 Prompt（关键帧）：**
```
a young Chinese warrior male with sharp jawline and black hair in high ponytail, wearing dark patterned combat outfit with bronze sword at waist, holding a gleaming longsword and cautiously stepping forward, inside a ruined ancient Chinese palace hall with broken stone pillars and scattered bronze mirror fragments, thin mist and dramatic Tyndall effect lighting, medium close-up low angle shot, dramatic lighting shallow DOF, cinematic photorealistic 8K film grain, masterpiece ultra-detailed --ar 16:9 --s 250 --q 2
```

**Negative Prompt（通用）：**
```
blurry, deformed, ugly, low quality, watermark, extra limbs, bad anatomy, modern elements, text, logo
```
