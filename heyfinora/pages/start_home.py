"""00 START HERE and 01 HOME."""
from __future__ import annotations

from ..core import Ctx, Group, Page, Section
from .common import LIFE_AREAS

START_BAR = [("WELCOME", "start.welcome"), ("QUICK START", "start.quick"),
             ("HOW IT WORKS", "start.how"), ("NAVIGATION", "start.nav"), ("FAQ", "start.faq")]


def welcome(c: Ctx):
    return [
        c.h1("Welcome to your HEYFINORA Planner PRO"),
        c.p("One notebook where your time, tasks, goals, projects, work and money connect. "
            "Open one page each morning, know exactly what matters today, and trust that nothing is lost."),
        c.h2("Start in this order"),
        c.numbered(["[[Quick Start: Your First 15 Minutes|start.quick]]",
                    "[[How the System Works|start.how]]",
                    "[[Navigation Guide|start.nav]]",
                    "Then open [[HOME|home.dashboard]] and plan today."]),
        c.h2("What's inside"),
        c.table(["Area", "What it's for"], [
            ["[[HOME|home.dashboard]]", "Launch point with links to this year, quarter, month and week"],
            ["[[PLAN|@year]]", "Year › Quarter › Month › Week pages, pre-dated and linked"],
            ["[[TASKS|tasks.dashboard]]", "Inbox → Action List → Week → Day"],
            ["[[GOALS|goals.dashboard]]", "Vision → annual goals → goal pages"],
            ["[[HABITS|habits.dashboard]]", "Habit design, routines, monthly trackers"],
            ["[[PROJECTS|projects.portfolio]]", "Portfolio + a 5-page kit per project"],
            ["[[WORK & BUSINESS|work.dashboard]]", "Meetings, clients, content, SOPs, decisions"],
            ["[[MONEY|money.dashboard]]", "Budgets, bills, savings, debt (password-protectable)"],
            ["[[GROWTH|growth.dashboard]] · [[JOURNAL|journal.home]] · [[NOTES|notes.quick]]",
             "Learning, reflection and knowledge"],
            ["[[REVIEWS|reviews.hub]]", "The review cadence that keeps everything current"],
            ["[[TEMPLATE LIBRARY|tpl.guide]] · [[ARCHIVE|archive.guide]]", "Blank templates; finished items"],
        ], widths=[240, 400], shade_first=True),
        c.h2("Support"),
        c.p("Questions or a broken link? Contact HEYFINORA support through the shop you bought from. "
            "Please include your device (Windows, Mac, web, iPad, phone) and the page name."),
    ]


def quick_start(c: Ctx):
    return [
        c.note("Tick each step. You'll have your first day planned in about 15 minutes."),
        c.h2("Minutes 1–3: get your bearings"),
        c.todos(["Open [[HOME|home.dashboard]] and click each link in the global bar once",
                 "Read the two-minute [[How the System Works|start.how]]"]),
        c.h2("Minutes 4–8: point the planner at today"),
        c.todos(["On the Master Dashboard, check the Current box links open this year, quarter, month and week",
                 "Name your 3 most important goals on [[the goals page|goals.dashboard]] (one line each is fine)",
                 "Rename the 8 [[Life Areas|home.areas]] if you want different ones"]),
        c.h2("Minutes 9–12: empty your head"),
        c.todos(["Write every open task you can think of in the [[Inbox|tasks.inbox]]",
                 "Move this week's must-dos to the [[Action List|tasks.actions]] This Week block"]),
        c.h2("Minutes 13–15: plan today"),
        c.todos(["Open this week's page from HOME → This Week",
                 "Add today's page under the week from [[TEMPLATE · Daily – Standard|tpl.daily]]",
                 "Choose your Top 3 and go"]),
        c.h2("This week"),
        c.todos(["Set up tags once on Windows: [[Tags & Checkbox Setup|start.tags]]",
                 "Put a password on the MONEY sections (right-click the section → Password Protect)",
                 "Do your first [[Weekly Review|reviews.weekly]] on Sunday"]),
    ]


def how_it_works(c: Ctx):
    return [
        c.h2("The operating model"),
        c.table(["Part", "Job"], [
            ["HOME", "Routes you. Holds only the “You are here” links."],
            ["PLAN", "Decides when: year, quarter, month, week, day."],
            ["SYSTEMS", "Hold what: Tasks, Goals, Habits, Projects."],
            ["DOMAINS", "Specialist detail: Work & Business, Money, Growth."],
            ["CAPTURE & REFLECT", "Catch everything: Notes, Journal."],
            ["REVIEWS", "Move things to their right home, every period."],
            ["TEMPLATE LIBRARY", "Creates new pages anywhere."],
        ], widths=[170, 470], shade_first=True),
        c.h2("Seven rules"),
        c.numbered(["**One home per item.** Every task, goal, number or note lives in one place; other pages link to it.",
                    "**Time pages plan; system pages hold.**",
                    "**Pre-built vs on demand.** Years to weeks are ready; days, projects, meetings and notes come from templates.",
                    "**Three clicks to anything.** Home → area → page.",
                    "**The same bar on every page.**",
                    "**Native OneNote only.** Tags, checkboxes, tables, links, subpages, passwords.",
                    "**Reviews close every loop.**"]),
        c.h2("The review cadence"),
        c.table(["Cadence", "When", "Time", "Where"], [
            ["Daily shutdown", "End of day", "5 min", "Day page"],
            ["Weekly", "Sunday", "30 min", "[[Weekly Review Checklist|reviews.weekly]] + Week page"],
            ["Monthly", "Last day", "30 min", "Month Review (under each Month Dashboard)"],
            ["Quarterly", "Last week", "45 min", "Quarter Review in each quarter section"],
            ["Yearly", "Late December", "90 min", "Year-End Review in the Year section"],
        ], widths=[120, 110, 70, 340]),
        c.h2("The goal cascade"),
        c.p("Life Vision → Annual Goals → Quarter Objectives → Month Targets → Weekly Big 3 → Daily Top 3."),
    ]


def navigation(c: Ctx):
    return [
        c.p("One rule: **blue caps text is a link; HOME always brings you back.**"),
        c.h2("Layer 1 – Global bar (every page)"),
        c.p("HOME · PLAN · TASKS · GOALS · PROJECTS · WORK · MONEY · NOTES · REVIEWS · MORE"),
        c.bullets(["PLAN opens the current Year Dashboard.",
                   "MORE opens the [[Notebook Map|home.map]]: Habits, Growth, Journal, Templates, Archive, Start Here."]),
        c.h2("Layer 2 – Context bar (changes by page)"),
        c.table(["Page", "Bar"], [
            ["Year Dashboard", "◀ PREV YEAR · Q1 · Q2 · Q3 · Q4 · AT A GLANCE · NEXT YEAR ▶"],
            ["Quarter Plan", "2027 › Q2 · APRIL · MAY · JUNE · QUARTER REVIEW · ◀ PREV · NEXT ▶"],
            ["Month Dashboard", "2027 › Q2 › MAY · W18 · W19 … · HABITS · BUDGET · REVIEW · ◀ PREV · NEXT ▶"],
            ["Week page", "2027 › Q2 › MAY › W19 · ACTION LIST · ◀ PREV WEEK · NEXT WEEK ▶"],
            ["Day page", "TODAY'S PLAN · ACTION LIST · INBOX · HABITS · JOURNAL"],
        ], widths=[140, 500], shade_first=True),
        c.p("The breadcrumb (2027 › Q2 › MAY) is your BACK button: each part opens one level up."),
        c.h2("Footer"), c.p("▲ TOP · HOME · SECTION DASHBOARD"),
        c.h2("Keep “This Week” current"),
        c.p("OneNote can't link to “today” automatically. Every Sunday: right-click next week's page → "
            "Copy Link to Page → on the Master Dashboard, select the words This Week → Ctrl+K → paste. 20 seconds."),
        c.h2("Three-click paths"),
        c.table(["I want to…", "Path"], [
            ["Plan today", "HOME → This Week → today's Day page"],
            ["Add a task", "TASKS → Inbox"],
            ["Check a goal", "GOALS → Goals Dashboard → goal page"],
            ["Log a bill", "MONEY → this month's budget"],
            ["Start a project", "PROJECTS → How to Start a Project"],
        ], widths=[160, 480], shade_first=True),
    ]


def tags_setup(c: Ctx):
    return [
        c.h2("Tags used in the planner"),
        c.table(["Tag", "Meaning", "Windows", "Mac"], [
            ["To Do (checkbox)", "Any task", "Ctrl+1", "Cmd+1"],
            ["Important (star)", "High priority", "Ctrl+2", "Cmd+2"],
            ["Question", "Needs an answer or decision", "Ctrl+3", "Cmd+3"],
            ["Waiting For (custom)", "Blocked on someone", "set up below", "shows once created"],
        ], widths=[160, 240, 120, 120], shade_first=True),
        c.h2("Create the Waiting For tag (Windows, once)"),
        c.numbered(["Home tab → Tags gallery → Customize Tags → New Tag.",
                    "Name it Waiting For, pick the hourglass or clock symbol, OK.",
                    "It now appears on every device that syncs this notebook."]),
        c.h2("See every high-priority item (Windows)"),
        c.p("Home → Find Tags → Group by Tag name → Search: This Notebook → Create Summary Page. "
            "Every starred item appears with a link back to where it lives. "
            "On other devices, search for the star or read the Action List's High Priority rows."),
        c.h2("Optional reminders"),
        c.p("On Windows with Outlook, select a task → Home → Outlook Tasks to add a reminder."),
    ]


def devices(c: Ctx):
    return [
        c.table(["Device", "Best for", "Notes"], [
            ["Windows (OneNote)", "Setup and weekly planning", "Everything works: templates, tag summaries, passwords, inline maths"],
            ["Mac", "Daily use and reviews", "Copy templates by right-click → Copy To; passwords work"],
            ["Web (onenote.com)", "Quick access anywhere", "Links and checkboxes work; locked sections may need desktop"],
            ["iPad", "Daily pages, handwriting", "Great for the Day page with a pencil"],
            ["Phone", "Capture", "Add to Inbox or Quick Notes; tick tasks"],
        ], widths=[150, 170, 320], shade_first=True),
        c.h2("Sync tips"),
        c.bullets(["Keep the notebook in OneDrive so every device sees the same copy.",
                   "If a page looks out of date, right-click the notebook → Sync This Notebook Now.",
                   "Never keep two copies of the notebook: links always point to the original pages."]),
    ]


def faq(c: Ctx):
    qa = [
        ("A link opens the wrong page or nothing.", "The target page was probably deleted. Finished items belong in Archive, not the bin, so links keep working. Re-link with right-click → Copy Link to Page."),
        ("Why don't the tables add up?", "OneNote tables don't calculate. On Windows type 1250+380= and press Enter. For automatic totals, use the HEYFINORA Excel or Google Sheets budget."),
        ("Where are the day pages?", "Days are created when you need them from TEMPLATE · Daily, so the notebook stays fast."),
        ("How do I extend past December 2027?", "Copy the Planning templates into a new PLAN group; see the [[Template Index|tpl.guide]]."),
        ("Can I rename things?", "Yes. Links follow pages, not names, so renaming is safe."),
        ("I missed a week.", "Skip it. Do a normal Weekly Review for the coming week; don't back-fill."),
    ]
    out = []
    for q, a in qa:
        out += [c.h3(q), c.p(a)]
    return out


def start_section() -> Section:
    b = START_BAR
    return Section("start.sec", "00 START HERE", [
        Page("start.welcome", "Welcome & Support", welcome, bar=b),
        Page("start.quick", "Quick Start: Your First 15 Minutes", quick_start, bar=b),
        Page("start.how", "How the System Works", how_it_works, bar=b),
        Page("start.nav", "Navigation Guide", navigation, bar=b),
        Page("start.tags", "Tags & Checkbox Setup", tags_setup, bar=b),
        Page("start.devices", "Devices & Sync Guide", devices, bar=b),
        Page("start.faq", "FAQ & Troubleshooting", faq, bar=b),
    ])


# ---------------------------------------------------------------------- HOME
HOME_BAR = [("MASTER DASHBOARD", "home.dashboard"), ("LIFE AREAS", "home.areas"), ("NOTEBOOK MAP", "home.map")]


def master_dashboard(c: Ctx):
    tiles = [
        ("PLAN", "@year"), ("TASKS", "tasks.dashboard"), ("GOALS", "goals.dashboard"), ("HABITS", "habits.dashboard"),
        ("PROJECTS", "projects.portfolio"), ("WORK", "work.dashboard"), ("MONEY", "money.dashboard"), ("GROWTH", "growth.dashboard"),
        ("JOURNAL", "journal.home"), ("NOTES", "notes.quick"), ("REVIEWS", "reviews.hub"), ("TEMPLATES", "tpl.guide"),
    ]
    rows = [[f"**[[{a}|{b}]]**" for a, b in tiles[i:i + 4]] for i in range(0, len(tiles), 4)]
    return [
        c.h2("You are here"),
        c.table(["This Year", "This Quarter", "This Month", "This Week"],
                [["[[This Year|@year]]", "[[This Quarter|@quarter]]", "[[This Month|@month]]", "[[This Week|@week]]"]],
                widths=[160, 160, 160, 160]),
        c.small("Every Sunday, repoint This Week (and on the 1st, This Month): right-click the page → "
                "Copy Link to Page → select the words here → Ctrl+K → paste."),
        c.h2("Today"),
        c.bullets(["Open This Week → today's Day page (or create it from [[TEMPLATE · Daily – Standard|tpl.daily]])",
                   "Capture anything new in the [[Inbox|tasks.inbox]]",
                   "Glance at the [[Action List|tasks.actions]]"]),
        c.h2("Areas"),
        c.table(["", "", "", ""], rows, widths=[160, 160, 160, 160], header=False),
        c.h2("Active goals"),
        c.table(["Goal (link)", "Life area", "Status"], [], widths=[340, 150, 150], blank=3),
        c.h2("Active projects"),
        c.table(["Project (link)", "Next milestone", "Due"], [], widths=[300, 220, 120], blank=3),
        c.h2("Reminders"),
        c.todos(["Weekly Review on Sunday: [[checklist|reviews.weekly]]",
                 "Month-end: Month Review, budget close, habit %"]),
    ]


def life_areas(c: Ctx):
    return [
        c.note("The backbone of the planner. Goals, projects, habits and the review scorecard all tag to "
               "these eight areas. Rename them to suit your life."),
        c.table(["Life area", "What it covers for me", "Score now (1–10)", "Linked goals", "Linked habits"],
                [[a, "", "", "", ""] for a in LIFE_AREAS], widths=[130, 210, 90, 110, 100], shade_first=True),
        c.p("Quarterly scores: [[Life Area Scorecard|reviews.scorecard]] · Vision: [[Life Vision|goals.vision]]"),
    ]


def notebook_map(c: Ctx):
    out = [c.note("Every section in the notebook. Click a name to open its first page.")]
    for item in c.nb.items:
        if isinstance(item, Group):
            out.append(c.h3(item.name))
            out.append(c.bullets([f"[[{s.name}|{s.pages[0].key}]] – {len(s.pages)} pages"
                                  for s in item.sections if s.pages]))
        elif item.pages:
            out.append(c.h3(f"[[{item.name}|{item.pages[0].key}]]"))
    return out


def home_section() -> Section:
    return Section("home.sec", "01 HOME", [
        Page("home.dashboard", "Master Dashboard", master_dashboard, bar=HOME_BAR),
        Page("home.areas", "Life Areas", life_areas, bar=HOME_BAR),
        Page("home.map", "Notebook Map", notebook_map, bar=HOME_BAR),
    ])
