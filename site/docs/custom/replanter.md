---
title: 再植
createTime: 2026/11/15
---

# 再植

<span class="bs-tag" style="color:#66c18c;border-color:#66c18c">罕见</span> · 最高 **Lv.1** · 内部 ID <code>replanter</code>

> 踩坏耕地时，只会使作物退化而不是掉落

## 基本信息

| 项目 | 内容 |
| --- | --- |
| 适用物品 | 靴子 |
| 冲突附魔组 | — |
| 互斥附魔 | — |
| 每级效果预览 | `&7踩坏耕地时，只会使作物退化&a{退化阶段}` |
| 监听机制 | `on-physical` ← player-interact |

## 数值参数

| 属性 | 单位 | 表达式 / 取值 |
| --- | --- | --- |
| 退化阶段 | 阶段 | `3-{level}` |

> [!note] 表达式说明
> 公式中的 `{level}` 为附魔等级。除常数项外，其余数值随等级线性变化。
