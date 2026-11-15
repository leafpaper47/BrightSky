import { defineUserConfig } from 'vuepress'
import { viteBundler } from '@vuepress/bundler-vite'
import { plumeTheme } from 'vuepress-theme-plume'
import { navbar, sidebar } from './sidebar.js'

// GitHub Pages 项目站点路径：https://<用户名>.github.io/<仓库名>/
// 仓库名改了只改这一行（末尾斜杠必须有）
const BASE = '/BrightSky/'
// 站点完整地址，只影响 sitemap/SEO
const HOSTNAME = 'https://leafpaper47.github.io/'

export default defineUserConfig({
  lang: 'zh-CN',
  title: '白熊附魔大全 · BrightSky',
  description: 'Aiyatsbus 与 NereusOpus 附魔速查手册：名称、品质、等级、适用物品与数值参数',
  base: BASE,
  bundler: viteBundler(),
  head: [
    // 站点图标：public/logo.png（由「涅柔斯之作」像素图缩放而来）
    ['link', { rel: 'icon', href: `${BASE}favicon-32.png`, type: 'image/png', sizes: '32x32' }],
    ['link', { rel: 'icon', href: `${BASE}logo.png`, type: 'image/png', sizes: '512x512' }],
    ['link', { rel: 'apple-touch-icon', href: `${BASE}apple-touch-icon.png`, sizes: '180x180' }],
    ['meta', { name: 'theme-color', content: '#22374d' }],
  ],
  theme: plumeTheme({
    // 不要再手动拼 BASE，VuePress 会自动加前缀
    logo: '/logo.png',
    hostname: HOSTNAME,
    navbar,
    sidebar,
    // 「此页内容」大纲必须是 [起始级, 结束级]
    outline: [2, 3],
    search: { provider: 'local' },
    editLink: false,
    // 关掉随机 permalink（保留 title/createTime 注入）
    autoFrontmatter: { permalink: false },
    contributors: false,
    changelog: false,
    lastUpdated: false,
    footer: {
      message: '白熊附魔大全 · BrightSky',
      copyright: '数据由 Aiyatsbus 与 NereusOpus 默认配置自动生成',
    },
    markdown: {
      icon: { provider: 'iconify' },
    },
  }),
})
