---
title: 反击
createTime: 2026/11/15
---

# 反击

<span class="bs-tag" style="color:#fba414;border-color:#fba414">传奇</span> · 最高 **Lv.3** · 内部 ID <code>counter</code>

> 举盾格挡时记录伤害，短时间内下一次攻击造成额外伤害

## 基本信息

| 项目 | 内容 |
| --- | --- |
| 适用物品 | 盾牌 |
| 冲突附魔组 | — |
| 互斥附魔 | — |
| 每级效果预览 | `&7举盾格挡时记录伤害，&a{蓄力窗口}&7内下一次攻击额外造成&a{反击倍率}&7倍伤害` |
| 监听机制 | `on-block` ← entity-damaged-by-other、`on-attack` ← entity-damage-other |

## 数值参数

| 属性 | 单位 | 表达式 / 取值 |
| --- | --- | --- |
| 蓄力窗口 | 秒 | `3+1*{level}` |
| 反击倍率 | 倍 | `0.5+0.5*{level}` |

> [!note] 表达式说明
> 公式中的 `{level}` 为附魔等级。除常数项外，其余数值随等级线性变化。
