"""10 GROWTH, 11 JOURNAL, 12 NOTES & KNOWLEDGE, 13 REVIEWS, 15 ARCHIVE."""
from __future__ import annotations

from ..core import Ctx, Group, Page, Section
from ..dates import Calendar
from .common import LIFE_AREAS

# -------------------------------------------------------------------- GROWTH
GROWTH_BAR = [("GROWTH DASHBOARD", "growth.dashboard"), ("SKILL MAP", "growth.skills"),
              ("COURSES", "growth.courses"), ("READING", "growth.reading")]


def growth_dashboard(c: Ctx):
    return [
        c.lines(["Current learning focus 1", "Current learning focus 2", "This quarter's growth objective"]),
        c.small("Learning goals are ordinary goal pages tagged to Growth: [[Goals Dashboard|goals.dashboard]]"),
        c.h2("Learning log"),
        c.table(["Date", "What I learned", "Where it's noted"], [], widths=[90, 380, 170], blank=10),
    ]


def skill_map(c: Ctx):
    return [c.table(["Skill", "Why it matters", "Level now (1–5)", "Target", "How I'll build it", "Next step"],
                    [], widths=[110, 130, 70, 60, 140, 130], blank=8)]


def course_tracker(c: Ctx):
    return [
        c.note("Course notes go as subpages under this page, from [[TEMPLATE · Course Notes|tpl.course]]."),
        c.table(["Course", "Platform", "Start", "Target finish", "% done", "Status", "Notes (link)"], [],
                widths=[140, 90, 70, 80, 60, 80, 110], blank=6),
    ]


def reading_list(c: Ctx):
    return [
        c.note("Book notes go as subpages under this page, from [[TEMPLATE · Book Notes|tpl.book]]."),
        c.table(["Book", "Author", "Category", "Status", "Rating", "Notes (link)"], [],
                widths=[170, 120, 90, 90, 60, 110], blank=12),
        c.small("Status: To read · Reading · Done"),
    ]


def growth_section() -> Section:
    b = GROWTH_BAR
    return Section("growth.sec", "10 GROWTH", [
        Page("growth.dashboard", "Growth Dashboard", growth_dashboard, bar=b),
        Page("growth.skills", "Skill Map", skill_map, bar=b),
        Page("growth.courses", "Course Tracker", course_tracker, bar=b),
        Page("growth.reading", "Reading List", reading_list, bar=b),
    ])


# ------------------------------------------------------------------- JOURNAL
JOURNAL_BAR = [("JOURNAL HOME", "journal.home"), ("WINS", "journal.wins"), ("LESSONS", "journal.lessons")]

PROMPTS = {
    "Clarity": ["What matters most this week, and why?", "What am I avoiding?",
                "If I could only do one thing tomorrow, what would it be?", "What would make today a 10?",
                "What does ‘enough’ look like for me right now?", "What am I tolerating?",
                "Which commitment should I drop?", "What would I do if I weren't afraid?"],
    "Gratitude": ["Three small things that went right today", "Who helped me recently? How can I thank them?",
                  "A place I love and why", "Something I have now that I once wished for",
                  "A skill I'm glad I learned", "A hard time that taught me something",
                  "What made me laugh this week?", "What in my home am I grateful for?"],
    "Decisions": ["What are my real options?", "What would I advise a friend to do?",
                  "What will I think of this choice in 5 years?", "What's the cost of not deciding?",
                  "Which option fits my values best?", "What information am I missing?",
                  "What's the smallest reversible step?", "What does my gut say – and why?"],
    "Stress": ["What exactly is worrying me?", "What part of this can I control?",
               "What's the worst case, and could I handle it?", "What would help me rest tonight?",
               "Who could I ask for help?", "What can I remove from my plate?",
               "When did I last feel calm? What was different?", "What do I need to hear right now?"],
    "Growth": ["What did I learn this week?", "Where did I grow this month?",
               "What feedback did I get, and what's true in it?", "What habit would change my year?",
               "Who do I want to become?", "What am I proud of?",
               "What would I tell my younger self?", "What is the next level for me?"],
}


def journal_home(c: Ctx):
    out = [c.note("A 3-line reflection already sits on every Day page. Use this section for longer writing. "
                  "Make a month divider page (e.g. 2026-09 · September), then add entries under it from "
                  "[[TEMPLATE · Journal Entry|tpl.journal]]."),
           c.h2("Prompt library")]
    for group, prompts in PROMPTS.items():
        out += [c.h3(group), c.bullets(prompts)]
    return out


def wins(c: Ctx):
    return [c.note("Best wins and gratitudes, moved here from Day pages in the Weekly Review."),
            c.table(["Date", "Win or gratitude", "Life area"], [], widths=[90, 420, 130], blank=15)]


def lessons(c: Ctx):
    return [c.table(["Date", "Challenge", "What happened", "Lesson", "Next time I'll…"], [],
                    widths=[70, 130, 150, 140, 150], blank=10)]


def journal_section() -> Section:
    b = JOURNAL_BAR
    return Section("journal.sec", "11 JOURNAL", [
        Page("journal.home", "Journal Home & Prompt Library", journal_home, bar=b),
        Page("journal.wins", "Wins & Gratitude Log", wins, bar=b),
        Page("journal.lessons", "Lessons & Challenges Log", lessons, bar=b),
    ])


# ------------------------------------------------------------ NOTES & KNOWLEDGE
NOTES_BAR = [("QUICK NOTES", "notes.quick"), ("IDEA VAULT", "notes.ideas"), ("RESEARCH", "notes.research"),
             ("KNOWLEDGE BASE", "notes.kb"), ("VAULT", "notes.vault")]


def quick_notes(c: Ctx):
    return [c.note("One running page for anything. Newest at the top. In the Weekly Review: task → "
                   "[[Inbox|tasks.inbox]], idea → [[Idea Vault|notes.ideas]], info → "
                   "[[Knowledge Base|notes.kb]], or delete. For a big brain dump use "
                   "[[TEMPLATE · Brain Dump|tpl.braindump]]."),
            c.p(), c.p(), c.p()]


def idea_vault(c: Ctx):
    return [c.note("Business ideas worth testing move to the [[Opportunity Lab|work.opportunity]]."),
            c.table(["Idea", "Date", "Type", "Next step"], [], widths=[280, 80, 130, 150], blank=12),
            c.small("Type: Personal · Business · Content · Project")]


def research_index(c: Ctx):
    return [c.note("Create research pages from [[TEMPLATE · Research Note|tpl.research]] in this section."),
            c.table(["Question (link)", "Started", "Status", "Conclusion"], [], widths=[230, 80, 90, 240], blank=8)]


def kb_index(c: Ctx):
    out = [c.note("Evergreen “how I do X” articles live in this section, from "
                  "[[TEMPLATE · Knowledge Article|tpl.kb]]. The index also links notes that live elsewhere: "
                  "[[Book Notes|growth.reading]], [[Course Notes|growth.courses]], [[SOPs|work.sops]], "
                  "[[Meetings|work.meetings]].")]
    for block in ["A–E", "F–J", "K–O", "P–T", "U–Z"]:
        out += [c.h3(block), c.p()]
    return out


def important_info(c: Ctx):
    return [
        c.note("**No passwords, card numbers or ID numbers on this page.** Password-protect this section.",
               color="#F6DCD5"),
        c.h2("Emergency contacts"),
        c.table(["Name", "Relationship", "Phone"], [], widths=[220, 200, 220], blank=4),
        c.h2("Service providers"),
        c.table(["Service", "Company", "Contact", "Notes"], [["Doctor", "", "", ""], ["Dentist", "", "", ""],
                                                             ["Plumber", "", "", ""], ["Mechanic", "", "", ""]],
                widths=[120, 170, 170, 180], blank=2),
        c.h2("Renewals & warranties"),
        c.table(["Item", "Renewal / expiry", "Where the paperwork is"], [], widths=[220, 150, 270], blank=5),
    ]


def contacts(c: Ctx):
    return [c.table(["Name", "Role", "Contact details", "Context"], [], widths=[150, 120, 200, 170], blank=15)]


def useful_links(c: Ctx):
    return [c.table(["Link", "What it is", "Category"], [], widths=[260, 250, 130], blank=15)]


def notes_group() -> Group:
    b = NOTES_BAR
    return Group("notes", "12 NOTES & KNOWLEDGE", [
        Section("notes.capture", "Capture", [
            Page("notes.quick", "Quick Notes", quick_notes, bar=b),
            Page("notes.ideas", "Idea Vault", idea_vault, bar=b),
        ]),
        Section("notes.research.sec", "Research", [Page("notes.research", "Research Index", research_index, bar=b)]),
        Section("notes.kb.sec", "Knowledge Base", [Page("notes.kb", "KB Index (A–Z)", kb_index, bar=b)]),
        Section("notes.vault.sec", "Reference Vault", [
            Page("notes.vault", "Important Info", important_info, bar=b),
            Page("notes.contacts", "Contacts", contacts, bar=b),
            Page("notes.links", "Useful Links", useful_links, bar=b),
        ]),
    ])


# ------------------------------------------------------------------- REVIEWS
REVIEW_BAR = [("REVIEW HUB", "reviews.hub"), ("WEEKLY CHECKLIST", "reviews.weekly"),
              ("SCORECARD", "reviews.scorecard")]


def review_hub(cal: Calendar):
    def body(c: Ctx):
        rows = []
        for y in cal.years:
            for q in cal.quarters_of(y):
                for m in cal.months_in_quarter(y, q):
                    rows.append([m.label, f"[[Month Review|{m.review_key}]]", ""])
                rows.append([f"Q{q} {y}", f"[[Quarter Review|plan.{y}.q{q}.review]]", ""])
            rows.append([f"{y}", f"[[Year-End Review|plan.{y}.review]] · [[Money|money.plan.{y}]]", ""])
        return [
            c.h2("Cadence"),
            c.table(["Review", "When", "Time", "Page"], [
                ["Daily shutdown", "End of workday", "5 min", "Day page"],
                ["Weekly", "Sunday", "30 min", "[[Weekly Review Checklist|reviews.weekly]] + Week page"],
                ["Monthly", "Last day of month", "30 min", "Month Review under each Month Dashboard"],
                ["Quarterly", "Last week of quarter", "45 min", "Quarter Review + [[Scorecard|reviews.scorecard]]"],
                ["Business", "Quarterly", "30 min", "[[Business Reviews|work.bizreviews]]"],
                ["Yearly", "Late December", "90 min", "Year-End Review + Money Plan & Review"],
            ], widths=[120, 140, 70, 310], shade_first=True),
            c.h2("Review log"),
            c.small("After each review, write its key insight here."),
            c.table(["Period", "Review", "Key insight"], rows, widths=[140, 220, 280]),
        ]
    return body


def weekly_checklist(c: Ctx):
    return [
        c.note("Sunday, 30 minutes. Go top to bottom; untick them all next week (or copy fresh boxes)."),
        c.h2("1 · Get current (5 min)"),
        c.todos(["Repoint **This Week** on the [[Master Dashboard|home.dashboard]]: right-click next week's page → "
                 "Copy Link to Page → select This Week → Ctrl+K → paste",
                 "On the 1st of a month, also repoint This Month (and This Quarter at quarter start)"]),
        c.h2("2 · Get clear (10 min)"),
        c.todos(["Empty the [[Inbox|tasks.inbox]] and [[Quick Notes|notes.quick]]",
                 "Move action items from this week's meeting pages to Tasks",
                 "Review [[Waiting For|tasks.waiting]] – chase anything overdue",
                 "Move ticked tasks to the [[Completed Log|tasks.done]]",
                 "Move best wins from Day pages to the [[Wins Log|journal.wins]]"]),
        c.h2("3 · Look back (5 min)"),
        c.todos(["Answer the review questions at the bottom of this week's page",
                 "Update project status logs and the [[Portfolio|projects.portfolio]]"]),
        c.h2("4 · Plan next week (10 min)"),
        c.todos(["Read the Month Dashboard targets and due items",
                 "Copy this week's items from [[Recurring Tasks|tasks.recurring]]",
                 "Choose next week's Big 3",
                 "Move commitments from the [[Action List|tasks.actions]] (This Week block)",
                 "Plan the Work lane and meetings",
                 "Check [[Bills|money.bills]] due next week"]),
    ]


def scorecard(cal: Calendar):
    def body(c: Ctx):
        qs = [f"Q{q} {str(y)[2:]}" for y, q in cal.all_quarters()]
        return [
            c.note("Rate each area 1–10 at the end of every quarter. Look for the trend, not the number."),
            c.table(["Life area"] + qs, [[a] + [""] * len(qs) for a in LIFE_AREAS] + [["**Average**"] + [""] * len(qs)],
                    widths=[150] + [80] * len(qs), shade_first=True),
            c.lines(["Lowest area this quarter", "One change to lift it"]),
        ]
    return body


def reviews_section(cal: Calendar) -> Section:
    b = REVIEW_BAR
    return Section("reviews.sec", "13 REVIEWS", [
        Page("reviews.hub", "Review Hub", review_hub(cal), bar=b),
        Page("reviews.weekly", "Weekly Review Checklist", weekly_checklist, bar=b),
        Page("reviews.scorecard", "Life Area Scorecard", scorecard(cal), bar=b),
    ])


# ------------------------------------------------------------------- ARCHIVE
ARCHIVE_BAR = [("ARCHIVE GUIDE", "archive.guide")]


def archive_guide(c: Ctx):
    return [
        c.note("Finished items move here, never to the bin, so every link to them keeps working."),
        c.h2("How to archive"),
        c.table(["Item", "How", "Where"], [
            ["Past quarter", "Right-click the quarter section → Move or Copy → Move", "[[Past Periods|archive.periods]]"],
            ["Finished project", "Move the whole project section", "[[Completed Projects|archive.projects]]"],
            ["Completed goal", "Right-click the goal page → Move or Copy → Move", "[[Completed Goals|archive.goals]]"],
            ["Past client, old notes", "Move the page", "[[Past Clients & Notes|archive.clients]]"],
        ], widths=[140, 300, 200], shade_first=True),
        c.h2("Archive index"),
        c.table(["Date archived", "Item", "Moved to"], [], widths=[110, 330, 200], blank=8),
    ]


def archive_about(what: str):
    def body(c: Ctx):
        return [c.note(f"{what} Moved here from their original place. See the [[Archive Guide|archive.guide]].")]
    return body


def archive_group() -> Group:
    b = ARCHIVE_BAR
    return Group("archive", "15 ARCHIVE", [
        Section("archive.guide.sec", "Archive Guide", [Page("archive.guide", "Archive Guide", archive_guide, bar=b)]),
        Section("archive.periods.sec", "Past Periods",
                [Page("archive.periods", "About Past Periods", archive_about("Finished quarter sections."), bar=b)]),
        Section("archive.projects.sec", "Completed Projects",
                [Page("archive.projects", "About Completed Projects",
                      archive_about("Finished project sections."), bar=b)]),
        Section("archive.goals.sec", "Completed Goals",
                [Page("archive.goals", "About Completed Goals", archive_about("Completed goal pages."), bar=b)]),
        Section("archive.clients.sec", "Past Clients & Notes",
                [Page("archive.clients", "About Past Clients & Notes",
                      archive_about("Past client pages and old notes."), bar=b)]),
    ])
