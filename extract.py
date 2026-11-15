# -*- coding: utf-8 -*-
"""从 Aiyatsbus 与 NereusOpus 两个插件包里抽取全部附魔数据 -> data/enchants.json"""
import json, os, re, sys
import yaml

ROOT = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(ROOT, "raw")
OUT = os.path.join(ROOT, "data")


def load(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        try:
            return yaml.safe_load(f)
        except Exception as e:
            print("YAML FAIL", path, e, file=sys.stderr)
            return None


def s(v):
    if v is None:
        return ""
    return str(v).strip()


# ---------------- Aiyatsbus ----------------
def extract_aiya():
    base = os.path.join(RAW, "aiya", "enchants")
    rarity_raw = load(os.path.join(base, "rarity.yml")) or {}
    rarities = {}
    for key, v in rarity_raw.items():
        if not isinstance(v, dict):
            continue
        col = s(v.get("color"))
        m = re.search(r"#([0-9a-fA-F]{6})", col)
        rarities[key] = {
            "key": key,
            "name": s(v.get("name")),
            "color": ("#" + m.group(1)) if m else "#888888",
            "weight": v.get("weight"),
            "inaccessible": bool(v.get("inaccessible")),
        }
    by_name = {r["name"]: r for r in rarities.values()}

    out = []
    for sub, vanilla in (("Packet-Vanilla", True), ("Packet-Default", False)):
        d = os.path.join(base, sub)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".yml"):
                continue
            data = load(os.path.join(d, fn)) or {}
            basic = data.get("basic") or {}
            display = ((data.get("display") or {}).get("description") or {})
            rar_name = s(data.get("rarity"))
            rar = by_name.get(rar_name)
            lims = data.get("limitations") or []
            groups, conflicts = [], []
            for L in lims:
                L = s(L)
                if L.startswith("CONFLICT_GROUP:"):
                    groups.append(L.split(":", 1)[1])
                elif L.startswith("CONFLICT_ENCHANT:"):
                    conflicts.append(L.split(":", 1)[1])
                elif L:
                    conflicts.append(L)
            variables = data.get("variables") or {}
            leveled = {}
            for k, v in (variables.get("leveled") or {}).items():
                leveled[s(k)] = s(v)
            ordinary = {}
            for k, v in (variables.get("ordinary") or {}).items():
                if isinstance(v, (list, dict)):
                    ordinary[s(k)] = json.dumps(v, ensure_ascii=False)
                else:
                    ordinary[s(k)] = s(v)
            listeners = []
            mech = data.get("mechanisms") or {}
            for name, body in (mech.get("listeners") or {}).items():
                if isinstance(body, dict):
                    listeners.append({"name": s(name), "listen": s(body.get("listen"))})
            out.append({
                "plugin": "aiya",
                "id": s(basic.get("id")) or fn[:-4],
                "name": s(basic.get("name")),
                "max_level": basic.get("max-level", 1),
                "rarity_key": rar["key"] if rar else "",
                "rarity": rar["name"] if rar else rar_name,
                "rarity_color": rar["color"] if rar else "#888888",
                "targets": [s(t) for t in (data.get("targets") or [])],
                "conflict_groups": groups,
                "conflicts": conflicts,
                "general": s(display.get("general")),
                "specific": s(display.get("specific")),
                "variables_leveled": leveled,
                "variables_ordinary": ordinary,
                "listeners": listeners,
                "vanilla": vanilla,
                "enabled": basic.get("enable", True) is not False,
            })
    return rarities, out


# ---------------- NereusOpus ----------------
def extract_nereus():
    base = os.path.join(RAW, "nereus", "enchantments")
    rarity_raw = load(os.path.join(base, "rarities.yml")) or {}
    rarities = {}
    for key, v in rarity_raw.items():
        if not isinstance(v, dict):
            continue
        rarities[key] = {
            "key": key,
            "name": s(v.get("displayName")) or key,
            "color": s(v.get("colorFormat")) or "§7",
            "weight": v.get("weight"),
        }
    # 技能附魔用 unknown 品质，插件内置，不在 rarities.yml 里
    rarities.setdefault("unknown", {"key": "unknown", "name": "未知", "color": "§8", "weight": None})

    out = []
    for sub, kind in (("simple", "simple"), ("skill", "skill"), ("curse", "curse")):
        d = os.path.join(base, sub)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".yml"):
                continue
            data = load(os.path.join(d, fn)) or {}
            lim = data.get("limits") or {}
            rk = s(data.get("rarity")) or ("unknown" if kind == "skill" else "")
            rar = rarities.get(rk)
            params = data.get("params") or {}
            out.append({
                "plugin": "nereus",
                "kind": kind,
                "id": fn[:-4],
                "name": s(data.get("name")),
                "display_name": s(data.get("displayName")),
                "description": s(data.get("description")),
                "max_level": data.get("maxLevel", 1),
                "rarity_key": rk,
                "rarity": rar["name"] if rar else rk,
                "rarity_color": rar["color"] if rar else "§7",
                "grindstoneable": data.get("grindstoneable", True),
                "enabled": data.get("enabled", True) is not False,
                "targets": [s(t) for t in (lim.get("targets") or [])],
                "conflicts": [s(t) for t in (lim.get("conflicts") or [])],
                "needed": [s(t) for t in (lim.get("neededEnchants") or [])],
                "permission": s(lim.get("permission")),
                "params": {s(k): (json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else s(v))
                           for k, v in params.items()},
            })
    return rarities, out


def main():
    os.makedirs(OUT, exist_ok=True)
    ar, aiya = extract_aiya()
    nr, nereus = extract_nereus()
    data = {
        "aiya_rarity": ar,
        "aiya": aiya,
        "nereus_rarity": nr,
        "nereus": nereus,
    }
    with open(os.path.join(OUT, "enchants.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

    # 统计
    from collections import Counter
    print("aiya total", len(aiya),
          "vanilla", sum(1 for e in aiya if e["vanilla"]),
          "custom", sum(1 for e in aiya if not e["vanilla"]))
    print("aiya rarity", Counter(e["rarity"] for e in aiya))
    print("aiya missing name", [e["id"] for e in aiya if not e["name"]])
    nt = Counter(e["kind"] for e in nereus)
    print("nereus total", len(nereus), dict(nt))
    print("nereus rarity", Counter(e["rarity"] for e in nereus))
    print("nereus missing display", [e["id"] for e in nereus if not e["display_name"]][:20])
    print("nereus missing desc", [e["id"] for e in nereus if not e["description"]][:20])
    tg = Counter(t for e in nereus for t in e["targets"])
    print("nereus targets", dict(tg))
    ta = Counter(t for e in aiya for t in e["targets"])
    print("aiya targets", dict(ta))
    print("aiya rarity keys", list(ar.keys()))
    print("nereus rarity keys", list(nr.keys()))


if __name__ == "__main__":
    main()
