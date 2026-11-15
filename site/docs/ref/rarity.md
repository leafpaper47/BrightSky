---
title: 品质对照
createTime: 2026/11/15
pageLayout: doc
---

# 品质对照表

两个插件各自维护一套品质体系，中文名大体一致，但**内部键名、权重与颜色不同**。

| 通用档位 | Aiyatsbus | NereusOpus | 备注 |
| --- | --- | --- | --- |
| <span class="bs-tag" style="color:#f8f4ed;border-color:#f8f4ed">普通</span> | **普通** · 权重 1000 · <code>#f8f4ed</code> | **普通** · 权重 500 · <code>§7</code> | 最常见的底子货 |
| <span class="bs-tag" style="color:#66c18c;border-color:#66c18c">罕见</span> | **罕见** · 权重 500 · <code>#66c18c</code> | **罕见** · 权重 250 · <code>§a</code> | 少量增益 |
| <span class="bs-tag" style="color:#63bbd0;border-color:#63bbd0">精良</span> | **精良** · 权重 250 · <code>#63bbd0</code> | **精良** · 权重 125 · <code>§b</code> | 主流战力档 |
| <span class="bs-tag" style="color:#eb507e;border-color:#eb507e">史诗</span> | **史诗** · 权重 50 · <code>#eb507e</code> | **史诗** · 权重 25 · <code>§d</code> | 强力效果 |
| <span class="bs-tag" style="color:#fba414;border-color:#fba414">传奇</span> | **传奇** · 权重 10 · <code>#fba414</code> | **传奇** · 权重 5 · <code>§6</code> | 顶级稀有 |
| <span class="bs-tag" style="color:#fbda41;border-color:#fbda41">稀世</span> | **稀世** · 权重 5 · <code>#fbda41</code> | **稀世** · 权重 1 · <code>§e</code> | 两插件命名不同：Aiyatsbus 叫 splendid，NereusOpus 叫 unknown |
| <span class="bs-tag" style="color:#d42517;border-color:#d42517">诅咒</span> | **诅咒** · 权重 25 · <code>#d42517</code> | **诅咒** · 权重 25 · <code>§c</code> | 负面效果，只能砂轮清除 |
| <span class="bs-tag" style="color:#ec9bad;border-color:#ec9bad">皮肤</span> | **皮肤** · 权重 1 · <code>#ec9bad</code> | **皮肤** · 权重 1 · <code>§7</code> | 外观类，不参与正常产出 |

补充说明：

- **Aiyatsbus**：品质决定附魔书的显示模型与附魔台出现权重；`皮肤（artifact）` 标记 `inaccessible`，不会从任何正常渠道产出。
- **NereusOpus**：稀世档的内部键名是 `unknown`（权重 1），与 Aiyatsbus 的 `splendid` 对应，**不是「未知品质」**；技能附魔也普遍使用该档。
- 诅咒在两套体系里都是独立档位（权重 25），不影响其它品质的产出概率。
- 两套品质的**颜色值不同**（Aiyatsbus 用 `#hex`，NereusOpus 用 `§` 颜色码），本站按各自配置着色。
