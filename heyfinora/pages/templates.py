"""14 TEMPLATE LIBRARY: blank templates that link only to fixed hubs."""
from __future__ import annotations

from ..core import Ctx, Group, Page, Section
from . import plan
from .money import budget_body, money_plan
from .projects_work import kit_pages
from .systems import goal_page_body

T = "TEMPLATE · "
TPL_BAR = [("TEMPLATE INDEX", "tpl.guide"), ("HOME", "home.dashboard")]
DAY_BAR = [("TODAY'S PLAN", "home.dashboard"), ("ACTION LIST", "tasks.actions"), ("INBOX", "tasks.inbox"),
           ("HABITS", "habits.dashboard"), ("JOURNAL", "journal.home")]

RENAME_DAY = "Copy me under this week's page, then rename: YYYY-MM-DD · Weekday."


def _hours(c: Ctx, start: int = 6, end: int = 21) -> str:
    return c.table(["Time", "Plan", "Done"], [[f"{h:02d}:00", "", "[ ]"] for h in range(start, end + 1)],
                   widths=[70, 480, 90], shade_first=True)


def daily_standard(c: Ctx):
    return [
        c.small(RENAME_DAY),
        c.h2("Top 3"), c.blank_todos(3),
        c.h2("Time blocks"), _hours(c),
        c.h2("Tasks"), c.small("From this week's commitments."), c.blank_todos(6),
        c.h2("Routines"), c.todos(["Morning routine", "Evening routine", "Work shutdown"]),
        c.h2("Notes"), c.p(), c.p(),
        c.h2("Reflection"), c.lines(["Grateful for", "Today's win", "One lesson", "Energy (1–5)"]),
        c.h2("Shutdown"),
        c.todos(["Unfinished tasks moved to tomorrow or back to the [[Action List|tasks.actions]]",
                 "Tomorrow's Top 3 chosen", "Habits ticked"]),
    ]


def daily_work(c: Ctx):
    return [
        c.small(RENAME_DAY),
        c.h2("Top 3 work outcomes"), c.blank_todos(3),
        c.h2("Deep work blocks"),
        c.table(["Time", "Focus", "Done"], [["", "", "[ ]"]] * 3, widths=[110, 440, 90]),
        c.h2("Meetings"),
        c.table(["Time", "Meeting (link)", "Actions captured"], [["", "", "[ ]"]] * 4, widths=[90, 420, 130]),
        c.h2("Work tasks"), c.blank_todos(6),
        c.h2("Personal must-dos"), c.blank_todos(3),
        c.h2("Shutdown"),
        c.todos(["Email processed", "Actions moved to [[Action List|tasks.actions]] / [[Waiting For|tasks.waiting]]",
                 "Tomorrow's Top 3 chosen"]),
        c.lines(["Today's win", "Energy (1–5)"]),
    ]


def daily_minimal(c: Ctx):
    return [c.small(RENAME_DAY), c.h2("Top 3"), c.blank_todos(3), c.h2("Tasks"), c.blank_todos(5),
            c.h2("One line"), c.p()]


def library_guide(sections: list[Section]):
    def body(c: Ctx):
        out = [
            c.note("Never type into a template. Copy it, move the copy where it belongs, then rename it. "
                   "Every template title starts with TEMPLATE · so an unrenamed copy is easy to spot."),
            c.h2("Three ways to duplicate"),
            c.table(["Method", "Works on", "Steps", "Best for"], [
                ["Copy page", "All apps", "Right-click the template page → Copy (or Move or Copy → Copy) → "
                                          "choose section → rename", "Any single template"],
                ["Section default template", "Windows desktop",
                 "Insert → Page Templates → Save current page as a template → set it as the default for "
                 "each quarter section", "Days: + Page makes a ready day page"],
                ["Copy section", "Windows, Mac", "Right-click the Project Kit section → Move or Copy → "
                                                 "Copy into PROJECTS → rename", "New projects"],
            ], widths=[120, 100, 300, 120]),
            c.h2("Duplicate regularly"),
            c.p("Daily (every day) · Meeting Notes · Goal Page · Project Kit · Client Page · Brain Dump · "
                "Journal Entry. The rest exist to extend the planner past December 2027."),
            c.h2("Index"),
        ]
        rows = []
        for s in sections[1:]:
            rows.append([f"**{s.name}**", " · ".join(f"[[{p.title.replace(T, '')}|{p.key}]]" for p in s.pages)])
        out.append(c.table(["Section", "Templates"], rows, widths=[140, 500], shade_first=True))
        return out
    return body


def habit_card(c: Ctx):
    return [c.lines(["Habit", "Why (goal it serves)", "Cue (after I…)", "Minimum version", "Time / place",
                     "Reward", "Start date"])]


def habit_tracker_blank(c: Ctx):
    rows = [[str(d)] + ["[ ]"] * 6 + ["", "", "", ""] for d in range(1, 32)]
    return [c.small("Rename: YYYY-MM · Month Habit Tracker. Write the weekday next to each day."),
            c.table(["Day", "H1", "H2", "H3", "H4", "H5", "H6", "Energy", "Mood", "Sleep", "Note"], rows,
                    widths=[50, 38, 38, 38, 38, 38, 38, 50, 45, 45, 170])]


def biz_review(c: Ctx):
    return [
        c.small("Rename: Qn YYYY · Business Review and place it under Work HQ › Business Reviews."),
        c.h2("Numbers"),
        c.table(["", "Target", "Actual"], [["Revenue", "", ""], ["Profit", "", ""], ["New customers", "", ""],
                                           ["Email list", "", ""]], widths=[220, 210, 210], shade_first=True),
        c.lines(["Best-selling offer", "Best channel", "What customers said", "Biggest lesson"]),
        c.h2("Next quarter"), c.lines(["Priority 1", "Priority 2", "Stop doing"]),
    ]


def meeting(c: Ctx):
    return [
        c.small("Rename: YYYY-MM-DD · Meeting name. Add a row to the [[Meeting Index|work.meetings]]."),
        c.lines(["Date / time", "Attendees", "Project / client", "Purpose"]),
        c.h2("Agenda"), c.numbered(["", "", ""]),
        c.h2("Notes"), c.p(), c.p(),
        c.h2("Decisions"), c.bullets([""]),
        c.h2("Action items"),
        c.table(["Done", "Action", "Owner", "Due"], [["[ ]", "", "", ""]] * 5, widths=[40, 360, 120, 120]),
        c.small("In the Weekly Review, move your actions to the Action List and others' to Waiting For; "
                "note “moved to Tasks” here."),
    ]


def one_on_one(c: Ctx):
    return [
        c.small("One running page per person or series. Newest meeting at the top."),
        c.lines(["Person / series", "Cadence", "Shared goals"]),
        c.h2("YYYY-MM-DD"),
        c.table(["Topic", "Notes"], [["Wins", ""], ["Updates", ""], ["Blockers", ""], ["Feedback", ""]],
                widths=[140, 500], shade_first=True),
        c.table(["Done", "Action", "Owner", "Due"], [["[ ]", "", "", ""]] * 3, widths=[40, 360, 120, 120]),
    ]


def client_page(c: Ctx):
    return [
        c.small("Rename to the client name. Add it to the [[Client Directory|work.clients]]."),
        c.h2("Profile"), c.lines(["Contact", "Company", "Email / phone", "Service", "Start date", "Value band"]),
        c.h2("Scope"), c.p(),
        c.h2("Deliverables"),
        c.table(["Done", "Deliverable", "Due"], [["[ ]", "", ""]] * 5, widths=[40, 460, 140]),
        c.h2("Communication log"),
        c.table(["Date", "Channel", "Summary", "Next step"], [], widths=[80, 90, 300, 170], blank=6),
        c.h2("Files & links"), c.bullets([""]),
    ]


def sop(c: Ctx):
    return [
        c.small("Rename: SOP · What it does. Add it to the [[SOP Library|work.sops]]."),
        c.lines(["Purpose", "Trigger (when to use it)", "Tools", "Owner", "Last updated"]),
        c.h2("Steps"), c.todos(["", "", "", "", "", ""]),
        c.h2("Notes & gotchas"), c.p(),
    ]


def content_calendar(c: Ctx):
    return [
        c.small("Rename: YYYY-MM · Content Calendar. Place it in Work & Business › Content."),
        c.table(["Date", "Channel", "Piece", "Status", "Link"], [], widths=[80, 110, 250, 90, 110], blank=20),
        c.small("Status: Idea · Drafting · Scheduled · Published"),
    ]


def content_brief(c: Ctx):
    return [c.lines(["Title", "Pillar", "Audience", "Goal (what they'll do)", "Format / channel", "Key points",
                     "Call to action", "Due date"]),
            c.h2("Outline"), c.numbered(["", "", ""])]


def opportunity_card(c: Ctx):
    return [
        c.lines(["Idea", "Problem it solves", "Who has the problem", "How I'd test it cheaply"]),
        c.table(["Criterion", "Score 1–5", "Notes"], [[x, "", ""] for x in
                ["Demand", "Fit with my skills", "Revenue potential", "Effort (5 = easy)", "Time to first sale"]] +
                [["**Total**", "", ""]], widths=[200, 100, 340], shade_first=True),
        c.lines(["Decision (Test / Park / Drop)", "Next step"]),
    ]


def brain_dump(c: Ctx):
    return [
        c.small("Rename: YYYY-MM-DD · Brain Dump. Write everything, then process it."),
        c.p(), c.p(), c.p(), c.p(),
        c.h2("Process"),
        c.todos(["Tasks → [[Inbox|tasks.inbox]]", "Ideas → [[Idea Vault|notes.ideas]]",
                 "Information → [[Knowledge Base|notes.kb]]", "Everything else deleted"]),
    ]


def research_note(c: Ctx):
    return [c.lines(["Question", "Why it matters"]),
            c.h2("Sources"), c.table(["Source (link)", "Key point"], [], widths=[260, 380], blank=5),
            c.h2("Findings"), c.p(), c.lines(["Conclusion", "Next step"])]


def kb_article(c: Ctx):
    return [c.small("Title it “How I …” or the topic name. Add it to the [[KB Index|notes.kb]]."),
            c.lines(["Summary (2 lines)", "Tags / related"]),
            c.h2("Details"), c.p(), c.p(), c.h2("Steps / examples"), c.numbered(["", "", ""])]


def book_notes(c: Ctx):
    return [c.small("Place as a subpage under the [[Reading List|growth.reading]]."),
            c.lines(["Book", "Author", "Finished", "Rating (1–5)"]),
            c.h2("The big idea"), c.p(),
            c.h2("Key points"), c.bullets(["", "", ""]),
            c.h2("Quotes, in my words"), c.bullets(["", ""]),
            c.h2("Actions"), c.todos(["", ""]),
            c.lines(["Would I reread it?"])]


def course_notes(c: Ctx):
    return [c.small("Place as a subpage under the [[Course Tracker|growth.courses]]."),
            c.lines(["Course", "Module"]),
            c.h2("Notes"), c.p(), c.p(),
            c.h2("Key ideas"), c.bullets(["", "", ""]),
            c.h2("Actions to apply"), c.todos(["", ""])]


def journal_entry(c: Ctx):
    return [c.small("Rename: YYYY-MM-DD · Title. Place under its month divider in the [[Journal|journal.home]]."),
            c.lines(["Prompt (optional)", "Mood (1–5)"]), c.p(), c.p(), c.p(), c.p()]


def blank_page(c: Ctx):
    return [c.p(), c.p(), c.p()]


def template_group() -> Group:
    def pg(key, title, fn, bar=TPL_BAR):
        return Page(key, T + title, fn, bar=bar)

    sections = [
        Section("tpl.planning", "Planning", [
            pg("tpl.daily", "Daily – Standard", daily_standard, DAY_BAR),
            pg("tpl.daily.work", "Daily – Work Focus", daily_work, DAY_BAR),
            pg("tpl.daily.min", "Daily – Minimal", daily_minimal, DAY_BAR),
            pg("tpl.week", "Weekly", plan.week_body(None, None)),
            pg("tpl.month", "Month Dashboard", plan.month_dashboard_body(None, None)),
            pg("tpl.quarter", "Quarter Plan", plan.quarter_plan_body(None, None, None)),
            pg("tpl.year", "Year Dashboard", plan.year_dashboard_body(None, None)),
        ]),
        Section("tpl.reviews", "Reviews", [
            pg("tpl.monthreview", "Month Review", plan.month_review_body(None, None)),
            pg("tpl.quarterreview", "Quarter Review", plan.quarter_review_body(None, None, None)),
            pg("tpl.yearreview", "Year-End Review", plan.year_review_body(None, None)),
            pg("tpl.bizreview", "Business Review", biz_review),
        ]),
        Section("tpl.goals", "Goals & Habits", [
            pg("tpl.goal", "Goal Page", goal_page_body(False)),
            pg("tpl.habittracker", "Monthly Habit Tracker", habit_tracker_blank),
            pg("tpl.habitcard", "Habit Design Card", habit_card),
        ]),
        Section("tpl.kit", "Project Kit", kit_pages(T, "tpl.kit", False)),
        Section("tpl.meetings", "Meetings & Clients", [
            pg("tpl.meeting", "Meeting Notes", meeting),
            pg("tpl.oneonone", "Recurring Meeting / 1:1", one_on_one),
            pg("tpl.client", "Client Page", client_page),
        ]),
        Section("tpl.business", "Business", [
            pg("tpl.sop", "SOP", sop),
            pg("tpl.contentcal", "Content Calendar", content_calendar),
            pg("tpl.brief", "Content Brief", content_brief),
            pg("tpl.opportunity", "Opportunity Scorecard", opportunity_card),
        ]),
        Section("tpl.money", "Money", [
            pg("tpl.budget", "Monthly Budget", budget_body(None)),
            pg("tpl.moneyplan", "Money Plan & Review", money_plan(None)),
        ]),
        Section("tpl.notes", "Notes & Journal", [
            pg("tpl.braindump", "Brain Dump", brain_dump),
            pg("tpl.research", "Research Note", research_note),
            pg("tpl.kb", "Knowledge Article", kb_article),
            pg("tpl.book", "Book Notes", book_notes),
            pg("tpl.course", "Course Notes", course_notes),
            pg("tpl.journal", "Journal Entry", journal_entry),
            pg("tpl.blank", "Blank HEYFINORA Page", blank_page),
        ]),
    ]
    guide = Section("tpl.guide.sec", "Library Guide", [])
    all_sections = [guide] + sections
    guide.pages.append(Page("tpl.guide", "Template Index & How to Copy", library_guide(all_sections),
                            bar=[("HOME", "home.dashboard")]))
    return Group("tpl", "14 TEMPLATE LIBRARY", all_sections)
