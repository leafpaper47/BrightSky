---
title: 爆破
createTime: 2026/11/15
---

# 爆破 · Dynamite

<span class="bs-tag" style="color:#FF55FF;border-color:#FF55FF">史诗</span> · 最高 **Lv.2** · 内部 ID <code>dynamite</code>

> 右击可大范围破坏方块（冷却时间: 360秒）

## 使用条件

- **适用物品**：镐
- **砂轮可移除**：是

## 参数

| 参数 | 取值 |
| --- | --- |
| 音效 <code>sound</code> | `ENTITY_DRAGON_FIREBALL_EXPLODE` |
| 冷却（秒） <code>cooldown</code> | `360` |
| 每 N 刻 <code>tick-per</code> | `16` |
| 粒子效果 <code>particle</code> | `{"type": "EXPLOSION_HUGE", "amount": 1}` |
| 权限校验 <code>permission-check</code> | `True` |
| 硬度判定 <code>hardness-check</code> | `bedrock,obisidian` |
| 作用范围 <code>range</code> | `1+level` |
