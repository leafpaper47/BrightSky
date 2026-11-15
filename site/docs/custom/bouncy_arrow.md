---
title: 跃动
createTime: 2026/11/15
---

# 跃动

<span class="bs-tag" style="color:#fbda41;border-color:#fbda41">稀世</span> · 最高 **Lv.1** · 内部 ID <code>bouncy_arrow</code>

> 射箭撞方块反弹并有概率分裂

## 基本信息

| 项目 | 内容 |
| --- | --- |
| 适用物品 | 弓、弩 |
| 冲突附魔组 | — |
| 互斥附魔 | — |
| 每级效果预览 | `&7射箭撞方块可反弹最多&a{次数}&7并有&a{概率}&7的概率分裂` |
| 监听机制 | `on-projectile-hit` ← projectile-hit |

## 数值参数

| 属性 | 单位 | 表达式 / 取值 |
| --- | --- | --- |
| 次数 | 次 | `{level}` |
| 速度 | — | `0.5+0.1*{level}` |
| 概率 | % | `20*{level}` |

> [!note] 表达式说明
> 公式中的 `{level}` 为附魔等级。除常数项外，其余数值随等级线性变化。
