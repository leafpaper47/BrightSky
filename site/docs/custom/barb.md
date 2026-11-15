---
title: 棘盾
createTime: 2026/11/15
---

# 棘盾

<span class="bs-tag" style="color:#eb507e;border-color:#eb507e">史诗</span> · 最高 **Lv.3** · 内部 ID <code>barb</code>

> 举盾格挡近战攻击时反弹伤害给攻击者

## 基本信息

| 项目 | 内容 |
| --- | --- |
| 适用物品 | 盾牌 |
| 冲突附魔组 | — |
| 互斥附魔 | — |
| 每级效果预览 | `&7举盾格挡近战攻击时反弹&a{反弹伤害}&7给攻击者` |
| 监听机制 | `on-damaged` ← entity-damaged-by-other |

## 数值参数

| 属性 | 单位 | 表达式 / 取值 |
| --- | --- | --- |
| 反弹伤害 | 点 | `2+1*{level}` |

> [!note] 表达式说明
> 公式中的 `{level}` 为附魔等级。除常数项外，其余数值随等级线性变化。
