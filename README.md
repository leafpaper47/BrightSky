# 白熊附魔大全 · BrightSky

> Aiyatsbus 与 NereusOpus 的**附魔查询页**——打开就能搜，按物品反查，点开看完整数值。

站点地址：**https://leafpaper47.github.io/BrightSky/**

<img src="web/logo.png" width="110" alt="BrightSky">

## 为什么不是文档站

文档站要一层层点进分类页才能找到一个附魔，玩家实际只想问两件事：

1. 「**这件附魔是干嘛的？**」→ 顶部搜索框，输入名字或效果关键词即可（支持中文名 / 英文 ID / 参数名，如 `掉落`、`cooldown`）。
2. 「**我这把剑/这张弓能附什么？**」→ 点「穿在」里的物品标签，立刻只剩该物品可用的附魔。

其余按需出现：品质筛选、来源筛选（Aiyatsbus / NereusOpus）、按品质或等级排序、卡片点开看参数表与互斥关系。

## 功能

- **即时搜索**：多关键词 AND，例如 `剑 爆炸` 同时命中「可附在剑上」且说明里有「爆炸」的附魔。
- **物品反查**：剑 77、弓 57、斧 52、靴子 47、头盔 38、弩 38、三叉戟 34……
- **品质筛选**：普通 / 罕见 / 精良 / 史诗 / 传奇 / 稀世 / 诅咒，带各自颜色。
- **详情面板**：效果原文、可附物品、数值参数（英文键 + 中文名）、互斥附魔与分组、需要先有的附魔、触发时机、内部 ID（一键复制）。
- **可分享链接**：搜索词与筛选条件都写进 URL，例如
  `?q=爆炸&t=剑` 或 `?id=tremor` 直接打开某件附魔。
- **手机优先**：卡片自适应列数，详情在手机上是从底部弹出的面板，支持深/浅色跟随系统。
- 快捷键：`/` 聚焦搜索，`Esc` 关闭详情。

## 收录

| 分类 | 数量 | 来源 |
| --- | --- | --- |
| 原版附魔 | 45 | Aiyatsbus `enchants/Packet-Vanilla/` |
| 自定义附魔 | 15 | Aiyatsbus `enchants/Packet-Default/` |
| 技能（主动） | 12 | NereusOpus `enchantments/skill/` |
| 被动附魔 | 172 | NereusOpus `enchantments/simple/` |
| 诅咒 | 9 | NereusOpus `enchantments/curse/` |
| **合计** | **253** | |

## 目录

```
.
├── extract.py       # 两个插件 jar 的 YAML → data/enchants.json
├── build_app.py     # data/enchants.json → web/data.json（扁平化 + 搜索索引 + 中文标签）
├── raw/             # 从 jar 解出的原始配置（aiya 83 个 / nereus 197 个）
├── data/            # 中间产物
└── web/             # 站点本体（纯静态，无构建步骤）
    ├── index.html
    ├── app.js       # 搜索 / 筛选 / 详情，原生 JS
    ├── style.css
    └── data.json
```

## 更新数据

```bash
python extract.py      # 需要 PyYAML
python build_app.py
git add -A && git commit -m "data: 同步插件配置" && git push
```

推送到 `main` 即触发 `.github/workflows/deploy.yml`（纯静态发布，无 Node 构建）。

本地预览（`fetch` 需要 http，不能直接双击 html）：

```bash
cd web && python -m http.server 8080
# 打开 http://127.0.0.1:8080/
```

## 数据说明

- 全部来自两个插件的**默认配置**，数值原样保留（`4+level*2` 表示按等级线性成长）。
- 原版附魔的效果由客户端/服务端原版逻辑实现，插件只接管名称、品质、适用物品与冲突。
- NereusOpus 的 `unknown` 档实际中文是「稀世」（不是「未知品质」），已与 Aiyatsbus 的 `splendid` 合并为同一档。
- 「皮肤（artifact）」档在两个插件里都标记为不可获得，一般不出现在正常流程中。

## 致谢

附魔数据：Aiyatsbus、NereusOpus 作者；图标素材来自白熊「涅柔斯之作」。
