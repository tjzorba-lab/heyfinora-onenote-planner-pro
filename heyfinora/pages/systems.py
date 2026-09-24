"""04 TASKS, 05 GOALS, 06 HABITS."""
from __future__ import annotations

from typing import Optional

from ..core import Ctx, Page, Section
from ..dates import MON3, Calendar, Month
from .common import LIFE_AREAS, STATUSES

# --------------------------------------------------------------------- TASKS
TASK_BAR = [("TASK DASHBOARD", "tasks.dashboard"), ("INBOX", "tasks.inbox"),
            ("ACTION LIST", "tasks.actions"), ("WAITING FOR", "tasks.waiting")]


def task_dashboard(c: Ctx):
    return [
        c.note("Capture in the Inbox → sort onto the Action List → commit on the Week page → do on the "
               "Day page → log when done. **Move, don't copy:** a task sits in one place at a time."),
        c.h2("The flow"),
        c.table(["Step", "Where", "When"], [
            ["1 Capture", "[[Inbox|tasks.inbox]] or [[Quick Notes|notes.quick]]", "Any time"],
            ["2 Process", "Under 2 min → do it · actionable → Action List · someone else → Waiting For · "
                          "multi-step → a project · not now → Someday / Maybe", "Weekly Review"],
            ["3 Commit", "This week's Week page (Big 3 + commitments)", "Sunday"],
            ["4 Do", "Day page Top 3 + tasks", "Each morning"],
            ["5 Log", "[[Completed Log|tasks.done]]; unfinished → back to the Action List", "Shutdown / weekly"],
        ], widths=[90, 420, 130], shade_first=True),
        c.h2("Tag legend"),
        c.table(["Tag", "Meaning", "Shortcut"], [
            ["☐ To Do", "Any task", "Ctrl+1 / Cmd+1"],
            ["★ Important", "High priority", "Ctrl+2 / Cmd+2"],
            ["? Question", "Needs an answer or decision", "Ctrl+3 / Cmd+3"],
            ["⌛ Waiting For", "Blocked on someone (custom tag)", "[[setup|start.tags]]"],
        ], widths=[140, 300, 200], shade_first=True),
        c.h2("Task pages"),
        c.bullets(["[[Inbox|tasks.inbox]] – anything unprocessed; emptied weekly",
                   "[[Action List|tasks.actions]] – every standalone next action",
                   "[[Waiting For|tasks.waiting]] – delegated items",
                   "[[Recurring Tasks|tasks.recurring]] – routines by frequency",
                   "[[Someday / Maybe|tasks.someday]] – ideas not committed",
                   "[[Completed Log|tasks.done]] – ticked items by month"]),
        c.small("Project tasks stay in their project's Plan & Timeline page and surface through tags."),
    ]


def inbox(c: Ctx):
    return [
        c.note("Write anything here, fast. No sorting now – you empty this page in the Weekly Review."),
        c.blank_todos(20),
    ]


def action_list(c: Ctx):
    head = ["Task", "Life area", "Due", "Priority"]
    w = [30, 330, 120, 90, 70]
    return [
        c.note("Every standalone next action, in three horizons. Star (Ctrl+2) the high-priority ones. "
               "On Sunday, move this week's picks to the Week page."),
        c.h2("This Week"), c.todo_table(head, blank=8, widths=w),
        c.h2("Next 30 Days"), c.todo_table(head, blank=8, widths=w),
        c.h2("Later"), c.todo_table(head, blank=8, widths=w),
        c.small("Sort rows on Windows: select the table → Table Layout → Sort."),
    ]


def waiting_for(c: Ctx):
    return [
        c.note("Things someone else owes you. Review every week; chase on the follow-up date."),
        c.todo_table(["What", "Who", "Date asked", "Follow up", "Source (meeting / client)"], blank=10,
                     widths=[30, 200, 110, 80, 80, 140]),
    ]


def recurring(c: Ctx):
    blocks = [
        ("Daily", ["Check calendar and Inbox", "Tick habits in the tracker"]),
        ("Weekly", ["Weekly Review (Sunday)", "Plan meals and groceries", "Back up files"]),
        ("Monthly", ["Month Review and budget close", "Pay bills / check subscriptions"]),
        ("Quarterly", ["Quarter Review and scorecard", "Review insurance and renewals"]),
        ("Yearly", ["Year-End Review", "Tax documents", "Health check-up"]),
    ]
    out = [c.note("During the Weekly Review, copy the items due this week onto the Week page's Recurring box.")]
    for name, items in blocks:
        out.append(c.h2(name))
        out.append(c.table(["Task", "Day / date", "Life area"], [[i, "", ""] for i in items],
                           widths=[340, 150, 150], blank=3))
    return out


def someday(c: Ctx):
    return [
        c.note("Ideas you're not committing to yet. Scan monthly: promote to the Action List, "
               "[[Project Pipeline|projects.pipeline]] or [[Opportunity Lab|work.opportunity]] – or delete."),
        c.table(["Idea", "Life area", "Added", "Review note"], [], widths=[300, 130, 90, 120], blank=12),
    ]


def completed_log(cal: Calendar):
    def body(c: Ctx):
        out = [c.note("In the Weekly Review, move ticked tasks here under the month. "
                      "Read it in reviews – it's proof of progress.")]
        for m in reversed(cal.months):
            out.append(c.h3(f"{m.name} {m.year}"))
            out.append(c.p())
        return out
    return body


def tasks_section(cal: Calendar) -> Section:
    b = TASK_BAR
    return Section("tasks.sec", "04 TASKS", [
        Page("tasks.dashboard", "Task Dashboard", task_dashboard, bar=b),
        Page("tasks.inbox", "Inbox", inbox, bar=b),
        Page("tasks.actions", "Action List", action_list, bar=b),
        Page("tasks.waiting", "Waiting For", waiting_for, bar=b),
        Page("tasks.recurring", "Recurring Tasks", recurring, bar=b),
        Page("tasks.someday", "Someday / Maybe", someday, bar=b),
        Page("tasks.done", "Completed Log", completed_log(cal), bar=b),
    ])


# --------------------------------------------------------------------- GOALS
GOAL_BAR = [("GOALS DASHBOARD", "goals.dashboard"), ("LIFE VISION", "goals.vision")]


def goals_dashboard(cal: Calendar):
    def body(c: Ctx):
        out = [c.note("Up to 7 goals a year, up to 3 active per quarter. Update the status and % "
                      "in each Month Review – OneNote does not calculate them."),
               c.small(f"Status: {STATUSES}")]
        for y in cal.years:
            months = [MON3[m.month] for m in cal.months_of(y)]
            out.append(c.h2(f"Active goals {y}"))
            out.append(c.table(["Goal (link)", "Area", "Deadline", "Status"] + months, [],
                               widths=[150, 70, 70, 70] + [36] * len(months), blank=5))
        out += [c.h2("Completed goals"),
                c.table(["Goal", "Completed", "Result"], [], widths=[260, 100, 280], blank=3),
                c.p("Finished goal pages move to [[Archive › Completed Goals|archive.goals]].")]
        return out
    return body


def life_vision(c: Ctx):
    return [
        c.note("Where am I heading in 3 years? One line per life area, written as if it's already true."),
        c.table(["Life area", "In 3 years…"], [[a, ""] for a in LIFE_AREAS], widths=[150, 490], shade_first=True),
        c.h2("My vision in one paragraph"), c.p(), c.p(),
        c.h2("What I will not trade for it"), c.p(),
    ]


def annual_goals(y: int, example_key: Optional[str]):
    def body(c: Ctx):
        span = "July–December" if y == 2026 else "January–December"
        out = [c.note(f"{y} goals ({span}). 3–7 goals, each with a measure and a deadline. Create a goal page "
                      "for each from [[TEMPLATE · Goal Page|tpl.goal]] as a subpage under this page."),
               c.lines(["Theme of the year", "Why these goals"]),
               c.table(["#", "Goal (link to goal page)", "Life area", "Measure", "Deadline"],
                       [[str(i), "", "", "", ""] for i in range(1, 8)], widths=[30, 260, 110, 140, 100])]
        if example_key:
            out.append(c.p(f"See a filled-in example: [[EXAMPLE – Goal page|{example_key}]]"))
        out.append(c.p(f"Break goals into quarter objectives on each [[Quarter Plan|@quarter]]."))
        return out
    return body


def goal_page_body(example: bool):
    def v(s: str) -> str:
        return s if example else ""

    def body(c: Ctx):
        out = []
        if example:
            out.append(c.note("EXAMPLE – read it, then delete or archive it when you've written your own."))
        out += [
            c.h2("Goal statement"),
            c.table(["", ""], [
                ["**Outcome**", v("Grow my side business to a steady monthly income")],
                ["**Measure**", v("Monthly revenue")],
                ["**Target**", v("1,000 per month for 3 months in a row")],
                ["**Deadline**", v("December 2027")],
                ["**Life area**", v("Business")],
            ], widths=[140, 500], header=False),
            c.h2("Why it matters"),
            c.p(v("Extra income gives me choices, and I want to prove I can build something of my own.")),
            c.p(v("Success looks like: repeat customers, a simple website, 5 hours a week of focused work.")),
            c.h2("Milestones"),
            c.table(["Milestone", "Target date", "Done"],
                    [[v("Website launched"), v("Oct 2026"), "[ ]"],
                     [v("First 10 customers"), v("Jan 2027"), "[ ]"],
                     [v("500 a month"), v("Jun 2027"), "[ ]"],
                     [v("1,000 a month × 3"), v("Dec 2027"), "[ ]"]], widths=[380, 160, 100]),
            c.h2("Action plan"),
            c.small("The first 3 next actions go to the [[Action List|tasks.actions]]."),
            c.todos([v("Choose website platform"), v("Write the About page"), v("List 20 people to tell")]),
            c.lines(["Linked projects", "Linked habits"]),
        ]
        if example:
            out.append(c.p("Project: [[EXAMPLE – Website Launch|projects.example.home]] · "
                           "Habit: 5 hours of business work each week"))
        out += [
            c.h2("Obstacles and if-then plans"),
            c.table(["If…", "then I will…"],
                    [[v("I'm too tired after work"), v("do 25 minutes before work instead")],
                     [v("sales are slow for a month"), v("ask 5 past customers for feedback")], ["", ""]],
                    widths=[300, 340]),
            c.h2("Progress log"),
            c.table(["Month", "% complete", "One-line note"],
                    [[v("Sep 2026"), v("10%"), v("Platform chosen; domain bought")], ["", "", ""], ["", "", ""]],
                    widths=[120, 100, 420]),
            c.h2("Close-out"),
            c.lines(["Result", "What worked", "What I'd change"]),
        ]
        return out
    return body


def goals_section(cal: Calendar) -> Section:
    b = GOAL_BAR
    pages = [Page("goals.dashboard", "Goals Dashboard", goals_dashboard(cal), bar=b),
             Page("goals.vision", "Life Vision", life_vision, bar=b)]
    for i, y in enumerate(cal.years):
        last = i == len(cal.years) - 1
        label = f"{y} Goals (H2)" if cal.months_of(y)[0].month == 7 else f"{y} Goals"
        pages.append(Page(f"goals.{y}", label, annual_goals(y, "goals.example" if last else None),
                          bar=b + [(f"{y} GOALS", f"goals.{y}")]))
    pages.append(Page("goals.example", "EXAMPLE – Goal page", goal_page_body(True), level=2, bar=b))
    return Section("goals.sec", "05 GOALS", pages)


# -------------------------------------------------------------------- HABITS
HABIT_BAR = [("HABIT DASHBOARD", "habits.dashboard"), ("HABIT DESIGN", "habits.design"),
             ("ROUTINES", "habits.routines")]


def habit_dashboard(cal: Calendar):
    def body(c: Ctx):
        out = [c.note("One row per habit, one column per month: consistency % = days done ÷ days in month. "
                      "Fill it in the Month Review. Recommended: no more than 5 active habits.")]
        for y in cal.years:
            ms = cal.months_of(y)
            out.append(c.h2(f"{y}"))
            out.append(c.table(["Habit", "Serves goal"] + [MON3[m.month] for m in ms], [],
                               widths=[140, 100] + [max(34, 400 // len(ms))] * len(ms), blank=5))
            out.append(c.p("Trackers: " + " · ".join(f"[[{MON3[m.month]}|{m.habits_key}]]" for m in ms)))
        return out
    return body


def habit_design(c: Ctx):
    out = [c.note("Design each habit once. Make the minimum version so small you can't fail.")]
    for i in range(1, 6):
        out.append(c.h3(f"Habit {i}"))
        out.append(c.lines(["Habit", "Why (goal it serves)", "Cue (after I…)", "Minimum version",
                            "Time / place", "Reward"]))
    return out


def routines(c: Ctx):
    r = {
        "Morning": ["Water + light", "Review today's Top 3", "Move for 10 minutes", "Tick the habit tracker"],
        "Evening": ["Tidy for 10 minutes", "Lay out tomorrow", "Screens off", "Read"],
        "Weekly reset": ["Laundry and groceries", "Clean desk and downloads", "[[Weekly Review|reviews.weekly]]"],
        "Work shutdown": ["Process email to zero or to the Inbox", "Update the Day page",
                          "Pick tomorrow's Top 3", "Close all tabs"],
    }
    out = [c.note("Edit these to fit you. The Day page has one “Routine done” box for each.")]
    for name, items in r.items():
        out += [c.h2(name), c.todos(items + ["", ""])]
    return out


def habit_tracker(m: Month):
    def body(c: Ctx):
        rows = [[f"{m.date(d).strftime('%a')} {d}"] + ["[ ]"] * 6 + ["", "", "", ""]
                for d in range(1, m.days + 1)]
        rows.append(["**Total**"] + [""] * 10)
        return [
            c.table(["Habit →", "", "", "", "", "", ""], [["Name"] + [""] * 6],
                    widths=[70] + [55] * 6, header_bg=c.t["teal"]),
            c.small("Write your habits in the top row, then tick each day. Energy and Mood 1–5; Sleep in hours."),
            c.table(["Day", "H1", "H2", "H3", "H4", "H5", "H6", "Energy", "Mood", "Sleep", "Note"], rows,
                    widths=[70, 38, 38, 38, 38, 38, 38, 50, 45, 45, 150]),
            c.p(f"Month-end: copy consistency % to the [[Habit Dashboard|habits.dashboard]] in the "
                f"[[Month Review|{m.review_key}]]."),
        ]
    return body


def habits_section(cal: Calendar) -> Section:
    b = HABIT_BAR
    pages = [Page("habits.dashboard", "Habit Dashboard", habit_dashboard(cal), bar=b),
             Page("habits.design", "Habit Design", habit_design, bar=b),
             Page("habits.routines", "Routines", routines, bar=b)]
    for y in cal.years:
        pages.append(Page(f"habits.{y}", f"{y} Trackers",
                          lambda c, y=y: [c.note(f"Monthly habit trackers for {y} are the subpages below.")],
                          bar=b))
        for m in cal.months_of(y):
            pm, nm = cal.prev_month(m), cal.next_month(m)
            pages.append(Page(m.habits_key, f"{m.label} Habit Tracker", habit_tracker(m), level=2,
                              bar=b + [("MONTH", m.key), ("◀ PREV", pm.habits_key if pm else None),
                                       ("NEXT ▶", nm.habits_key if nm else None)]))
    return Section("habits.sec", "06 HABITS", pages)
