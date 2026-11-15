import type { ThemeNavItem, ThemeSidebarMulti } from 'vuepress-theme-plume'

export const navbar: ThemeNavItem[] = [
  { text: '首页', link: '/' },
  { text: '原版附魔', link: '/vanilla/' },
  { text: '自定义附魔', link: '/custom/' },
  { text: '技能附魔', link: '/skills/' },
  { text: '普通附魔', link: '/simple/' },
  { text: '诅咒附魔', link: '/curse/' },
  { text: '品质对照', link: '/ref/rarity' },
  { text: '物品对照', link: '/ref/targets' },
]

export const sidebar: ThemeSidebarMulti = {
  '/vanilla/': [
    { text: '🪄 附魔总览', link: '/' },
    { text: '原版附魔', link: '/vanilla/' },
  ],
  '/custom/': [
    { text: '🪄 附魔总览', link: '/' },
    { text: '自定义附魔', link: '/custom/' },
    {
      text: '⚔️ Aiyatsbus 自定义附魔',
      link: '/custom/',
      collapsed: false,
      items: [
        { text: "再植", link: '/custom/replanter.md' },
        { text: "弹跳鞋", link: '/custom/jelly_legs.md' },
        { text: "剑气", link: '/custom/sword_beam.md' },
        { text: "推进器", link: '/custom/propulsion.md' },
        { text: "棘盾", link: '/custom/barb.md' },
        { text: "蓄能", link: '/custom/accumulating.md' },
        { text: "匠心", link: '/custom/artisanship.md' },
        { text: "反击", link: '/custom/counter.md' },
        { text: "反重力", link: '/custom/wings.md' },
        { text: "扎刺", link: '/custom/twinge.md' },
        { text: "播种机", link: '/custom/planter.md' },
        { text: "盾冲", link: '/custom/bash.md' },
        { text: "索敌", link: '/custom/aiming.md' },
        { text: "跃动", link: '/custom/bouncy_arrow.md' },
        { text: "震地", link: '/custom/tremor.md' },
      ],
    },
  ],
  '/skills/': [
    { text: '🪄 附魔总览', link: '/' },
    { text: '技能附魔', link: '/skills/' },
    {
      text: '✨ 主动技能',
      link: '/skills/',
      collapsed: false,
      items: [
        { text: "浇灌", link: '/skills/irrigate.md' },
        { text: "突袭", link: '/skills/charge.md' },
        { text: "腾空", link: '/skills/ascend.md' },
        { text: "爆破", link: '/skills/dynamite.md' },
        { text: "背水", link: '/skills/stand_and_fight.md' },
        { text: "自我", link: '/skills/self_realization.md' },
        { text: "触怒", link: '/skills/quake.md' },
        { text: "假寐", link: '/skills/catnap.md' },
        { text: "急救", link: '/skills/vitalize.md' },
        { text: "咒怨", link: '/skills/missile.md' },
        { text: "回溯", link: '/skills/flash_back.md' },
        { text: "慧眼", link: '/skills/xray.md' },
      ],
    },
  ],
  '/simple/': [
    { text: '🪄 附魔总览', link: '/' },
    { text: '普通附魔', link: '/simple/' },
    {
      text: '📚 按品质浏览',
      link: '/simple/',
      collapsed: false,
      items: [
        { text: "普通（19）", link: '/simple/common.md' },
        { text: "罕见（29）", link: '/simple/uncommon.md' },
        { text: "精良（59）", link: '/simple/rare.md' },
        { text: "史诗（39）", link: '/simple/epic.md' },
        { text: "传奇（19）", link: '/simple/legendary.md' },
        { text: "稀世（7）", link: '/simple/unknown.md' },
      ],
    },
  ],
  '/curse/': [
    { text: '🪄 附魔总览', link: '/' },
    { text: '诅咒附魔', link: '/curse/' },
  ],
  '/ref/': [
    { text: '🪄 附魔总览', link: '/' },
    { text: '品质对照', link: '/ref/rarity.md' },
    { text: '适用物品对照', link: '/ref/targets.md' },
  ],
}
