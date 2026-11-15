---
title: 震地
createTime: 2026/11/15
---

# 震地

<span class="bs-tag" style="color:#fbda41;border-color:#fbda41">稀世</span> · 最高 **Lv.3** · 内部 ID <code>tremor</code>

> 蓄力范围真伤并减速, 满蓄力追加击飞效果

## 基本信息

| 项目 | 内容 |
| --- | --- |
| 适用物品 | 弓 |
| 冲突附魔组 | — |
| 互斥附魔 | — |
| 每级效果预览 | `—` |
| 监听机制 | `on-move` ← player-move、`on-released` ← aiyatsbus-bow-charge-released、`on-break` ← aiyatsbus-bow-charge-break、`on-prepare` ← aiyatsbus-bow-charge-prepare |

## 数值参数

| 属性 | 单位 | 表达式 / 取值 |
| --- | --- | --- |
| 宽度下限 | 格 | `1+{level}*0.5` |
| 宽度上限 | 格 | `3.5+{level}*0.5` |
| 深度增长速度 | 格/刻 | `0.7+{level}*0.1` |
| 基础伤害倍率 | 倍 | `{level}*2.0` |
| 敌人缓慢等级 | 级 | `{level}-1` |
| 冷却 | 秒 | `5` |
| 最大深度 | 常量 | `25.0` |
| 过滤生物类型 | 常量 | `["ARMOR_STAND"]` |

> [!note] 表达式说明
> 公式中的 `{level}` 为附魔等级。除常数项外，其余数值随等级线性变化。
