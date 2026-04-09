# Sanskrit Verb Paradigms Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add verb conjugation paradigms to svapna.space, starting with the present system (laṭ, 10 classes) and the optative (liṅ), with reference tables, smart mnemonics, and validated exercises — following the same design language as the existing nominal paradigm pages.

**Architecture:** Each verb system gets its own HTML page with tabs (like the demonstrative-pronouns page). A new verb paradigm-nav links between verb pages. The left TOC category IV "Present-system verbs" becomes active and clickable. Paradigm data lives as Python dicts in a generator script, producing clean HTML via templates — same pattern used for the pronoun pages.

**Tech Stack:** Plain HTML/CSS/JS (no framework). Python generator for the HTML from paradigm data dicts. Existing `site.css` + `site.js`. Gentium Plus for Sanskrit forms, Inter for chrome.

---

## Scope — What Whitney/MacDonell covers

### Present system (laṭ) — Whitney §599–699, MacDonell §122–142
Ten verb classes (gaṇas), divided into two groups:
- **Thematic** (classes I, IV, VI, X): present stem + thematic vowel -a-
- **Athematic** (classes II, III, V, VII, VIII, IX): present stem directly before endings

For the first pass, we cover **4 representative classes** (one per major type):
1. **Class I** (bhvādi) — `bhū` "to be" → `bhava-` (thematic, most common)
2. **Class II** (adādi) — `as` "to be" → athematic root present  
3. **Class IV** (divādi) — `div/dīv` "to shine/play" → `-ya-` present
4. **Class VI** (tudādi) — `tud` "to strike" → thematic, accent on ending

### Optative (liṅ) — Whitney §557–560, MacDonell §148
The optative mood uses its own set of endings. Two types:
- **Thematic optative**: stem + `-e-` + secondary endings (bhav-e-t)
- **Athematic optative**: stem + `-yā-/-ī-` + secondary endings (s-yā-t)

### What we DON'T cover yet (future phases)
- Classes III, V, VII, VIII, IX (add later as needed)
- Imperative (loṭ), imperfect (laṅ)
- Perfect (liṭ), aorist (luṅ), futures (lṛṭ, luṭ)
- Passive, causative, desiderative, intensive
- These are marked "soon" in the TOC and paradigm-nav

---

## File Structure

### New files
| File | Purpose |
|------|---------|
| `docs/skt/present-verbs.html` | Present tense (laṭ) — 4 tabs (classes I, II, IV, VI) with parasmaipada + ātmanepada tables, mnemonics, exercises |
| `docs/skt/optative.html` | Optative mood (liṅ) — 2 tabs (thematic bhū, athematic as), both padas, exercises |
| `generate-verbs.py` | Python generator script producing both HTML files from paradigm data dicts |

### Modified files
| File | Change |
|------|--------|
| `docs/skt/index.html` | Grammar tile: make "Present-system verbs" clickable, update meta |
| `docs/skt/*.html` (all 18 grammar pages) | Canonicalise TOC: make IV "Present-system verbs" a link to `present-verbs.html`, make V "Other verb systems" link to `optative.html` |
| `docs/assets/site.css` | No new CSS needed — reuses existing `.tabs`, `.tab-btn`, `.tab-panel`, `.decl`, `.exercise-table`, `.page-layout`, `.page-toc` |

---

## Paradigm Data (Whitney / MacDonell verified)

### Present active endings (parasmaipada) — all classes share these
```
        Singular    Dual        Plural
1st     -mi         -vaḥ        -maḥ
2nd     -si         -thaḥ       -tha
3rd     -ti         -taḥ        -anti (thematic) / -ati (athematic)
```

### Present middle endings (ātmanepada)
```
        Singular    Dual        Plural
1st     -e          -vahe       -mahe
2nd     -se         -āthe       -dhve
3rd     -te         -āte        -ante (thematic) / -ate (athematic)
```

### Class I: bhū → bhava- (thematic)
**Parasmaipada:**
```
bhavāmi    bhavāvaḥ    bhavāmaḥ
bhavasi    bhavathaḥ   bhavatha
bhavati    bhavataḥ    bhavanti
```

**Ātmanepada** (bhū is usually para, but for completeness):
Uses thematic -a- + middle endings.

### Class II: as "to be" → athematic root present
**Parasmaipada only** (no ātmanepada for √as):
```
asmi       svaḥ        smaḥ
asi        sthaḥ       stha
asti       staḥ        santi
```

Note: strong stem `as-`, weak stem `s-`. Whitney §636.

### Class IV: div → dīvya- (ya-class)
**Parasmaipada:**
```
dīvyāmi    dīvyāvaḥ    dīvyāmaḥ
dīvyasi    dīvyathaḥ   dīvyatha
dīvyati    dīvyataḥ    dīvyanti
```

### Class VI: tud → tuda- (thematic, accent on ending)
**Parasmaipada:**
```
tudāmi     tudāvaḥ     tudāmaḥ
tudasi     tudathaḥ    tudatha
tudati     tudataḥ     tudanti
```

**Ātmanepada:**
```
tude       tudāvahe    tudāmahe
tudase     tudāthe     duddhve
tudate     tudāte      tudante
```

### Optative — thematic (bhū)
**Parasmaipada:**
```
bhaveyam    bhaveva      bhavema
bhaveḥ      bhavetam     bhaveta
bhavet      bhavetām     bhaveyuḥ
```

**Ātmanepada:**
```
bhaveya     bhavevahi    bhavemahi
bhavethāḥ   bhaveyāthām  bhavedhvam
bhaveta     bhaveyātām   bhaveran
```

### Optative — athematic (as → syā-)
**Parasmaipada only:**
```
syām       syāva       syāma
syāḥ       syātam      syāta
syāt       syātām      syuḥ
```

---

## Tasks

### Task 1: Create the Python generator script

**Files:**
- Create: `docs/generate-verbs.py`

This script contains the paradigm data as Python dicts and an HTML template function, producing both `present-verbs.html` and `optative.html`. Same approach used for `demonstrative-pronouns.html`.

- [ ] **Step 1: Write the generator script**

The script must:
1. Define paradigm data for each verb class (parasmaipada + ātmanepada where applicable)
2. Define paradigm data for optative (thematic + athematic)
3. Use a shared HTML template function that produces: head (GA, favicon, SEO), home-shell, breadcrumbs, page-layout (TOC + page-main), paradigm-nav, tabs, reference tables, exercise tables, exercise JS, footer
4. Output two HTML files

Key design decisions:
- Verb tables have **3 persons × 3 numbers = 9 cells** (not 7-8 cases × 3 numbers like nouns)
- Row headers are "1st / 2nd / 3rd" (not case names like "Nom. / Acc.")
- Column headers remain "Singular / Dual / Plural"
- Each tab shows one class or one mood variant
- Para and ātma tables are stacked vertically within each tab (like m/f/n tables in i-short)

CSS class `.case` is reused for person labels (works fine visually — just different text content).

- [ ] **Step 2: Run the generator**

```bash
cd ~/svapna/docs && python3 generate-verbs.py
```

Expected: creates `skt/present-verbs.html` and `skt/optative.html`

- [ ] **Step 3: Verify both pages load locally**

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8733/docs/skt/present-verbs.html
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8733/docs/skt/optative.html
```

Expected: both 200

- [ ] **Step 4: Open and visually verify**

```bash
open http://localhost:8733/docs/skt/present-verbs.html
open http://localhost:8733/docs/skt/optative.html
```

Check: tabs switch correctly, exercise validation works, tables render cleanly, paradigm-nav shows verb items.

- [ ] **Step 5: Commit**

```bash
cd ~/svapna
git add docs/generate-verbs.py docs/skt/present-verbs.html docs/skt/optative.html
git commit -m "feat: add present-system verbs (classes I, II, IV, VI) and optative

Present verbs page: 4 tabs (Class I bhū, Class II as, Class IV div, 
Class VI tud) with parasmaipada + ātmanepada tables where applicable.
Optative page: 2 tabs (thematic bhū, athematic as) with both padas.
Both pages include per-tab exercises with live validation.
Whitney §599-699 (present), §557-560 (optative).
MacDonell §122-142, §148.

Generated by docs/generate-verbs.py from paradigm data dicts."
```

### Task 2: Update TOC on all existing grammar pages

**Files:**
- Modify: all 18 files in `docs/skt/` that have `<aside class="page-toc">`

The canonical TOC must update:
- Row IV: "Present-system verbs" → clickable `<a href="present-verbs.html">`, sub changes to "classes I, II, IV, VI · laṭ"
- Row V: "Other verb systems" → clickable `<a href="optative.html">`, sub changes to "optative (liṅ) · more soon"

- [ ] **Step 1: Write a Python bulk-update script**

```python
# Update canonical TOC on all grammar pages
import re, pathlib

skt = pathlib.Path('docs/skt')
pages = [f for f in skt.glob('*.html') if f.name not in ('index.html',)]

for p in pages:
    s = p.read_text()
    # Replace span.title Present-system with a link
    s = re.sub(
        r'<span class="title">Present-system verbs</span>\s*<span class="sub">classes I – X</span>',
        '<a href="present-verbs.html">Present-system verbs</a><span class="sub">classes I, II, IV, VI · laṭ</span>',
        s
    )
    # Replace span.title Other verb with a link  
    s = re.sub(
        r'<span class="title">Other verb systems</span>\s*<span class="sub">[^<]*</span>',
        '<a href="optative.html">Other verb systems</a><span class="sub">optative (liṅ) · more soon</span>',
        s
    )
    p.write_text(s)
```

- [ ] **Step 2: Run the script**

```bash
cd ~/svapna && python3 -c "<paste script above>"
```

- [ ] **Step 3: Verify a sample page**

```bash
grep "present-verbs.html\|optative.html" docs/skt/a-stems-m.html
```

Expected: both links present in the TOC `<ol>`

- [ ] **Step 4: Commit**

```bash
git add docs/skt/
git commit -m "chore: update TOC on all grammar pages — verbs now clickable"
```

### Task 3: Update SKT landing page

**Files:**
- Modify: `docs/skt/index.html`

- [ ] **Step 1: Make "Present-system verbs" and "Other verb systems" clickable in the Grammar tile**

Replace the two `<span class="soon">` entries with `<a>` entries:

```html
<!-- Was: -->
<span class="soon">
  Present-system verbs
  <span class="meta">classes I – X · soon</span>
</span>

<!-- Becomes: -->
<a href="present-verbs.html">
  Present-system verbs
  <span class="meta">classes I, II, IV, VI &nbsp;·&nbsp; laṭ present tense</span>
</a>
```

```html
<!-- Was: -->
<span class="soon">
  Other verb systems
  <span class="meta">perfect, aorist, future · soon</span>
</span>

<!-- Becomes: -->
<a href="optative.html">
  Other verb systems
  <span class="meta">optative (liṅ) &nbsp;·&nbsp; more coming</span>
</a>
```

- [ ] **Step 2: Commit**

```bash
git add docs/skt/index.html
git commit -m "feat: make verb entries clickable on SKT landing page"
```

### Task 4: Deploy and verify

- [ ] **Step 1: Push to GitHub**

```bash
git push origin main
```

- [ ] **Step 2: Wait for Pages build and verify**

```bash
sleep 45
curl -s -o /dev/null -w "%{http_code}\n" https://svapna.space/skt/present-verbs.html
curl -s -o /dev/null -w "%{http_code}\n" https://svapna.space/skt/optative.html
```

Expected: both 200

- [ ] **Step 3: Verify tabs, exercises, and navigation on live site**

Open both pages, switch tabs, try exercises, click paradigm-nav links, verify TOC links work from other grammar pages.

---

## Future expansion (not in this plan)

After this first pass, the verb paradigm system can be extended by adding tabs/pages for:

**More present classes** (add tabs to present-verbs.html):
- Class III (juhotyādi): reduplicated — hu → juho- (Whitney §655)
- Class V (svādi): -nu- suffix — su → suno- (Whitney §674)
- Class VII (rudhādi): nasal infix — rudh → runa-dh- (Whitney §680)
- Class VIII (tanādi): -u- suffix — tan → tano- (Whitney §685)
- Class IX (kryādi): -nā-/-nī- suffix — krī → krīṇā- (Whitney §688)
- Class X (curādi): causative-like -aya- — cur → coraya- (Whitney §694)

**More verb systems** (new pages):
- Imperfect (laṅ) — past unaugmented
- Imperative (loṭ) — command
- Perfect (liṭ) — reduplicated past
- Aorist (luṅ) — 7 formations
- Futures (lṛṭ simple, luṭ periphrastic)
- Passive (-ya-)
- Causative (-aya-)
- Desiderative (reduplication + -sa-)
- Intensive/frequentative (heavy reduplication)

Each becomes a new page or set of tabs, linked via the verb paradigm-nav.
