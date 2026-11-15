# 白熊附魔大全 · BrightSky

> Aiyatsbus 与 NereusOpus 两个附魔插件的**完整附魔速查手册**，从插件默认配置自动生成。

站点地址：**https://leafpaper47.github.io/BrightSky/**

<img src="site/docs/.vuepress/public/logo.png" width="120" alt="BrightSky">

## 收录内容

| 分类 | 数量 | 来源 |
| --- | --- | --- |
| 原版附魔 | 45 | Aiyatsbus `enchants/Packet-Vanilla/` |
| 自定义附魔 | 15 | Aiyatsbus `enchants/Packet-Default/` |
| 技能附魔（主动） | 12 | NereusOpus `enchantments/skill/` |
| 普通附魔 | 172 | NereusOpus `enchantments/simple/` |
| 诅咒附魔 | 9 | NereusOpus `enchantments/curse/` |
| **合计** | **253** | |

每个附魔都给出：中文名 / 内部 ID / 品质（含颜色）/ 最高等级 / 适用物品 / 互斥与前置 / 说明 / 数值参数（英文键与中文说明并列）。

另外附两张对照表：

- `ref/rarity` —— 两个插件各自的品质名称、颜色码与权重（注意两套档位并不完全同名）
- `ref/targets` —— 英文部位键（swords、bow…）与中文物品名对照

## 目录结构

```
.
├── extract.py          # 解析 raw/ 下的插件配置 → data/enchants.json
├── gen_docs.py         # data/enchants.json → site/docs/**/*.md + 侧边栏
├── raw/                # 从两个插件 jar 解出的原始 YAML（aiya 83 个 / nereus 197 个）
│   ├── aiya/enchants/
│   └── nereus/enchantments/
├── data/enchants.json  # 归一化后的附魔数据（生成物，已入库便于对比）
└── site/               # VuePress 2 + vuepress-theme-plume 站点
    └── docs/
```

## 本地构建

```bash
# 1) 生成数据与页面（需要 python + PyYAML）
python extract.py
python gen_docs.py

# 2) 构建站点
cd site
pnpm install
pnpm dev      # 本地预览 http://127.0.0.1:8088/BrightSky/
pnpm build    # 产物在 docs/.vuepress/dist
```

## 发布

推送到 `main` 分支即触发 `.github/workflows/deploy.yml`：pnpm 9 + Node 22 构建 → `actions/deploy-pages@v4` 发布到 GitHub Pages。

首次使用需在仓库 **Settings → Pages → Source** 选择 **GitHub Actions**。

> 站点 `base` 固定为 `/BrightSky/`，若改了仓库名，记得同步修改 `site/docs/.vuepress/config.ts` 的 `BASE` 与 `HOSTNAME`。

## 数据说明

- 数据全部来自两个插件的**默认配置**，未做主观改动；数值参数保留原样（如 `4+level*2` 表示按等级线性成长）。
- 原版附魔的**效果**仍由 Minecraft 原版实现，Aiyatsbus 只接管名称、品质、适用物品与冲突关系。
- NereusOpus 的 `unknown` 品质键实际对应中文「稀世」（不是「未知品质」），站点已按实际中文名归一。
- 「皮肤（artifact）」档在两个插件里都标记为不可获得（`inaccessible`），一般不会出现在正常游戏流程中。

## 致谢

- 附魔数据：Aiyatsbus、NereusOpus 插件作者
- 站点模板：本项目沿用作者此前 `xingmian-docs` 的 VuePress + Plume 结构
