/* ============================================================
   svapna · passage + traditions tree renderer
   uses existing data: kamika_agama_passages, all_saiva_passages
   ============================================================ */

(function(){

  // ---------- category metadata ----------
  const CAT = {
    revelation:             { label:'Revelation',    roman:'I',   color:'teal'   },
    empowerment:            { label:'Empowerment',   roman:'II',  color:'amber'  },
    magic:                  { label:'Dream Magic',   roman:'III', color:'rose'   },
    'yoga&consciousness':   { label:'Consciousness', roman:'IV',  color:'indigo' },
    yoga:                   { label:'Consciousness', roman:'IV',  color:'indigo' },
    consciousness:          { label:'Consciousness', roman:'IV',  color:'indigo' },
    omens:                  { label:'Omens',         roman:'V',   color:'slate'  }
  };

  // for the left border accent: primary category determines colour
  const PRIMARY = ['revelation','empowerment','magic','yoga&consciousness','yoga','consciousness','omens'];
  const CAT_CLASS = {
    revelation:'has-revelation', empowerment:'has-empowerment',
    magic:'has-magic', 'yoga&consciousness':'has-consciousness',
    yoga:'has-consciousness', consciousness:'has-consciousness',
    omens:'has-omens'
  };

  const esc = s => String(s||'').replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));

  // ---------- render one passage ----------
  function renderPassage(p){
    const cats = (p.categories || []).filter(c => CAT[c]);
    const primaryCat = PRIMARY.find(c => cats.includes(c));
    const leftClass = primaryCat ? (CAT_CLASS[primaryCat] || '') : '';

    const tags = cats.map(c => {
      const m = CAT[c];
      return `<span class="cat-tag tag-${m.color}">${m.roman} · ${m.label}</span>`;
    }).join('');

    const translator = p.translated && p.translator
      ? `<span class="translator-badge">tr. ${esc(p.translator)}</span>`
      : (p.translator
          ? `<span class="translator-badge">tr. ${esc(p.translator)}</span>`
          : `<span class="translator-badge untranslated">untranslated</span>`);

    const verses = (p.verses || []).map(v => {
      const num = v.number ? `<div class="verse-num">${esc(v.number)}</div>` : `<div class="verse-num"></div>`;
      const skt = v.sanskrit ? `<div class="verse-skt">${esc(v.sanskrit)}</div>` : '';
      const tr  = v.translation ? `<div class="verse-tr">${esc(v.translation)}</div>` : '';
      return `${num}<div>${skt}${tr}</div>`;
    }).join('');

    const context = p.context
      ? `<p class="passage-context">${esc(p.context)}</p>`
      : '';

    return `
      <article class="passage ${leftClass}">
        <header class="passage-head">
          <div class="passage-ref">${esc(p.reference || '—')}</div>
          <div class="passage-tags">${tags}${translator}</div>
        </header>
        <div class="verses">${verses}</div>
        ${context}
      </article>
    `;
  }

  // ---------- render one text entry ----------
  function renderText(key, text){
    const passages = Object.values(text.passages || {})
      .map(renderPassage)
      .join('');
    return `
      <section class="text-entry" id="${esc(key)}">
        <header class="text-head">
          <div class="text-branch">${esc(text.branch || '')}</div>
          <h3 class="text-name"><em>${esc(text.name || key)}</em></h3>
          <div class="text-period">${esc(text.period || '')}</div>
        </header>
        <div class="passages">${passages}</div>
      </section>
    `;
  }

  // ---------- group texts by top-level branch ----------
  const GROUPS = [
    { id:'siddhanta', title:'Śaiva Siddhānta', sub:'The canonical Śaiva Āgamas — foundations of mainstream tantric ritual',
      match: b => /Siddhānta/i.test(b) },
    { id:'mantrapitha', title:'Mantrapīṭha — Early Bhairava Tantras', sub:'The Bhairava-stream texts, cult of wrathful Śiva, ninth-century Kashmirian core',
      match: b => /Mantrapīṭha/i.test(b) },
    { id:'vidyapitha', title:'Vidyāpīṭha — Yāmala, Trika, Krama', sub:'The goddess-centred stream: Yāmala-tantras, Trika triads, Krama sequences',
      match: b => /Vidyāpīṭha/i.test(b) },
    { id:'kaula', title:'Kaula — The Four Āmnāyas', sub:'The reformed transmissions — Pūrva, Paścima, Uttara, Dakṣiṇa',
      match: b => /Kaula|Āmnāya|āmnāya|amnāya/i.test(b) },
    { id:'kashmir', title:'Kashmir Śaivism — Exegetical tradition', sub:'Non-dual Kashmirian philosophy: Spanda, Pratyabhijñā, the Śivasūtra commentators',
      match: b => /Kashmir/i.test(b) },
    { id:'late', title:'Late Syncretic Śākta', sub:'Assam, Bengal, Mahāvidyā compilations — the long tail of the tradition',
      match: b => /Late Syncretic|Bengal|Assam|Mahāvidyā/i.test(b) }
  ];

  function groupTexts(data){
    const buckets = Object.fromEntries(GROUPS.map(g => [g.id, []]));
    buckets._other = [];
    for(const [key, text] of Object.entries(data)){
      const branch = text.branch || '';
      const g = GROUPS.find(g => g.match(branch));
      if(g) buckets[g.id].push([key, text]);
      else  buckets._other.push([key, text]);
    }
    return buckets;
  }

  // ---------- render everything into #traditions-content ----------
  function renderAll(){
    const container = document.getElementById('traditions-content');
    if(!container) return;
    if(typeof all_saiva_passages === 'undefined'){
      container.innerHTML = '<div class="loading">failed to load passage data — check console</div>';
      return;
    }

    const buckets = groupTexts(all_saiva_passages);

    const html = GROUPS.map(g => {
      const texts = buckets[g.id];
      if(!texts.length) return '';
      return `
        <section class="tradition-group" id="group-${g.id}">
          <div class="group-title">${esc(g.title)}</div>
          <div class="group-subtitle">${esc(g.sub)}</div>
          ${texts.map(([k,t]) => renderText(k,t)).join('')}
        </section>
      `;
    }).join('');

    const other = buckets._other.length
      ? `<section class="tradition-group"><div class="group-title">Other</div>${buckets._other.map(([k,t]) => renderText(k,t)).join('')}</section>`
      : '';

    container.innerHTML = html + other;

    // count texts and passages for any counter elements
    const textCount = Object.keys(all_saiva_passages).length;
    let passageCount = 0;
    Object.values(all_saiva_passages).forEach(t => {
      passageCount += Object.keys(t.passages || {}).length;
    });
    document.querySelectorAll('[data-count="texts"]').forEach(el => el.textContent = textCount);
    document.querySelectorAll('[data-count="passages"]').forEach(el => el.textContent = passageCount);
  }

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', renderAll);
  } else {
    renderAll();
  }

})();
