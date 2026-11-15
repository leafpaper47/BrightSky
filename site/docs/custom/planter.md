---
title: 播种机
createTime: 2026/11/15
---

# 播种机

<span class="bs-tag" style="color:#fba414;border-color:#fba414">传奇</span> · 最高 **Lv.1** · 内部 ID <code>planter</code>

> 右击可范围播种作物(需要种子)

## 基本信息

| 项目 | 内容 |
| --- | --- |
| 适用物品 | 锄 |
| 冲突附魔组 | — |
| 互斥附魔 | — |
| 每级效果预览 | `&7右击可范围播种作物(需要种子) (&a{边长}×&a{边长} &7冷却:&a{冷却}&7)` |
| 监听机制 | `on-right-click` ← player-interact |

## 数值参数

| 属性 | 单位 | 表达式 / 取值 |
| --- | --- | --- |
| 冷却 | 秒 | `3.5-{level}` |
| 边长 | 格 | `{level}+1` |
| 作物 | 常量 | `{"BEETROOT_SEEDS": "BEETROOTS", "MELON_SEEDS": "MELON_STEM", "PUMPKIN_SEEDS": "PUMPKIN_STEM", "TORCHFLOWER_SEEDS": "TORCHFLOWER_CROP", "WHEAT_SEEDS": "WHEAT", "CARROT": "CARROTS", "POTATO": "POTATOES"}` |
| 下界作物 | 常量 | `{"NETHER_WART": "NETHER_WART"}` |

> [!note] 表达式说明
> 公式中的 `{level}` 为附魔等级。除常数项外，其余数值随等级线性变化。
