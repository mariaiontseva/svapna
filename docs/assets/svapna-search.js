/* ============================================================
   svapna · search + catalog
   loads data.json (311 texts) + search_index.json (pre-indexed terms)
   ============================================================ */

(function(){

  const DATA_URL  = '../data.json';
  const INDEX_URL = '../search_index.json';

  // pre-indexed terms we know about (used for quick-buttons + snippet search)
  const INDEXED_TERMS = ['svapna','nidrā','jāgrat','suṣupti','turīya'];

  let DATA  = null;   // full data.json
  let INDEX = null;   // full search_index.json
  let STATE = { term: '', tradition: '', period: '', author: '' };

  const esc = s => String(s||'').replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));

  // ---------- init ----------
  Promise.all([
    fetch(DATA_URL).then(r => r.json()),
    fetch(INDEX_URL).then(r => r.json()).catch(() => ({}))
  ]).then(([data, index]) => {
    DATA = data;
    INDEX = index;
    populateFilters();
    wireEvents();
    render();
    updateHeaderStats();
  }).catch(err => {
    console.error('svapna-search: load failed', err);
    const el = document.getElementById('search-results');
    if(el) el.innerHTML = `<div class="empty-state"><b>Failed to load data</b><br><small style="font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase">check console — ${esc(err.message)}</small></div>`;
  });

  // ---------- header stats (uses data-count attrs) ----------
  function updateHeaderStats(){
    if(!DATA) return;
    const s = DATA.stats || {};
    document.querySelectorAll('[data-count="texts"]').forEach(el => el.textContent = s.total_texts || '—');
    document.querySelectorAll('[data-count="sources"]').forEach(el => el.textContent = s.unique_sources || '—');
    document.querySelectorAll('[data-count="matches"]').forEach(el => el.textContent = (s.svapna_matches || 0).toLocaleString());
    document.querySelectorAll('[data-count="svapna-texts"]').forEach(el => el.textContent = s.svapna_texts || '—');
  }

  // ---------- populate filter selects ----------
  function populateFilters(){
    const f = (DATA && DATA.filters) || {};
    fillSelect('#f-tradition', 'All traditions', f.traditions || []);
    fillSelect('#f-period',    'All periods',    f.periods    || []);
    fillSelect('#f-author',    'All authors',    f.authors    || []);
  }
  function fillSelect(sel, allLabel, items){
    const el = document.querySelector(sel);
    if(!el) return;
    el.innerHTML = `<option value="">${allLabel}</option>` +
      items.map(i => `<option value="${esc(i)}">${esc(i)}</option>`).join('');
  }

  // ---------- wire events ----------
  function wireEvents(){
    const form = document.getElementById('search-form');
    const input = document.getElementById('search-input');
    const tradSel = document.querySelector('#f-tradition');
    const perSel  = document.querySelector('#f-period');
    const authSel = document.querySelector('#f-author');

    if(form) form.addEventListener('submit', e => { e.preventDefault(); STATE.term = (input.value || '').trim(); syncTermButtons(); render(); });
    if(tradSel) tradSel.addEventListener('change', () => { STATE.tradition = tradSel.value; render(); });
    if(perSel)  perSel.addEventListener('change',  () => { STATE.period = perSel.value; render(); });
    if(authSel) authSel.addEventListener('change', () => { STATE.author = authSel.value; render(); });

    document.querySelectorAll('.quick-terms button[data-term]').forEach(btn => {
      btn.addEventListener('click', () => {
        const t = btn.dataset.term;
        STATE.term = STATE.term === t ? '' : t;
        if(input) input.value = STATE.term;
        syncTermButtons();
        render();
      });
    });

    const clearBtn = document.getElementById('clear-filters');
    if(clearBtn) clearBtn.addEventListener('click', () => {
      STATE = { term:'', tradition:'', period:'', author:'' };
      if(input) input.value = '';
      if(tradSel) tradSel.value = '';
      if(perSel)  perSel.value  = '';
      if(authSel) authSel.value = '';
      syncTermButtons();
      render();
    });
  }

  function syncTermButtons(){
    document.querySelectorAll('.quick-terms button[data-term]').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.term === STATE.term);
    });
  }

  // ---------- rendering ----------
  function highlight(text, term){
    if(!term) return esc(text);
    const safe = esc(text);
    const re = new RegExp('(' + term.replace(/[.*+?^${}()|[\]\\]/g,'\\$&') + ')', 'gi');
    return safe.replace(re, '<mark>$1</mark>');
  }

  function matchesFilters(item){
    if(STATE.tradition && item.tradition !== STATE.tradition) return false;
    if(STATE.period    && item.period    !== STATE.period)    return false;
    if(STATE.author    && item.author    !== STATE.author)    return false;
    return true;
  }

  function render(){
    const out = document.getElementById('search-results');
    const summary = document.getElementById('result-summary');
    if(!out || !DATA) return;

    const term = STATE.term;
    let items = [];
    let mode = 'catalog';

    if(term && INDEX && INDEX[term]){
      // pre-indexed term → show results with snippets
      mode = 'indexed';
      items = INDEX[term].results.filter(matchesFilters);
    } else if(term){
      // fallback: substring match on display_name / author / tradition
      mode = 'metadata';
      const t = term.toLowerCase();
      items = (DATA.texts || []).filter(matchesFilters).filter(tx => {
        const hay = [tx.display_name, tx.author, tx.tradition, tx.filename].join(' ').toLowerCase();
        return hay.includes(t);
      });
    } else {
      // no term → filtered catalog
      items = (DATA.texts || []).filter(matchesFilters);
      // sort by svapna_count desc by default when browsing catalog
      items = items.slice().sort((a,b) => (b.svapna_count||0) - (a.svapna_count||0));
    }

    // summary
    if(summary){
      let left = '';
      if(term && mode === 'indexed'){
        left = `<b>${items.length}</b> texts containing <b style="font-style:italic;font-family:var(--serif);font-size:13px;letter-spacing:0;text-transform:none">${esc(term)}</b>`;
      } else if(term){
        left = `<b>${items.length}</b> metadata matches for “${esc(term)}”`;
      } else {
        left = `<b>${items.length}</b> of <b>${(DATA.stats||{}).total_texts || '—'}</b> texts`;
      }
      const filterCount = [STATE.tradition, STATE.period, STATE.author].filter(Boolean).length;
      const filters = filterCount ? ` · filtered by <b>${filterCount}</b>` : '';
      const sortLabel = term ? 'sorted by matches' : 'sorted by svapna count';
      summary.innerHTML = `<div>${left}${filters}</div><div class="sort">${sortLabel}</div>`;
    }

    // results
    if(!items.length){
      out.innerHTML = `<div class="empty-state">Nothing matches these filters.<br><b>Try clearing them above.</b></div>`;
      return;
    }

    out.innerHTML = items.slice(0, 200).map(item => renderResult(item, term, mode)).join('');
  }

  function renderResult(item, term, mode){
    const name = item.display_name || item.filename || '—';
    const tradition = item.tradition || '—';
    const period = item.period || '—';
    const author = item.author || 'Unknown';
    const count = item.svapna_count !== undefined ? item.svapna_count : (item.count || null);

    const snippets = (mode === 'indexed' && item.snippets)
      ? item.snippets.slice(0, 3).map(s => `<div class="snippet">${highlight(s, term)}</div>`).join('')
      : '';

    const countBlock = count !== null
      ? `<div class="count">${count}</div><span class="count-label">svapna hits</span>`
      : '';

    return `
      <article class="result">
        <div class="main">
          <div class="title"><em>${esc(name)}</em></div>
          <div class="meta">
            <span><b>${esc(tradition)}</b></span>
            <span class="sep">·</span>
            <span>${esc(period)}</span>
            <span class="sep">·</span>
            <span>${esc(author)}</span>
          </div>
          ${snippets ? `<div class="snippets">${snippets}</div>` : ''}
        </div>
        <div class="aside">${countBlock}</div>
      </article>
    `;
  }

})();
