---
title: 索敌
createTime: 2026/11/15
---

# 索敌

<span class="bs-tag" style="color:#fbda41;border-color:#fbda41">稀世</span> · 最高 **Lv.1** · 内部 ID <code>aiming</code>

> 箭矢会自动追踪目标

## 基本信息

| 项目 | 内容 |
| --- | --- |
| 适用物品 | 弓 |
| 冲突附魔组 | — |
| 互斥附魔 | — |
| 每级效果预览 | `—` |
| 监听机制 | `on-shoot-bow` ← entity-shoot-bow |

## 数值参数

| 属性 | 单位 | 表达式 / 取值 |
| --- | --- | --- |
| steer_coefficient_xz | 常量 | `0.1` |
| steer_coefficient_y | 常量 | `0.08` |
| blacklist | 常量 | `["ALLAY", "VILLAGER", "WANDERING_TRADER", "WOLF", "CAT", "BAT", "ENDERMAN", "HORSE", "SKELETON_HORSE", "ZOMBIE_HORSE", "PIG", "COW", "SHEEP", "CAMEL", "CHICKEN", "COD", "DOLPHIN", "DONKEY", "FOX", "FROG", "GOAT", "IRON_GOLEM", "LLAMA", "MULE", "OCELOT", "PANDA", "PARROT", "POLAR_BEAR", "PUFFERFISH", "RABBIT", "SALMON", "SNIFFER", "SNOW_GOLEM", "TRADER_LLAMA", "TROPICAL_FISH", "TURTLE"]` |

> [!note] 表达式说明
> 公式中的 `{level}` 为附魔等级。除常数项外，其余数值随等级线性变化。
