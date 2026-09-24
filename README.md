# HEYFINORA Ultimate OneNote Planner PRO 2026–2027

This builder turns the *Product Blueprint, Part 1: Information Architecture* into a real OneNote
notebook. It creates the notebook in **your own OneNote account** through Microsoft Graph, with all
16 areas, 284 pages, and working navigation bars, breadcrumbs and prev/next links.

| | |
|---|---|
| Notebook | 16 top-level areas numbered 00–15 (8 sections, 8 section groups, 44 sections in total) |
| Pages | 284 = 101 fixed + 177 pre-dated + 6 samples (same counts as the blueprint) |
| Dates | Jul 2026 – Dec 2027, weeks start Monday, each week filed under the month that holds its Thursday |
| Templates | 36, in 9 Template Library sections |
| Links | Global bar, context bar and footer on every page, all linked to real pages |

---

## Quick start (Roman Urdu)

**1. Python install karein** (3.10 ya naya): https://www.python.org/downloads/

**2. Yeh folder download karein** (GitHub pe *Code → Download ZIP*) aur terminal usi folder mein kholein:

```bash
pip install -r requirements.txt
```

**3. Pehle preview dekh lein (optional):**

```bash
python build.py preview
```

Phir `preview/index.html` ko browser mein kholein. Har page aur har link aap click karke check kar sakte hain.

**4. OneNote mein banayein:**

```bash
python build.py publish
```

Screen par ek code aur link (`https://microsoft.com/devicelogin`) aayega. Link kholein, code dalein, aur
apne Microsoft account se sign in karein (wohi account jis mein OneNote hai). Uske baad script khud:

- Pass 1: notebook, section groups, sections aur 284 pages banati hai
- Pass 2: har page par saare links (HOME, PLAN, ◀ PREV, NEXT ▶, breadcrumbs) set karti hai

Is mein takreeban 15–30 minute lagte hain. Agar beech mein ruk jaye to wohi command dobara chalayein.
`.heyfinora-state.json` progress yaad rakhti hai, is liye wahin se shuru hoga aur koi page dobara nahi banega.

**5. OneNote mein aakhri steps** (API yeh kaam nahi kar sakti, is liye haath se karne honge):

| Step | Kaise |
|---|---|
| **Subpages banayein** | Har quarter section mein week pages aur Month Review ko select karein → `Ctrl+Alt+]` (Windows) ya right-click → *Make Subpage*. Script end mein poori list print karti hai. HABITS ke monthly trackers aur GOALS ka EXAMPLE page bhi. |
| Money par password | MONEY ke teeno sections aur *Reference Vault* par right-click → *Password Protect This Section* |
| Waiting For tag | *Tags & Checkbox Setup* page par diye gaye steps (Windows par sirf ek dafa) |
| Day page shortcut (Windows) | *TEMPLATE · Daily – Standard* ko *Insert → Page Templates* se save karein aur har quarter section ka default template bana dein |

---

## Options

```bash
python build.py stats                              # har area ke page count
python build.py preview --out preview              # offline HTML preview
python build.py publish --start 2026-01            # Jan 2026 se shuru (blueprint ka doosra option)
python build.py publish --name "My Planner"        # notebook ka alag naam
python build.py publish --today 2026-10-05         # "You are here" links is date ke hisaab se
python build.py publish --links web                # OneNote ke app links ke bajaye web links
python build.py publish --tenant consumers         # sirf personal Microsoft account
```

### Sign-in doesn't work?

By default the script signs in through Microsoft's public "Graph Command Line Tools" app. If your
account or organisation blocks it (an `AADSTS…` error), register your own free app:

1. Go to https://entra.microsoft.com → *App registrations* → *New registration*.
2. Supported account types: *Accounts in any organizational directory and personal Microsoft accounts*.
3. Open *Authentication*, set *Allow public client flows* to **Yes**, and save.
4. Open *API permissions* → *Add* → *Microsoft Graph* → *Delegated* → `Notes.ReadWrite`.
5. Run `python build.py publish --client-id <Application (client) ID>`.

---

## How it maps to the blueprint

| Blueprint | Code |
|---|---|
| §3 Master notebook architecture | `heyfinora/notebook.py` |
| §4 PLAN groups: Year, Quarter, Month, Week, reviews | `heyfinora/pages/plan.py`, `heyfinora/dates.py` |
| §4, 7–9: Tasks, Goals, Habits | `heyfinora/pages/systems.py` |
| §10–11: Projects (Project Kit + EXAMPLE), Work & Business | `heyfinora/pages/projects_work.py` |
| §12: Money | `heyfinora/pages/money.py` |
| §13–15: Growth, Journal, Notes, Reviews, Archive | `heyfinora/pages/life.py` |
| §16: Template library (36) | `heyfinora/pages/templates.py` |
| §0–1: Start Here, Home | `heyfinora/pages/start_home.py` |
| §6: Navigation (global bar, context bar, footer) | `heyfinora/core.py` |
| Publishing through Microsoft Graph | `heyfinora/graph.py` |

The **Decisions for you before Part 2** use the blueprint's recommended defaults: 18 months
(Jul 2026 – Dec 2027), Monday weeks, all 13 merges, the 8 default Life Areas, and full Content and
Clients sections. You can change the date range with `--start` and `--end`. The other defaults are
set in code.

### Known limits (OneNote API)

- **Subpage levels:** the API can't set them, so pages are created in the right order and you indent
  them once (step 5). Links don't depend on this.
- **Paragraph links** (▲ TOP to a heading): the API can't make them, so ▲ TOP links to the page itself.
- **Styling:** colours and fonts come from the five-token theme in `heyfinora/core.py` (`THEME`).
  The Part 2 visual design can replace these values.
- **Selling copies:** links point to *this* notebook. For buyer delivery, test the `.onepkg` and
  OneDrive-copy routes before launch, as the blueprint's "biggest technical risk" note says.

## Tests

```bash
pip install pytest && python -m pytest -q
```

The tests check the blueprint page counts (284), ISO week placement, that every link resolves to a
real page, that templates link only to fixed hubs, and that section names are safe for the Graph API.
