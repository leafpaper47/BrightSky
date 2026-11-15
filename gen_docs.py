# -*- coding: utf-8 -*-
"""白熊附魔大全 · BrightSky —— 由两个插件包的实际配置生成文档站内容。

输入：data/enchants.json（extract.py 产出）
输出：site/docs/**/*.md 与 site/docs/.vuepress/sidebar.ts
"""
import json, os, re
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "site", "docs")
DATA = json.load(open(os.path.join(ROOT, "data", "enchants.json"), encoding="utf-8"))

AIYA = DATA["aiya"]
NEREUS = DATA["nereus"]
AIYA_R = DATA["aiya_rarity"]
NEREUS_R = DATA["nereus_rarity"]

# ---------------- 颜色 / 名称 ----------------
CODE_HEX = {
    "0": "#000000", "1": "#0000AA", "2": "#00AA00", "3": "#00AAAA",
    "4": "#AA0000", "5": "#AA00AA", "6": "#FFAA00", "7": "#AAAAAA",
    "8": "#555555", "9": "#5555FF", "a": "#55FF55", "b": "#55FFFF",
    "c": "#FF5555", "d": "#FF55FF", "e": "#FFFF55", "f": "#FFFFFF",
}

TARGET_CN = {
    "swords": "剑", "axes": "斧", "bow": "弓", "crossbow": "弩", "trident": "三叉戟",
    "shears": "剪刀", "helmets": "头盔", "chestplates": "胸甲", "leggings": "护腿",
    "boots": "靴子", "pickaxes": "镐", "shovels": "铲", "hoes": "锄", "rod": "钓鱼竿",
    "shield": "盾牌", "elytra": "鞘翅", "all": "所有物品",
}

RARITY_ORDER = ["common", "uncommon", "rare", "epic", "legendary", "splendid", "unknown", "curse", "artifact"]
RARITY_CN = {
    "common": "普通", "uncommon": "罕见", "rare": "精良", "epic": "史诗",
    "legendary": "传奇", "splendid": "稀世", "unknown": "未知", "curse": "诅咒", "artifact": "皮肤",
}
RARITY_HEX = {
    "common": "#f8f4ed", "uncommon": "#66c18c", "rare": "#63bbd0", "epic": "#eb507e",
    "legendary": "#fba414", "splendid": "#fbda41", "unknown": "#9a9a9a", "curse": "#d42517",
    "artifact": "#ec9bad",
}

# NereusOpus 参数键 -> 中文说明（配置里仍是英文键，页面上双语并列）
PARAM_CN = {
    "chance": "触发概率", "damage-multiplier": "伤害倍率", "duration": "持续时间（刻）",
    "range": "作用范围", "amplifier": "效果等级", "require-full-charge": "需满蓄力",
    "cooldown": "冷却（秒）", "repeat-ticks": "重复间隔（刻）", "sound": "音效",
    "particle": "粒子效果", "damage": "伤害", "velocity": "速度", "power": "强度",
    "disable-on-sneak": "潜行时禁用", "permission-check": "权限校验", "targets": "作用目标",
    "durability-decrease": "耐久损耗", "durability-increase": "耐久增加",
    "durability-decrease-extra": "额外耐久损耗", "amount": "数量",
    "damage-splash": "溅射伤害", "damage-splash-multiplier": "溅射伤害倍率",
    "drops": "掉落物", "hardness-check": "硬度判定", "heal": "治疗量",
    "heal-multiplier": "治疗倍率", "disable-on-players": "对玩家禁用",
    "enable-sound": "启用音效", "blacklist": "黑名单", "percent": "百分比",
    "min-health": "最低生命", "min-health-percent": "最低生命百分比",
    "only_player": "仅对玩家", "avaliable-on-players": "对玩家生效（配置原文拼写）",
    "cause-fire": "造成着火", "break-blocks": "破坏方块", "angle": "角度",
    "items": "物品", "absorption-multiplier": "伤害吸收倍率", "custom-heads": "自定义头颅",
    "per-tick": "每刻生效", "range_x": "范围 X", "range_y": "范围 Y", "range_z": "范围 Z",
    "spread": "散布", "level_multiplier": "等级倍率", "cooldown-decreased": "冷却减免",
    "drop-xp": "掉落经验", "add-damage-multiplier": "追加伤害倍率",
    "del-damage-multiplier": "削减伤害倍率", "only-on-sneak": "仅潜行时生效",
    "softmode": "柔和模式", "oxygen": "氧气值", "max-distance": "最大距离",
    "delay": "延迟（刻）", "direct": "直接生效", "decrease-if-cooldown": "冷却中递减",
    "speed": "速度", "food": "饱食度", "check-radius": "检测半径",
    "check-delay": "检测间隔", "max-health-increase": "最大生命增加",
    "health-judging-line": "血量判定线", "high-damage-multiplier": "高伤倍率",
    "low-damage-multiplier": "低伤倍率", "exp-multiplier": "经验倍率",
    "tick-per": "每 N 刻", "blocks": "方块列表", "colored": "彩色高亮",
}


def nereus_hex(e):
    c = e.get("rarity_color") or "§7"
    m = re.match(r"^[§&]([0-9a-fA-F])$", c.strip())
    if m:
        return CODE_HEX.get(m.group(1).lower(), "#AAAAAA")
    return RARITY_HEX.get(e.get("rarity_key"), "#AAAAAA")


def strip_codes(t):
    return re.sub(r"[§&][0-9a-fk-orA-FK-OR]", "", t or "").strip()


def tag(text, color):
    return ('<span class="bs-tag" style="color:%s;border-color:%s">%s</span>' % (color, color, text))


def rarity_badge_aiya(e):
    return tag(e["rarity"], e["rarity_color"])


def rarity_badge_nereus(e):
    return tag(e["rarity"], nereus_hex(e))


def aiya_cn(key):
    """Aiyatsbus 自己的品质中文名（splendid=稀世）"""
    r = AIYA_R.get(key)
    return r["name"] if r else RARITY_CN.get(key, key)


def nereus_cn(key):
    """NereusOpus 自己的品质中文名（unknown=稀世）"""
    r = NEREUS_R.get(key)
    return r["name"] if r else RARITY_CN.get(key, key)


def cell(v):
    return (v or "").replace("|", "\\|")


def write(rel, text):
    path = os.path.join(DOCS, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    return path


def esc(t):
    # 表格/正文里避免被当成 HTML
    return (t or "").replace("<", "&lt;").replace(">", "&gt;")


# ---------------- 统计 ----------------
n_aiya_v = sum(1 for e in AIYA if e["vanilla"])
n_aiya_c = len(AIYA) - n_aiya_v
n_skill = [e for e in NEREUS if e["kind"] == "skill"]
n_simple = [e for e in NEREUS if e["kind"] == "simple"]
n_curse = [e for e in NEREUS if e["kind"] == "curse"]
TOTAL = len(AIYA) + len(NEREUS)

skill_by_id = {e["id"]: e for e in n_skill}
ALL_NAME = {e["id"]: e["display_name"] for e in NEREUS}


def ref_name(eid):
    """英文附魔 id -> 中文名（找不到就原样显示）"""
    return ALL_NAME.get(eid, eid)

# ---------------- 首页 ----------------
index = f"""---
title: 白熊附魔大全
createTime: 2026/11/15
permalink: /
---

# 白熊附魔大全 · BrightSky

基于 **Aiyatsbus** 与 **NereusOpus** 两个插件包内实际配置自动生成的附魔速查手册，共收录 **{TOTAL}** 个附魔。

| 分类 | 数量 | 说明 |
| --- | --- | --- |
| [原版附魔](/vanilla/) | {n_aiya_v} | 原版 45 个附魔的中文名、品质、适用物品与冲突 |
| [自定义附魔](/custom/) | {n_aiya_c} | Aiyatsbus 自研附魔（震地、飞矢、剑芒……） |
| [技能附魔](/skills/) | {len(n_skill)} | NereusOpus 主动技能（右击触发、带冷却） |
| [普通附魔](/simple/) | {len(n_simple)} | NereusOpus 被动附魔，共 {len(n_simple)} 个 |
| [诅咒附魔](/curse/) | {len(n_curse)} | NereusOpus 诅咒，负面效果 |
| [品质对照](/ref/rarity.md) | — | 两个插件各自的品质名称、颜色与权重 |
| [适用物品对照](/ref/targets.md) | — | 英文部位键与中文物品名对照 |

## 品质图例

{ " ".join(tag(RARITY_CN[k], RARITY_HEX[k]) for k in ["common","uncommon","rare","epic","legendary","splendid","curse"]) }

## 阅读说明

- 每个附魔页面均标注 **品质 / 最高等级 / 适用物品 / 冲突关系 / 数值参数**，数据直接来自插件默认配置。
- 原版附魔的机制由客户端与服务端原版逻辑实现，本插件只改显示与命名，因此“数值参数”一栏不重复列出。
- 品质名称在两套插件中并不完全等价：Aiyatsbus 的稀世档内部键名是 splendid，NereusOpus 用的是 unknown（同一档，并非「未知品质」），详见 [品质对照](/ref/rarity.md)。
- 本站内容随配置更新重新生成，如与你服务器上的实际配置不同，以服务器 `plugins/` 下的 yml 为准。
"""
write("index.md", index)

# ---------------- 原版附魔 ----------------
vanilla = [e for e in AIYA if e["vanilla"]]
vanilla.sort(key=lambda e: (RARITY_ORDER.index(e["rarity_key"]) if e["rarity_key"] in RARITY_ORDER else 99, e["name"]))
rows = []
for e in vanilla:
    rows.append("| {name} | {rar} | {lv} | {tg} | {cf} | {desc} |".format(
        name=f"**{cell(e['name'])}**<br><code>{e['id']}</code>",
        rar=rarity_badge_aiya(e),
        lv=e["max_level"],
        tg=cell("、".join(e["targets"]) or "—"),
        cf=cell("、".join(e["conflicts"]) or "—"),
        desc=cell(e["general"]) or "—",
    ))
van = f"""---
title: 原版附魔
createTime: 2026/11/15
---

# 原版附魔（{len(vanilla)} 个）

Aiyatsbus 接管原版附魔的**名称、品质、适用物品与冲突**，附魔效果本身仍由原版实现。

> [!tip] 「原版附魔」与「自定义附魔」的区别
> 原版附魔（锋利、保护、时运……）机制不变，只是被赋予了中文品质与说明；
> Aiyatsbus 的自定义附魔则运行 Fluxon 脚本，可以做到原版没有的效果。

| 附魔 | 品质 | 最高等级 | 适用物品 | 冲突 | 说明 |
| --- | --- | --- | --- | --- | --- |
{chr(10).join(rows)}
"""
write("vanilla/index.md", van)

# ---------------- 自定义附魔（Aiyatsbus） ----------------
custom = [e for e in AIYA if not e["vanilla"]]
custom.sort(key=lambda e: (RARITY_ORDER.index(e["rarity_key"]) if e["rarity_key"] in RARITY_ORDER else 99, e["name"]))

cards = []
for e in custom:
    cards.append(f"### [{e['name']}](/custom/{e['id']}.md)\n\n"
                 f"{rarity_badge_aiya(e)} · 最高 **Lv.{e['max_level']}** · 适用：{('、'.join(e['targets']) or '—')}\n\n"
                 f"{cell(e['general']) or '—'}\n")
custom_index = f"""---
title: 自定义附魔
createTime: 2026/11/15
---

# 自定义附魔（{len(custom)} 个）

Aiyatsbus 内置的非原版附魔，机制由 Fluxon 脚本驱动，可组合出原版没有的战斗效果。

{chr(10).join(cards)}
"""
write("custom/index.md", custom_index)


def aiya_page(e):
    var_rows = []
    for k, v in e["variables_leveled"].items():
        unit, _, expr = v.partition(":")
        if not expr:
            unit, expr = "", v
        var_rows.append(f"| {cell(k)} | {cell(unit) or '—'} | `{cell(expr)}` |")
    for k, v in e["variables_ordinary"].items():
        var_rows.append(f"| {cell(k)} | 常量 | `{cell(v)}` |")
    if not var_rows:
        var_rows.append("| — | — | 该附魔无数值参数 |")
    lst = "、".join(f"`{l['name']}` ← {l['listen']}" for l in e["listeners"]) or "—"
    groups = "、".join(e["conflict_groups"]) or "—"
    conflicts = "、".join(e["conflicts"]) or "—"
    return f"""---
title: {e['name']}
createTime: 2026/11/15
---

# {e['name']}

{rarity_badge_aiya(e)} · 最高 **Lv.{e['max_level']}** · 内部 ID <code>{e['id']}</code>

> {cell(e['general']) or '（无说明）'}

## 基本信息

| 项目 | 内容 |
| --- | --- |
| 适用物品 | {'、'.join(e['targets']) or '—'} |
| 冲突附魔组 | {groups} |
| 互斥附魔 | {conflicts} |
| 每级效果预览 | `{cell(e['specific']) or '—'}` |
| 监听机制 | {lst} |

## 数值参数

| 属性 | 单位 | 表达式 / 取值 |
| --- | --- | --- |
{chr(10).join(var_rows)}

> [!note] 表达式说明
> 公式中的 `{{level}}` 为附魔等级。除常数项外，其余数值随等级线性变化。
"""
for e in custom:
    write(f"custom/{e['id']}.md", aiya_page(e))

# ---------------- 技能附魔（NereusOpus） ----------------
n_skill.sort(key=lambda e: (RARITY_ORDER.index(e["rarity_key"]) if e["rarity_key"] in RARITY_ORDER else 99, e["display_name"]))
skill_cards = []
for e in n_skill:
    cd = e["params"].get("cooldown", "")
    cd_txt = f" · 冷却 {cd} 秒" if cd else ""
    skill_cards.append(
        f"### [{e['display_name']}](/skills/{e['id']}.md)\n\n"
        f"{rarity_badge_nereus(e)} · 最高 **Lv.{e['max_level']}**{cd_txt} · 适用：{('、'.join(TARGET_CN.get(t, t) for t in e['targets']) or '—')}\n\n"
        f"{cell(strip_codes(e['description'])) or '—'}\n")
skills_index = f"""---
title: 技能附魔
createTime: 2026/11/15
---

# 技能附魔（{len(n_skill)} 个）

NereusOpus 的**主动技能**：装在对应物品上后，按右键（默认，可在配置里改成左键/切手）触发，有独立冷却。

{chr(10).join(skill_cards)}
"""
write("skills/index.md", skills_index)


def nereus_page(e):
    prm = []
    for k, v in e["params"].items():
        label = PARAM_CN.get(k)
        name = f"{label} <code>{k}</code>" if label else f"<code>{k}</code>"
        val = cell(v)
        if (val.startswith("{") or val.startswith("[")) and len(val) > 60:
            try:
                obj = json.loads(v)
                if isinstance(obj, dict):
                    val = f"{len(obj)} 组：" + "、".join(str(x) for x in list(obj)[:6]) + ("…" if len(obj) > 6 else "")
                else:
                    val = "、".join(str(x) for x in obj[:6]) + ("…" if len(obj) > 6 else "")
                prm.append(f"| {name} | {val}（详见插件配置） |")
                continue
            except Exception:
                val = val[:60] + "…"
        prm.append(f"| {name} | `{val}` |")
    if not prm:
        prm.append("| — | 该附魔无额外参数 |")
    lim = []
    if e["targets"]:
        lim.append("**适用物品**：" + "、".join(TARGET_CN.get(t, t) for t in e["targets"]))
    if e["needed"]:
        lim.append("**前置附魔**：" + "、".join(ref_name(t) for t in e["needed"]))
    if e["conflicts"]:
        lim.append("**互斥附魔**：" + "、".join(ref_name(t) for t in e["conflicts"]))
    if e["permission"]:
        lim.append(f"**使用权限**：`{e['permission']}`")
    lim.append(f"**砂轮可移除**：{'是' if e['grindstoneable'] else '否'}")
    return f"""---
title: {e['display_name']}
createTime: 2026/11/15
---

# {e['display_name']} · {e['name']}

{rarity_badge_nereus(e)} · 最高 **Lv.{e['max_level']}** · 内部 ID <code>{e['id']}</code>

> {cell(strip_codes(e['description'])) or '（无说明）'}

## 使用条件

{chr(10).join('- ' + x for x in lim)}

## 参数

| 参数 | 取值 |
| --- | --- |
{chr(10).join(prm)}
"""
for e in n_skill:
    write(f"skills/{e['id']}.md", nereus_page(e))

# ---------------- 普通附魔（按品质分页） ----------------
groups = defaultdict(list)
for e in n_simple:
    groups[e["rarity_key"]].append(e)
simp_cards = []
for k in RARITY_ORDER:
    if k in groups and groups[k]:
        simp_cards.append(f"- **{nereus_cn(k)}**（{len(groups[k])} 个）— [查看列表](/simple/{k}.md) "
                          f"{tag(nereus_cn(k), RARITY_HEX.get(k,'#888'))}")
simple_index = f"""---
title: 普通附魔
createTime: 2026/11/15
---

# 普通附魔（{len(n_simple)} 个）

NereusOpus 的**被动附魔**：装在物品上即生效，按下表品质分页查看。

{chr(10).join(simp_cards)}

> [!tip] 查找技巧
> 站内搜索（右上角）可直接输入中文名或英文 ID 跳转。
"""
write("simple/index.md", simple_index)

for k in RARITY_ORDER:
    lst = groups.get(k) or []
    if not lst:
        continue
    lst.sort(key=lambda e: e["display_name"])
    rows = []
    for e in lst:
        rows.append("| {n} | {lv} | {tg} | {cf} | {d} |".format(
            n=f"**{cell(e['display_name'])}**<br><code>{e['id']}</code>",
            lv=e["max_level"],
            tg=cell("、".join(TARGET_CN.get(t, t) for t in e["targets"]) or "—"),
            cf=cell("、".join(ref_name(t) for t in e["conflicts"]) or "—"),
            d=cell(strip_codes(e["description"])) or "—",
        ))
    write(f"simple/{k}.md", f"""---
title: {nereus_cn(k)}品质附魔
createTime: 2026/11/15
---

# {nereus_cn(k)} · 普通附魔（{len(lst)} 个）

| 附魔 | 最高等级 | 适用物品 | 互斥 | 效果 |
| --- | --- | --- | --- | --- |
{chr(10).join(rows)}
""")

# ---------------- 诅咒附魔 ----------------
n_curse.sort(key=lambda e: e["display_name"])
crows = []
for e in n_curse:
    crows.append("| {n} | {lv} | {tg} | {d} |".format(
        n=f"**{cell(e['display_name'])}**<br><code>{e['id']}</code>",
        lv=e["max_level"],
        tg=cell("、".join(TARGET_CN.get(t, t) for t in e["targets"]) or "—"),
        d=cell(strip_codes(e["description"])) or "—",
    ))
write("curse/index.md", f"""---
title: 诅咒附魔
createTime: 2026/11/15
---

# 诅咒附魔（{len(n_curse)} 个）

NereusOpus 的负面附魔，会给持有者带来惩罚，只能靠砂轮或祛魔手段清除。

| 附魔 | 最高等级 | 适用物品 | 效果 |
| --- | --- | --- | --- |
{chr(10).join(crows)}
""")

# ---------------- 品质对照 ----------------
# (展示名, Aiyatsbus 的 key, NereusOpus 的 key, 备注)
RARITY_MAP = [
    ("普通", "common", "common", "最常见的底子货"),
    ("罕见", "uncommon", "uncommon", "少量增益"),
    ("精良", "rare", "rare", "主流战力档"),
    ("史诗", "epic", "epic", "强力效果"),
    ("传奇", "legendary", "legendary", "顶级稀有"),
    ("稀世", "splendid", "unknown", "两插件命名不同：Aiyatsbus 叫 splendid，NereusOpus 叫 unknown"),
    ("诅咒", "curse", "curse", "负面效果，只能砂轮清除"),
    ("皮肤", "artifact", "artifact", "外观类，不参与正常产出"),
]
arows = []
for label, ak, nk, note in RARITY_MAP:
    a = AIYA_R.get(ak)
    n = NEREUS_R.get(nk)
    if not a and not n:
        continue
    acell = (f"**{a['name']}** · 权重 {a['weight']} · <code>{a['color']}</code>") if a else "—"
    ncell = (f"**{n['name']}** · 权重 {n['weight']} · <code>{n['color']}</code>") if n else "—"
    arows.append(f"| {tag(label, RARITY_HEX.get(ak, '#888'))} | {acell} | {ncell} | {note} |")
write("ref/rarity.md", f"""---
title: 品质对照
createTime: 2026/11/15
---

# 品质对照表

两个插件各自维护一套品质体系，中文名大体一致，但**内部键名、权重与颜色不同**。

| 通用档位 | Aiyatsbus | NereusOpus | 备注 |
| --- | --- | --- | --- |
{chr(10).join(arows)}

补充说明：

- **Aiyatsbus**：品质决定附魔书的显示模型与附魔台出现权重；`皮肤（artifact）` 标记 `inaccessible`，不会从任何正常渠道产出。
- **NereusOpus**：稀世档的内部键名是 `unknown`（权重 1），与 Aiyatsbus 的 `splendid` 对应，**不是「未知品质」**；技能附魔也普遍使用该档。
- 诅咒在两套体系里都是独立档位（权重 25），不影响其它品质的产出概率。
- 两套品质的**颜色值不同**（Aiyatsbus 用 `#hex`，NereusOpus 用 `§` 颜色码），本站按各自配置着色。
""")

# ---------------- 适用物品对照 ----------------
used = Counter()
for e in NEREUS:
    for t in e["targets"]:
        used[t] += 1
trows = []
for k, v in used.most_common():
    trows.append(f"| `{k}` | {TARGET_CN.get(k, k)} | {v} |")
aiya_t = Counter()
for e in AIYA:
    for t in e["targets"]:
        aiya_t[t] += 1
atrows = "\n".join(f"| {t} | {c} |" for t, c in aiya_t.most_common())
write("ref/targets.md", f"""---
title: 适用物品对照
createTime: 2026/11/15
---

# 适用物品对照

## NereusOpus（配置中用英文键）

| 配置键 | 中文 | 附魔数量 |
| --- | --- | --- |
{chr(10).join(trows)}

## Aiyatsbus（配置中直接写中文）

| 中文物品 | 附魔数量 |
| --- | --- |
{atrows}
""")

# ---------------- sidebar.ts ----------------
def q(s):
    return json.dumps(s, ensure_ascii=False)


def item(e, base):
    return "        { text: %s, link: '%s/%s.md' }," % (q(e_name(e)), base, e["id"])


def e_name(e):
    return e["display_name"] if e["plugin"] == "nereus" else e["name"]


simple_groups = []
for k in RARITY_ORDER:
    if groups.get(k):
        simple_groups.append("        { text: %s, link: '/simple/%s.md' }," % (q(f"{nereus_cn(k)}（{len(groups[k])}）"), k))

sidebar = f"""import type {{ ThemeNavItem, ThemeSidebarMulti }} from 'vuepress-theme-plume'

export const navbar: ThemeNavItem[] = [
  {{ text: '首页', link: '/' }},
  {{ text: '原版附魔', link: '/vanilla/' }},
  {{ text: '自定义附魔', link: '/custom/' }},
  {{ text: '技能附魔', link: '/skills/' }},
  {{ text: '普通附魔', link: '/simple/' }},
  {{ text: '诅咒附魔', link: '/curse/' }},
  {{ text: '品质对照', link: '/ref/rarity' }},
  {{ text: '物品对照', link: '/ref/targets' }},
]

export const sidebar: ThemeSidebarMulti = {{
  '/vanilla/': [
    {{ text: '🪄 附魔总览', link: '/' }},
    {{ text: '原版附魔', link: '/vanilla/' }},
  ],
  '/custom/': [
    {{ text: '🪄 附魔总览', link: '/' }},
    {{ text: '自定义附魔', link: '/custom/' }},
    {{
      text: '⚔️ Aiyatsbus 自定义附魔',
      link: '/custom/',
      collapsed: false,
      items: [
{chr(10).join(item(e, '/custom') for e in custom)}
      ],
    }},
  ],
  '/skills/': [
    {{ text: '🪄 附魔总览', link: '/' }},
    {{ text: '技能附魔', link: '/skills/' }},
    {{
      text: '✨ 主动技能',
      link: '/skills/',
      collapsed: false,
      items: [
{chr(10).join(item(e, '/skills') for e in n_skill)}
      ],
    }},
  ],
  '/simple/': [
    {{ text: '🪄 附魔总览', link: '/' }},
    {{ text: '普通附魔', link: '/simple/' }},
    {{
      text: '📚 按品质浏览',
      link: '/simple/',
      collapsed: false,
      items: [
{chr(10).join(simple_groups)}
      ],
    }},
  ],
  '/curse/': [
    {{ text: '🪄 附魔总览', link: '/' }},
    {{ text: '诅咒附魔', link: '/curse/' }},
  ],
  '/ref/': [
    {{ text: '🪄 附魔总览', link: '/' }},
    {{ text: '品质对照', link: '/ref/rarity.md' }},
    {{ text: '适用物品对照', link: '/ref/targets.md' }},
  ],
}}
"""
write(".vuepress/sidebar.ts", sidebar)

# 分类首页必须是普通文档布局（root README 才是 home），否则正文会被 hero 页吞掉
for rel in ["vanilla/index.md", "custom/index.md", "skills/index.md",
            "simple/index.md", "curse/index.md", "ref/rarity.md", "ref/targets.md"]:
    p = os.path.join(DOCS, rel)
    with open(p, encoding="utf-8") as f:
        txt = f.read()
    txt = re.sub(r"^pageLayout:\s*\w+\n", "", txt, flags=re.M)
    txt = txt.replace("---\n\n", "---\n\n", 1)
    end = txt.index("\n---\n", 3)
    fm = txt[:end]
    if "pageLayout:" not in fm:
        fm = fm + "\npageLayout: doc"
    txt = fm + txt[end:]
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(txt)

print("pages written:", TOTAL, "enchants")
print("  vanilla", len(vanilla), "custom", len(custom), "skill", len(n_skill), "simple", len(n_simple), "curse", len(n_curse))
