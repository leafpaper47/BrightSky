#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
把 data/enchants.json（extract.py 的产物）整理成 web/data.json，
供 web/index.html 这个纯静态查询页使用。

    python extract.py      # 插件 jar → data/enchants.json
    python build_app.py    # data/enchants.json → web/data.json
"""
import json
import os
import re
import html

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "data", "enchants.json")
OUT = os.path.join(HERE, "web", "data.json")

# ---------------- 对照表 ----------------
TARGET_CN = {
    "swords": "剑", "axes": "斧", "bow": "弓", "crossbow": "弩", "trident": "三叉戟",
    "shears": "剪刀", "helmets": "头盔", "chestplates": "胸甲", "leggings": "护腿",
    "boots": "靴子", "pickaxes": "镐", "shovels": "铲", "hoes": "锄", "rod": "钓鱼竿",
    "shield": "盾牌", "elytra": "鞘翅", "all": "所有物品",
}
TARGET_EMOJI = {
    "剑": "🗡️", "斧": "🪓", "弓": "🏹", "弩": "🎯", "三叉戟": "🔱", "剪刀": "✂️",
    "头盔": "⛑️", "胸甲": "🦺", "护腿": "👖", "靴子": "👢", "镐": "⛏️", "铲": "🥄",
    "锄": "🌾", "钓鱼竿": "🎣", "盾牌": "🛡️", "鞘翅": "🪽", "所有物品": "✨",
    "矛": "⚔️", "重锤": "🔨", "可损坏物品": "🧰", "头饰": "👑",
}
# Aiyatsbus 的 targets 本来就是中文，个别写法统一一下
TARGET_ALIAS = {
    "剑": "剑", "斧": "斧", "弓": "弓", "弩": "弩", "三叉戟": "三叉戟",
    "头盔": "头盔", "胸甲": "胸甲", "护腿": "护腿", "靴子": "靴子",
    "镐": "镐", "锹": "铲", "铲": "铲", "锄": "锄", "剪刀": "剪刀",
    "盾牌": "盾牌", "盾": "盾牌", "鞘翅": "鞘翅", "钓鱼竿": "钓鱼竿",
    "钓竿": "钓鱼竿", "所有物品": "所有物品", "全部": "所有物品", "全部物品": "所有物品",
}

RARITY_ORDER = ["common", "uncommon", "rare", "epic", "legendary", "splendid", "unknown", "curse", "artifact"]
RARITY_CN = {
    "common": "普通", "uncommon": "罕见", "rare": "精良", "epic": "史诗",
    "legendary": "传奇", "splendid": "稀世", "unknown": "稀世", "curse": "诅咒", "artifact": "皮肤",
}
RARITY_HEX = {
    "common": "#c9c4b4", "uncommon": "#66c18c", "rare": "#63bbd0", "epic": "#eb507e",
    "legendary": "#fba414", "splendid": "#fbda41", "unknown": "#fbda41", "curse": "#d42517",
    "artifact": "#ec9bad",
}
CODE_HEX = {
    "0": "#000000", "1": "#0000aa", "2": "#00aa00", "3": "#00aaaa", "4": "#aa0000",
    "5": "#aa00aa", "6": "#ffaa00", "7": "#aaaaaa", "8": "#555555", "9": "#5555ff",
    "a": "#55ff55", "b": "#55ffff", "c": "#ff5555", "d": "#ff55ff", "e": "#ffff55",
    "f": "#ffffff",
}

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
    "only_player": "仅对玩家", "avaliable-on-players": "对玩家生效（原文拼写）",
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

KIND = {
    "vanilla": "原版", "custom": "自定义", "skill": "技能", "simple": "被动", "curse": "诅咒",
}
SRC_LABEL = {"aiya": "Aiyatsbus", "nereus": "NereusOpus"}
LISTEN_CN = {
    "entity-damage-other": "造成伤害时", "entity-death": "击杀生物时", "block-break": "破坏方块时",
    "block-place": "放置方块时", "player-interact": "玩家交互时", "player-fish": "钓鱼时",
    "player-move": "移动时", "player-tick": "每刻", "entity-damage": "受到伤害时",
    "player-item-break": "物品损坏时", "entity-shoot-bow": "射箭时", "player-eat": "进食时",
}

code_re = re.compile(r"[§&][0-9a-fk-orA-FK-OR]")


def strip_codes(t):
    return code_re.sub("", t or "").strip()


def colorize(t):
    """把 §/& 颜色码转成 <span class="mcf-x">，其余格式码丢弃。"""
    t = html.escape(t or "")
    out = []
    open_span = False
    i = 0
    while i < len(t):
        if t[i] in "§&" and i + 1 < len(t):
            c = t[i + 1].lower()
            if c in CODE_HEX:
                if open_span:
                    out.append("</span>")
                out.append('<span class="mcf-%s">' % c)
                open_span = True
                i += 2
                continue
            if c == "r":
                if open_span:
                    out.append("</span>")
                    open_span = False
                i += 2
                continue
            if c in "klmno":
                tag = {"k": "obf", "l": "b", "m": "del", "n": "u", "o": "i"}[c]
                out.append("<%s>" % tag)
                i += 2
                continue
        out.append(t[i])
        i += 1
    if open_span:
        out.append("</span>")
    return "".join(out)


def nereus_hex(e):
    c = (e.get("rarity_color") or "§7").strip()
    m = re.match(r"^[§&]([0-9a-fA-F])$", c)
    if m:
        return CODE_HEX.get(m.group(1).lower(), "#AAAAAA")
    return RARITY_HEX.get(e.get("rarity_key"), "#AAAAAA")


def norm_targets(values):
    res = []
    for v in values or []:
        if not v:
            continue
        cn = TARGET_CN.get(v) or TARGET_ALIAS.get(v) or v
        if cn not in res:
            res.append(cn)
    return res


def build_aiya(e):
    desc = " ".join(x for x in (strip_codes(e.get("general")), strip_codes(e.get("specific"))) if x)
    desc_html = colorize(e.get("general") or "")
    spec = colorize(e.get("specific") or "")
    if spec:
        desc_html = (desc_html + '<span class="mcf-7"> ' + spec + "</span>").strip()
    params = []
    for k, v in (e.get("variables_leveled") or {}).items():
        unit, _, expr = str(v).partition(":")
        params.append({"k": k, "cn": "", "v": expr + (" " + unit if unit else "")})
    for k, v in (e.get("variables_ordinary") or {}).items():
        params.append({"k": k, "cn": "", "v": str(v)})
    listeners = []
    for l in e.get("listeners") or []:
        name = l.get("listen") or l.get("name") or ""
        listeners.append(LISTEN_CN.get(name, name))
    item = {
        "id": e["id"],
        "name": e.get("name") or e["id"],
        "en": "",
        "src": "aiya",
        "kind": "vanilla" if e.get("vanilla") else "custom",
        "lv": e.get("max_level"),
        "rarity": RARITY_CN.get(e.get("rarity_key"), e.get("rarity") or ""),
        "rc": RARITY_HEX.get(e.get("rarity_key"), "#AAAAAA"),
        "tg": norm_targets(e.get("targets")),
        "desc": desc,
        "descHtml": desc_html,
        "conflicts": [c for c in (e.get("conflicts") or []) if c],
        "groups": [c for c in (e.get("conflict_groups") or []) if c],
        "need": [],
        "params": params,
        "listeners": listeners,
        "perm": "",
        "gs": True,
    }
    return item


def build_nereus(e):
    desc = strip_codes(e.get("description"))
    params = []
    for k, v in (e.get("params") or {}).items():
        params.append({"k": k, "cn": PARAM_CN.get(k, ""), "v": str(v)})
    return {
        "id": e["id"],
        "name": e.get("display_name") or e.get("name") or e["id"],
        "en": e.get("name") or "",
        "src": "nereus",
        "kind": e.get("kind") or "simple",
        "lv": e.get("max_level"),
        "rarity": RARITY_CN.get(e.get("rarity_key"), e.get("rarity") or ""),
        "rc": nereus_hex(e),
        "tg": norm_targets(e.get("targets")),
        "desc": desc,
        "descHtml": colorize(e.get("description") or ""),
        "conflicts": [c for c in (e.get("conflicts") or []) if c],
        "groups": [],
        "need": [c for c in (e.get("needed") or []) if c],
        "params": params,
        "listeners": [],
        "perm": e.get("permission") or "",
        "gs": bool(e.get("grindstoneable")),
    }


def main():
    with open(SRC, encoding="utf-8") as f:
        raw = json.load(f)

    items = [build_aiya(e) for e in raw["aiya"]] + [build_nereus(e) for e in raw["nereus"]]

    # 品质归一到「稀世」后去重
    rarity_seen = {}
    for it in items:
        key = it["rarity"]
        rarity_seen.setdefault(key, it["rc"])

    order = ["普通", "罕见", "精良", "史诗", "传奇", "稀世", "诅咒", "皮肤"]
    rarities = [
        {"cn": r, "hex": rarity_seen[r], "count": sum(1 for i in items if i["rarity"] == r)}
        for r in order if r in rarity_seen
    ]

    # 物品分类（去重 + 计数）
    tcount = {}
    for it in items:
        for t in it["tg"]:
            tcount[t] = tcount.get(t, 0) + 1
    targets = [
        {"cn": t, "emoji": TARGET_EMOJI.get(t, "❔"), "count": c}
        for t, c in sorted(tcount.items(), key=lambda kv: -kv[1])
    ]

    # 搜索用文本（小写、去符号）
    for it in items:
        blob = " ".join([
            it["name"], it["en"], it["id"], it["desc"], it["rarity"],
            KIND.get(it["kind"], ""), SRC_LABEL.get(it["src"], ""), " ".join(it["tg"]),
            " ".join(p["k"] + " " + p["cn"] + " " + p["v"] for p in it["params"]),
            " ".join(it["conflicts"]) + " " + " ".join(it["groups"]) + " " + " ".join(it["need"]),
            " ".join(it["listeners"]),
        ])
        it["s"] = re.sub(r"\s+", " ", blob).lower()

    for it in items:
        it["kindLabel"] = KIND.get(it["kind"], it["kind"])
        it["srcLabel"] = SRC_LABEL.get(it["src"], it["src"])

    items.sort(key=lambda i: (i["src"], {"vanilla": 0, "custom": 1, "skill": 2, "simple": 3, "curse": 4}.get(i["kind"], 9), i["id"]))

    out = {
        "meta": {
            "total": len(items),
            "counts": {
                "Aiyatsbus": sum(1 for i in items if i["src"] == "aiya"),
                "NereusOpus": sum(1 for i in items if i["src"] == "nereus"),
            },
            "kinds": [
                {"key": k, "label": KIND[k], "count": sum(1 for i in items if i["kind"] == k)}
                for k in ("vanilla", "custom", "skill", "simple", "curse")
            ],
        },
        "rarities": rarities,
        "targets": targets,
        "items": items,
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    print("wrote", OUT, "items:", len(items), "size(KB):", round(os.path.getsize(OUT) / 1024, 1))
    print("rarities:", [(r["cn"], r["count"]) for r in rarities])
    print("targets:", [(t["cn"], t["count"]) for t in targets])


if __name__ == "__main__":
    main()
