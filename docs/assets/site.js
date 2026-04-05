/* ============================================================
   mariaiontseva · svapna.space
   shared site JS — scoped sidebars (SKT, SVAPNA) + drawer
   ============================================================ */

(function(){

  // ---------- compute base URL ----------
  const script = document.currentScript ||
    Array.from(document.scripts).find(s => /assets\/site\.js/.test(s.src));
  const BASE = script
    ? script.src.replace(/assets\/site\.js(\?.*)?$/, '')
    : '';
  const U = p => BASE + p;

  // body attributes drive everything:
  //   data-section : "skt" | "svapna"  (no attribute = no sidebar, e.g. home/about)
  //   data-page    : unique key for the current page, used to mark active item
  const section = document.body.getAttribute('data-section');
  const key = document.body.getAttribute('data-page');

  // ---------- HOME-BACK header reused by both sidebars ----------
  const homeBack = (label, sub) => `
    <div class="sb-brand home-back">
      <a class="home-link" href="${U('index.html')}" aria-label="Back to site home">
        <span class="back-arrow">←</span>
        <div class="mark">${label}</div>
        <div class="sub">${sub}</div>
      </a>
      <button class="sb-close" id="sbClose" aria-label="Close menu">×</button>
    </div>
  `;

  // ============================================================
  //  SKT — sanskrit paradigms sidebar
  // ============================================================
  const SB_SKT = `
    ${homeBack('SKT<em>·</em>', 'sanskrit<br>paradigms')}

    <div class="sb-search">
      <input type="text" placeholder="Search paradigms…" />
    </div>

    <nav class="sb-nav">

      <section class="cat-skt">
        <h3><span class="cat"></span>Nominals · Vowel stems</h3>
        <ul>
          <li class="soon"><span class="nolink"><span><span class="title-lat">a-</span>stems <span class="title-sub">m · n · deva, phala</span></span><span class="tag">soon</span></span></li>
          <li class="soon"><span class="nolink"><span><span class="title-lat">ā-</span>stems <span class="title-sub">f · senā</span></span><span class="tag">soon</span></span></li>
          <li class="soon"><span class="nolink"><span><span class="title-lat">i-, ī-</span>stems <span class="title-sub">agni, nadī</span></span><span class="tag">soon</span></span></li>
          <li class="soon"><span class="nolink"><span><span class="title-lat">u-, ū-</span>stems <span class="title-sub">guru, vadhū</span></span><span class="tag">soon</span></span></li>
          <li class="soon"><span class="nolink"><span><span class="title-lat">ṛ-</span>stems <span class="title-sub">pitṛ, mātṛ</span></span><span class="tag">soon</span></span></li>
        </ul>
      </section>

      <section class="cat-skt">
        <h3><span class="cat"></span>Nominals · Consonant stems</h3>
        <ul>
          <li data-key="skt-s-stems"><a href="${U('skt/s-stems.html')}"><span><span class="title-lat">s-</span>stems <span class="title-sub">tapas ⟷ kṛtsna-tapāḥ</span></span><span class="tag">now</span></a></li>
          <li class="soon"><span class="nolink"><span><span class="title-lat">n-</span>stems <span class="title-sub">rājan, ātman, nāman</span></span><span class="tag">soon</span></span></li>
          <li class="soon"><span class="nolink"><span><span class="title-lat">r-</span>stems <span class="title-sub">pitṛ athematic</span></span><span class="tag">soon</span></span></li>
          <li class="soon"><span class="nolink"><span><span class="title-lat">-vant / -mant</span> <span class="title-sub">bhagavant, hanumant</span></span><span class="tag">soon</span></span></li>
          <li class="soon"><span class="nolink"><span><span class="title-lat">-in</span> stems <span class="title-sub">yogin, hastin</span></span><span class="tag">soon</span></span></li>
          <li class="soon"><span class="nolink"><span>Participles in <span class="title-lat">-at</span> <span class="title-sub">present &amp; future</span></span><span class="tag">soon</span></span></li>
        </ul>
      </section>

      <section class="cat-skt">
        <h3><span class="cat"></span>Pronouns</h3>
        <ul>
          <li class="soon"><span class="nolink"><span>Personal <span class="title-sub">aham, tvam, sa</span></span><span class="tag">soon</span></span></li>
          <li class="soon"><span class="nolink"><span>Demonstratives <span class="title-sub">tad, etad, idam, adas</span></span><span class="tag">soon</span></span></li>
          <li class="soon"><span class="nolink"><span>Relative &amp; Interrogative <span class="title-sub">yad, kim</span></span><span class="tag">soon</span></span></li>
        </ul>
      </section>

      <section class="cat-skt">
        <h3><span class="cat"></span>Verbs · Present system</h3>
        <ul>
          <li class="soon"><span class="nolink"><span>Class I <span class="title-sub">bhū · thematic</span></span><span class="tag">soon</span></span></li>
          <li class="soon"><span class="nolink"><span>Class II <span class="title-sub">ad, as · athematic root</span></span><span class="tag">soon</span></span></li>
          <li class="soon"><span class="nolink"><span>Class III <span class="title-sub">hu, dā · reduplicating</span></span><span class="tag">soon</span></span></li>
          <li class="soon"><span class="nolink"><span>Class IV <span class="title-sub">div · -ya- present</span></span><span class="tag">soon</span></span></li>
          <li class="soon"><span class="nolink"><span>Class V <span class="title-sub">su · -nu-</span></span><span class="tag">soon</span></span></li>
          <li class="soon"><span class="nolink"><span>Class VI <span class="title-sub">tud · thematic accented</span></span><span class="tag">soon</span></span></li>
          <li class="soon"><span class="nolink"><span>Class VII <span class="title-sub">rudh · -na- infix</span></span><span class="tag">soon</span></span></li>
          <li class="soon"><span class="nolink"><span>Class VIII <span class="title-sub">tan, kṛ · -u-</span></span><span class="tag">soon</span></span></li>
          <li class="soon"><span class="nolink"><span>Class IX <span class="title-sub">krī · -nā-</span></span><span class="tag">soon</span></span></li>
          <li class="soon"><span class="nolink"><span>Class X <span class="title-sub">cur · causative-like</span></span><span class="tag">soon</span></span></li>
        </ul>
      </section>

      <section class="cat-skt">
        <h3><span class="cat"></span>Verbs · Other systems</h3>
        <ul>
          <li class="soon"><span class="nolink"><span>Perfect <span class="title-sub">reduplicated liṭ</span></span><span class="tag">soon</span></span></li>
          <li class="soon"><span class="nolink"><span>Aorist <span class="title-sub">seven formations</span></span><span class="tag">soon</span></span></li>
          <li class="soon"><span class="nolink"><span>Futures <span class="title-sub">lṛṭ · luṭ</span></span><span class="tag">soon</span></span></li>
          <li class="soon"><span class="nolink"><span>Optative &amp; Imperative <span class="title-sub">liṅ · loṭ</span></span><span class="tag">soon</span></span></li>
          <li class="soon"><span class="nolink"><span>Passive &amp; Causative <span class="title-sub">-ya- · -aya-</span></span><span class="tag">soon</span></span></li>
        </ul>
      </section>

      <section class="cat-skt">
        <h3><span class="cat"></span>Compounds</h3>
        <ul>
          <li class="soon"><span class="nolink"><span>Tatpuruṣa <span class="title-sub">determinative</span></span><span class="tag">soon</span></span></li>
          <li class="soon"><span class="nolink"><span>Karmadhāraya <span class="title-sub">descriptive</span></span><span class="tag">soon</span></span></li>
          <li class="soon"><span class="nolink"><span>Bahuvrīhi <span class="title-sub">possessive</span></span><span class="tag">soon</span></span></li>
          <li class="soon"><span class="nolink"><span>Dvandva <span class="title-sub">copulative</span></span><span class="tag">soon</span></span></li>
          <li class="soon"><span class="nolink"><span>Avyayībhāva <span class="title-sub">adverbial</span></span><span class="tag">soon</span></span></li>
        </ul>
      </section>

      <section class="cat-skt">
        <h3><span class="cat"></span>Sandhi</h3>
        <ul>
          <li class="soon"><span class="nolink"><span>Vowel sandhi <span class="title-sub">ac-sandhi</span></span><span class="tag">soon</span></span></li>
          <li class="soon"><span class="nolink"><span>Visarga sandhi <span class="title-sub">ḥ-sandhi</span></span><span class="tag">soon</span></span></li>
          <li class="soon"><span class="nolink"><span>Consonant sandhi <span class="title-sub">hal-sandhi</span></span><span class="tag">soon</span></span></li>
        </ul>
      </section>

      <div class="sb-foot">
        <div>Maria Iontseva</div>
        <div>Oxford · MPhil</div>
        <div><b>MMXXVI</b></div>
      </div>

    </nav>
  `;

  // ============================================================
  //  SVAPNA — dream research sidebar
  // ============================================================
  const SB_SVAPNA = `
    ${homeBack('SVAPNA', 'dream<br>research')}

    <div class="sb-search">
      <input type="text" placeholder="Search 311 texts…" />
    </div>

    <nav class="sb-nav">

      <section class="cat-svapna">
        <h3><span class="cat"></span>The project</h3>
        <ul>
          <li data-key="svapna-home"><a href="${U('svapna/index.html')}"><span>Search the corpus <span class="title-sub">311 texts · 5 indexed terms</span></span><span class="tag">now</span></a></li>
          <li data-key="svapna-traditions"><a href="${U('svapna/traditions.html')}"><span>Śaiva traditions <span class="title-sub">20 texts · passages by branch</span></span><span class="tag">now</span></a></li>
          <li data-key="svapna-typology" class="soon"><span class="nolink"><span>Typology of operations <span class="title-sub">five categories — essay</span></span><span class="tag">soon</span></span></li>
          <li data-key="svapna-method" class="soon"><span class="nolink"><span>Methodology <span class="title-sub">sources, criteria</span></span><span class="tag">soon</span></span></li>
        </ul>
      </section>

      <section class="cat-svapna">
        <h3><span class="cat"></span>Readings</h3>
        <ul>
          <li class="soon"><span class="nolink"><span>Yoginītantra <span class="title-sub">three dream vidyās · ch. 7</span></span><span class="tag">soon</span></span></li>
          <li class="soon"><span class="nolink"><span>Jayadrathayāmala <span class="title-sub">svapnamānavaka</span></span><span class="tag">soon</span></span></li>
          <li class="soon"><span class="nolink"><span>Brahmayāmala <span class="title-sub">dream chapters</span></span><span class="tag">soon</span></span></li>
          <li class="soon"><span class="nolink"><span>Tantrāloka 10 <span class="title-sub">three states</span></span><span class="tag">soon</span></span></li>
          <li class="soon"><span class="nolink"><span>Kashmir &amp; late synthesis <span class="title-sub">spanda, pratyabhijñā</span></span><span class="tag">soon</span></span></li>
        </ul>
      </section>

      <div class="sb-foot">
        <div>The Industry of Miracles</div>
        <div>Oxford · MPhil</div>
        <div><b>MMXXVI</b></div>
      </div>

    </nav>
  `;

  // ---------- universal top site-nav ----------
  const SITE_NAV_HTML = `
    <a class="brand" href="${U('index.html')}">svapna<span class="dot">·</span><span class="ext">space</span></a>
    <div class="links">
      <a href="${U('skt/s-stems.html')}" data-nav="skt">Sanskrit</a>
      <a href="${U('svapna/index.html')}" data-nav="svapna">Svapna</a>
      <a href="${U('about.html')}" data-nav="about">About</a>
    </div>
  `;
  const sitenav = document.getElementById('sitenav');
  if(sitenav){
    sitenav.innerHTML = SITE_NAV_HTML;
    const page = document.body.getAttribute('data-page') || '';
    const navKey = section || (page === 'about' ? 'about' : null);
    if(navKey){
      const link = sitenav.querySelector(`[data-nav="${navKey}"]`);
      if(link) link.classList.add('active');
    }
  }

  // ---------- mount sidebar (SKT only now) ----------
  const sb = document.getElementById('sidebar');
  if(sb && section === 'skt'){
    sb.innerHTML = SB_SKT;
    if(key){
      const li = sb.querySelector(`li[data-key="${key}"]`);
      if(li) li.classList.add('active');
    }
  }

  // ---------- mobile drawer ----------
  const bd = document.getElementById('backdrop');
  const openBtn = document.getElementById('sbOpen');
  const closeBtn = document.getElementById('sbClose');
  function open(){ sb && sb.classList.add('open'); bd && bd.classList.add('open'); document.body.style.overflow='hidden'; }
  function close(){ sb && sb.classList.remove('open'); bd && bd.classList.remove('open'); document.body.style.overflow=''; }
  if(openBtn) openBtn.addEventListener('click', open);
  if(closeBtn) closeBtn.addEventListener('click', close);
  if(bd) bd.addEventListener('click', close);
  document.addEventListener('keydown', e => { if(e.key === 'Escape') close(); });
  if(sb){
    sb.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => { if(window.innerWidth <= 880) close(); });
    });
  }

})();
