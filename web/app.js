/* 白熊附魔大全 · BrightSky —— 纯静态查询页（无框架、无构建） */
(() => {
  'use strict';

  const $ = (id) => document.getElementById(id);
  const RANK = { '普通': 0, '罕见': 1, '精良': 2, '史诗': 3, '传奇': 4, '稀世': 5, '诅咒': 6, '皮肤': 7 };

  const st = {
    data: null,
    q: '',
    targets: new Set(),
    rarities: new Set(),
    srcs: new Set(),
    sort: 'rarity',
    openId: null,
  };

  /* ---------------- URL 同步 ---------------- */
  function readUrl() {
    const p = new URLSearchParams(location.search);
    st.q = p.get('q') || '';
    st.targets = new Set((p.get('t') || '').split(',').filter(Boolean));
    st.rarities = new Set((p.get('r') || '').split(',').filter(Boolean));
    st.srcs = new Set((p.get('s') || '').split(',').filter(Boolean));
    st.sort = p.get('sort') || 'rarity';
    st.openId = p.get('id') || null;
  }

  function writeUrl(push) {
    const p = new URLSearchParams();
    if (st.q) p.set('q', st.q);
    if (st.targets.size) p.set('t', [...st.targets].join(','));
    if (st.rarities.size) p.set('r', [...st.rarities].join(','));
    if (st.srcs.size) p.set('s', [...st.srcs].join(','));
    if (st.sort !== 'rarity') p.set('sort', st.sort);
    if (st.openId) p.set('id', st.openId);
    const url = location.pathname + (p.toString() ? '?' + p : '');
    history[push ? 'pushState' : 'replaceState']({}, '', url);
  }

  /* ---------------- 过滤 ---------------- */
  function match(it) {
    if (st.targets.size && !it.tg.some((t) => st.targets.has(t))) return false;
    if (st.rarities.size && !st.rarities.has(it.rarity)) return false;
    if (st.srcs.size && !st.srcs.has(it.src)) return false;
    if (st.q) {
      const toks = st.q.toLowerCase().split(/\s+/).filter(Boolean);
      for (const t of toks) if (!it.s.includes(t)) return false;
    }
    return true;
  }

  function sortItems(arr) {
    const by = st.sort;
    return arr.sort((a, b) => {
      if (by === 'name') return a.name.localeCompare(b.name, 'zh-CN');
      if (by === 'level') return (b.lv || 0) - (a.lv || 0) || a.name.localeCompare(b.name, 'zh-CN');
      if (by === 'src') return a.srcLabel.localeCompare(b.srcLabel) || (RANK[a.rarity] ?? 9) - (RANK[b.rarity] ?? 9);
      return (RANK[b.rarity] ?? 9) - (RANK[a.rarity] ?? 9) || (b.lv || 0) - (a.lv || 0) || a.name.localeCompare(b.name, 'zh-CN');
    });
  }

  /* ---------------- 渲染：筛选条 ---------------- */
  function chip(label, count, pressed, onClick, dot) {
    const b = document.createElement('button');
    b.className = 'chip';
    b.type = 'button';
    b.setAttribute('aria-pressed', pressed ? 'true' : 'false');
    if (dot) {
      const d = document.createElement('span');
      d.className = 'chip-dot';
      d.style.background = dot;
      b.appendChild(d);
    }
    b.appendChild(document.createTextNode(label));
    const n = document.createElement('span');
    n.className = 'n';
    n.textContent = count;
    b.appendChild(n);
    b.addEventListener('click', onClick);
    return b;
  }

  function renderChips() {
    // 物品
    const tBox = $('chipsTarget');
    tBox.textContent = '';
    tBox.appendChild(chip('全部', st.data.meta.total, st.targets.size === 0, () => {
      st.targets.clear(); apply();
    }));
    for (const t of st.data.targets.filter((x) => x.count >= 3)) {
      tBox.appendChild(chip(t.emoji + ' ' + t.cn, t.count, st.targets.has(t.cn), () => {
        st.targets.has(t.cn) ? st.targets.delete(t.cn) : st.targets.add(t.cn);
        apply();
      }));
    }
    // 品质
    const rBox = $('chipsRarity');
    rBox.textContent = '';
    rBox.appendChild(chip('全部', st.data.meta.total, st.rarities.size === 0, () => {
      st.rarities.clear(); apply();
    }));
    for (const r of st.data.rarities) {
      rBox.appendChild(chip(r.cn, r.count, st.rarities.has(r.cn), () => {
        st.rarities.has(r.cn) ? st.rarities.delete(r.cn) : st.rarities.add(r.cn);
        apply();
      }, r.hex));
    }
    // 来源
    const sBox = $('chipsSrc');
    sBox.textContent = '';
    sBox.appendChild(chip('全部', st.data.meta.total, st.srcs.size === 0, () => {
      st.srcs.clear(); apply();
    }));
    for (const k of ['aiya', 'nereus']) {
      const label = k === 'aiya' ? 'Aiyatsbus' : 'NereusOpus';
      const n = st.data.meta.counts[label] || 0;
      sBox.appendChild(chip(label, n, st.srcs.has(k), () => {
        st.srcs.has(k) ? st.srcs.delete(k) : st.srcs.add(k);
        apply();
      }));
    }
  }

  /* ---------------- 渲染：列表 ---------------- */
  function card(it) {
    const el = document.createElement('article');
    el.className = 'card';
    el.style.setProperty('--rc', it.rc);
    el.tabIndex = 0;
    el.setAttribute('role', 'button');
    el.setAttribute('aria-label', it.name + ' ' + it.rarity);

    const h = document.createElement('div');
    h.className = 'card-h';
    const nm = document.createElement('span');
    nm.className = 'card-n';
    nm.textContent = it.name;
    const bd = document.createElement('span');
    bd.className = 'badge';
    bd.textContent = it.rarity;
    const lv = document.createElement('span');
    lv.className = 'card-lv';
    lv.textContent = it.lv ? 'Lv.' + it.lv : '';
    h.append(nm, bd, lv);

    const d = document.createElement('div');
    d.className = 'card-d';
    d.textContent = it.desc || '（无说明）';

    const f = document.createElement('div');
    f.className = 'card-f';
    for (const t of it.tg.slice(0, 4)) {
      const s = document.createElement('span');
      s.className = 'tg';
      s.textContent = t;
      f.appendChild(s);
    }
    const src = document.createElement('span');
    src.className = 'src';
    src.textContent = it.kindLabel + ' · ' + it.srcLabel;
    f.appendChild(src);

    el.append(h, d, f);
    el.addEventListener('click', () => openDetail(it.id, true));
    el.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openDetail(it.id, true); }
    });
    return el;
  }

  function render() {
    const all = st.data.items;
    const hits = all.filter(match);
    sortItems(hits);

    const list = $('list');
    list.textContent = '';
    const frag = document.createDocumentFragment();
    for (const it of hits) frag.appendChild(card(it));
    list.appendChild(frag);

    $('empty').hidden = hits.length > 0;
    $('resCount').innerHTML = '找到 <b>' + hits.length + '</b> 个附魔'
      + (hits.length !== all.length ? '（共 ' + all.length + ' 个）' : '');
    const active = st.targets.size + st.rarities.size + st.srcs.size + (st.q ? 1 : 0);
    $('hdStat').innerHTML = active
      ? '筛选中 · <b>' + hits.length + '</b> / ' + all.length
      : '共 <b>' + all.length + '</b> 个附魔 · ' + st.data.meta.counts.Aiyatsbus + ' + ' + st.data.meta.counts.NereusOpus;
  }

  /* ---------------- 详情 ---------------- */
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  }

  // 参数标签：中文名与英文键相同时只显示一行，避免「宽度下限 / 宽度下限」这种重复叠字
  function lblCell(p) {
    const k = String(p.k || '');
    const cn = String(p.cn || '');
    if (!cn || cn === k) return esc(k);
    return `${esc(cn)}<br><code>${esc(k)}</code>`;
  }

  // 互斥/前置里能定位到本页条目的，渲染成可点的链接（点一下直接看那件附魔）
  function linkList(names, ids, self_id) {
    return names.map((n, i) => {
      const id = (ids || [])[i];
      if (id && id !== self_id && st.data.items.some((x) => x.id === id))
        return `<a class="d-link" href="?id=${encodeURIComponent(id)}" data-jump="${esc(id)}">${esc(n)}</a>`;
      return `<span class="d-plain">${esc(n)}</span>`;
    }).join('、');
  }

  function openDetail(id, push) {
    const it = st.data.items.find((x) => x.id === id);
    if (!it) return;
    st.openId = id;
    writeUrl(push !== false);

    const box = $('drawerBody');
    const params = it.params || [];
    box.innerHTML = `
      <div class="d-en">${esc(it.en || '')}${it.en ? ' · ' : ''}${esc(it.srcLabel)} · ${esc(it.kindLabel)}</div>
      <div class="d-meta">
        <span class="badge" style="--rc:${it.rc}">${esc(it.rarity)}</span>
        <span class="tg">最高 ${it.lv || '?'} 级</span>
        ${it.gs ? '<span class="tg">磨石可移除</span>' : '<span class="tg">磨石不可移除</span>'}
        ${it.perm ? `<span class="tg">权限 ${esc(it.perm)}</span>` : ''}
      </div>
      <div class="d-sec"><h4>效果</h4><div class="d-desc">${it.descHtml || esc(it.desc) || '（无说明）'}</div></div>
      <div class="d-sec"><h4>可附在</h4><div class="d-tg">${(it.tg.length ? it.tg : ['（未标注）']).map((t) => `<span>${esc(t)}</span>`).join('')}</div></div>
      ${params.length ? `<div class="d-sec"><h4>数值参数</h4><table class="kv">${params.map((p) => `<tr><td>${lblCell(p)}</td><td><code>${esc(p.v)}</code></td></tr>`).join('')}</table></div>` : ''}
      ${it.conflicts.length || it.groups.length || it.need.length ? `<div class="d-sec"><h4>冲突与前置</h4><table class="kv">
        ${it.conflicts.length ? `<tr><td>互斥附魔</td><td>${linkList(it.conflicts, it.conflictsId, it.id)}</td></tr>` : ''}
        ${it.groups.length ? `<tr><td>互斥分组</td><td>${it.groups.map(esc).join('、')}</td></tr>` : ''}
        ${it.need.length ? `<tr><td>需要先有</td><td>${linkList(it.need, it.needId, it.id)}</td></tr>` : ''}
      </table></div>` : ''}
      ${it.listeners.length ? `<div class="d-sec"><h4>触发时机</h4><div class="d-tg">${it.listeners.map((l) => `<span>${esc(l)}</span>`).join('')}</div></div>` : ''}
      <div class="d-sec"><h4>内部 ID</h4>
        <div class="idrow"><code>${esc(it.id)}</code><button class="copy" data-copy="${esc(it.id)}">复制</button></div>
        <p class="note">用于 /enchant 或插件命令中指定该附魔。</p>
      </div>`;

    $('drawerTtl').textContent = it.name || '';
    // 锁定背景滚动，并补上滚动条宽度，避免打开瞬间整页横向跳动
    const sbw = window.innerWidth - document.documentElement.clientWidth;
    document.body.style.overflow = 'hidden';
    if (sbw > 0) document.body.style.paddingRight = sbw + 'px';
    $('drawer').hidden = false;
    $('drawerScroll').scrollTop = 0;
    $('drawerX').focus({ preventScroll: true });

    const cp = box.querySelector('.copy');
    if (cp) cp.addEventListener('click', async () => {
      try { await navigator.clipboard.writeText(it.id); cp.textContent = '已复制'; setTimeout(() => (cp.textContent = '复制'), 1200); }
      catch { cp.textContent = '复制失败'; }
    });

    box.querySelectorAll('a[data-jump]').forEach((a) => {
      a.addEventListener('click', (e) => {
        e.preventDefault();
        openDetail(a.getAttribute('data-jump'));
      });
    });
  }

  function closeDetail(push) {
    st.openId = null;
    $('drawer').hidden = true;
    document.body.style.overflow = '';
    document.body.style.paddingRight = '';
    writeUrl(push !== false);
  }

  /* ---------------- 主流程 ---------------- */
  function apply() {
    renderChips();
    render();
    writeUrl(false);
  }

  async function init() {
    const res = await fetch('data.json', { cache: 'no-cache' });
    st.data = await res.json();
    readUrl();

    $('q').value = st.q;
    $('sort').value = st.sort;
    $('clear').hidden = !st.q;

    $('q').addEventListener('input', (e) => {
      st.q = e.target.value.trim();
      $('clear').hidden = !st.q;
      render();
      writeUrl(false);
    });
    $('clear').addEventListener('click', () => {
      st.q = ''; $('q').value = ''; $('clear').hidden = true; render(); writeUrl(false); $('q').focus();
    });
    $('sort').addEventListener('change', (e) => { st.sort = e.target.value; render(); writeUrl(false); });
    $('reset').addEventListener('click', () => {
      st.q = ''; st.targets.clear(); st.rarities.clear(); st.srcs.clear(); st.sort = 'rarity';
      $('q').value = ''; $('sort').value = 'rarity'; $('clear').hidden = true;
      apply();
    });
    $('drawerX').addEventListener('click', () => closeDetail(true));
    $('drawerBd').addEventListener('click', () => closeDetail(true));

    document.addEventListener('keydown', (e) => {
      if (e.key === '/' && document.activeElement !== $('q')) { e.preventDefault(); $('q').focus(); }
      if (e.key === 'Escape') {
        if (!$('drawer').hidden) closeDetail(true);
        else if (document.activeElement === $('q')) $('q').blur();
      }
    });

    window.addEventListener('popstate', () => {
      readUrl();
      $('q').value = st.q;
      $('sort').value = st.sort;
      $('clear').hidden = !st.q;
      renderChips(); render();
      if (st.openId) openDetail(st.openId, false); else { $('drawer').hidden = true; document.body.style.overflow = ''; }
    });

    apply();
    if (st.openId) openDetail(st.openId, false);
  }

  init();
})();
