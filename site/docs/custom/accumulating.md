---
title: 蓄能
createTime: 2026/11/15
---

# 蓄能

<span class="bs-tag" style="color:#eb507e;border-color:#eb507e">史诗</span> · 最高 **Lv.1** · 内部 ID <code>accumulating</code>

> 每击杀若干只怪物后，下一次攻击伤害增加

## 基本信息

| 项目 | 内容 |
| --- | --- |
| 适用物品 | 剑、斧 |
| 冲突附魔组 | — |
| 互斥附魔 | — |
| 每级效果预览 | `&7每击杀&a{击杀累计}&7生物后，下一次攻击伤害增加&a{伤害增加百分比}` |
| 监听机制 | `on-damage` ← entity-damage-other、`on-kill` ← entity-death |

## 数值参数

| 属性 | 单位 | 表达式 / 取值 |
| --- | --- | --- |
| 击杀累计 | 只 | `4-{level}` |
| 伤害增加百分比 | % | `15.0*{level}` |

> [!note] 表达式说明
> 公式中的 `{level}` 为附魔等级。除常数项外，其余数值随等级线性变化。
