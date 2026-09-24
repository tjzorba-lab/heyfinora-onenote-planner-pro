"""02/03 PLAN groups: Year, Quarter, Month, Week pages and their reviews.

Every body function also works with no period (None) so the Template
Library can reuse it for the blank templates that extend the planner.
"""
from __future__ import annotations

import calendar
from typing import Optional

from ..core import Ctx, Group, Page, Section
from ..dates import MON3, MONTHS, Calendar, Month, Week, quarter_key
from .common import DAY_NAMES, LIFE_AREAS, STATUSES


def _k(cal: Optional[Calendar], key: str) -> Optional[str]:
    """Only link dated pages when rendering the dated (non-template) version."""
    return key if cal is not None else None


# ---------------------------------------------------------------- year pages
def year_dashboard_body(cal: Optional[Calendar], y: Optional[int]):
    def body(c: Ctx):
        yl = str(y) if y else "YYYY"
        qrows = []
        for q in range(1, 5):
            names = " · ".join(MONTHS[m][:3] for m in range(3 * q - 2, 3 * q + 1))
            has = cal is not None and q in cal.quarters_of(y)
            qk = quarter_key(y, q) if has else None
            qrows.append([f"Q{q}", names,
                          f"[[Quarter Plan|{qk}]]" if qk else "—",
                          f"[[Quarter Review|{qk}.review]]" if qk else "—", ""])
        return [
            c.note("Decide what this year is about. Keep it to one theme and 3–7 goals; "
                   "the quarters, months and weeks below turn them into action."),
            c.h2("Theme of the year"),
            c.lines(["Theme word or phrase", "Why this theme", f"At the end of {yl} I will feel…"]),
            c.h2("Top goals"),
            c.table(["Goal (link the goal page)", "Life area", "Deadline", "Status"], [],
                    widths=[300, 130, 100, 110], blank=5),
            c.p(f"Full list and goal pages: [[{yl} Goals|goals.{y}]]" if y else
                "Full list and goal pages: [[Goals Dashboard|goals.dashboard]]"),
            c.small(f"Status: {STATUSES}"),
            c.h2("Quarters"),
            c.table(["Quarter", "Months", "Plan", "Review", "Focus in one line"], qrows,
                    widths=[60, 130, 110, 110, 230]),
            c.h2("Key numbers"),
            c.table(["Number to watch", "Start", "Target", "Q1", "Q2", "Q3", "Q4"],
                    [[n, "", "", "", "", "", ""] for n in
                     ["Savings", "Debt", "Net worth", "Business revenue", "Workouts / week", "Books read"]],
                    widths=[170, 70, 70, 70, 70, 70, 70], blank=2),
            c.small("OneNote tables do not calculate. On Windows, type a sum such as 1250+380= "
                    "and press Enter to work it out inline."),
            c.h2("Year pages"),
            c.bullets([
                f"[[Year at a Glance|{_k(cal, f'plan.{y}.glance')}]] – mini calendars linking every month and week",
                f"[[Important Dates & Events|{_k(cal, f'plan.{y}.dates')}]]",
                f"[[Year-End Review|{_k(cal, f'plan.{y}.review')}]]",
                f"[[Money Plan & Review|{_k(cal, f'money.plan.{y}')}]] · [[Goals|goals.dashboard]] · "
                "[[Habits|habits.dashboard]] · [[Review Hub|reviews.hub]]",
            ]),
        ]
    return body


def _mini_month(c: Ctx, cal: Calendar, m: Month) -> str:
    rows = []
    for week in calendar.Calendar(0).monthdatescalendar(m.year, m.month):
        iy, iw, _ = week[0].isocalendar()
        w = Week(iy, iw)
        wk = f"[[{w.code}|{w.key}]]" if w in cal.weeks else w.code
        rows.append([wk] + [str(d.day) if d.month == m.month else "" for d in week])
    return (c.h3(f"[[{m.name}|{m.key}]]") +
            c.table(["Wk", "M", "T", "W", "T", "F", "S", "S"], rows,
                    widths=[34] + [24] * 7, header_bg=c.t["teal"]))


def glance_body(cal: Calendar, y: int):
    def body(c: Ctx):
        months = cal.months_of(y)
        cells = [_mini_month(c, cal, m) for m in months]
        grid = ['<table style="border-collapse:collapse">']
        for i in range(0, len(cells), 3):
            tds = "".join(f'<td style="width:250px">{x}</td>' for x in cells[i:i + 3])
            grid.append(f"<tr>{tds}</tr>")
        grid.append("</table>")
        return [c.note("Click a month name to open its Month Dashboard, or a week number (W27) "
                       "to open that week. Weeks belong to the month that holds their Thursday."),
                "".join(grid)]
    return body


def important_dates_body(cal: Calendar, y: int):
    def body(c: Ctx):
        out = [c.note("Birthdays, anniversaries, holidays, renewals and deadlines. Copy this month's "
                      "dates into the Month Dashboard's Key dates box. Bill renewals also live in "
                      "[[Bills & Subscriptions|money.bills]].")]
        for m in cal.months_of(y):
            out.append(c.h3(f"[[{m.name} {y}|{m.key}]]"))
            out.append(c.table(["Date", "Event", "Type", "Reminder set"], [],
                               widths=[80, 330, 130, 100], blank=3))
        out.append(c.small("Type: Birthday · Anniversary · Holiday · Renewal · Deadline · Travel · Other"))
        return out
    return body


def year_review_body(cal: Optional[Calendar], y: Optional[int]):
    def body(c: Ctx):
        yl = str(y) if y else "YYYY"
        nxt = str(y + 1) if y else "next year"
        return [
            c.note(f"Block 90 minutes in the last week of {yl}. Read your four Quarter Reviews and the "
                   "[[Review Hub|reviews.hub]] log first."),
            c.h2("The year in one paragraph"), c.p(), c.p(),
            c.h2("Goal results"),
            c.table(["Goal", "Result", "% done", "What made the difference"], [],
                    widths=[200, 180, 70, 190], blank=7),
            c.h2("Life areas"),
            c.table(["Life area", "Score now (1–10)", "Best moment", "Next year I want…"],
                    [[a, "", "", ""] for a in LIFE_AREAS], widths=[140, 110, 190, 200], shade_first=True),
            c.p("Scores over time: [[Life Area Scorecard|reviews.scorecard]]"),
            c.h2("Top 10 wins"), c.numbered([""] * 10),
            c.h2("Lessons: keep · change · stop"),
            c.table(["Keep doing", "Change", "Stop doing"], [], widths=[213, 213, 214], blank=4),
            c.h2("Money"),
            c.p(f"Complete the year-end half of [[Money Plan & Review|{_k(cal, f'money.plan.{y}')}]]."),
            c.h2(f"Looking ahead to {nxt}"),
            c.lines(["Theme", "Goal 1", "Goal 2", "Goal 3", "First step in January"]),
            c.h2("Close the year"),
            c.todos(["Update the [[Goals Dashboard|goals.dashboard]] and move finished goals to Archive",
                     "Move finished projects to [[Archive|archive.guide]]",
                     "Repoint the Master Dashboard's This Year link",
                     "Add this review to the [[Review Hub|reviews.hub]] log"]),
        ]
    return body


# ------------------------------------------------------------- quarter pages
def quarter_plan_body(cal: Optional[Calendar], y: Optional[int], q: Optional[int]):
    def body(c: Ctx):
        months = cal.months_in_quarter(y, q) if cal else []
        mrows = ([[f"[[{m.name}|{m.key}]]", "", f"[[Review|{m.review_key}]]"] for m in months]
                 or [["Month 1", "", ""], ["Month 2", "", ""], ["Month 3", "", ""]])
        return [
            c.note("One decision, one page: up to 3 objectives, the priorities and projects that move "
                   "them, and the milestones to hit. Objectives come from your "
                   f"[[annual goals|{_k(cal, f'goals.{y}') or 'goals.dashboard'}]]."),
            c.h2("Objectives (up to 3)"),
            c.table(["Objective", "Serves goal", "Measure", "Target", "Status"], [],
                    widths=[200, 130, 130, 80, 100], blank=3),
            c.h2("Priorities"),
            c.table(["Priority", "Life area", "Why now"], [], widths=[260, 130, 250], blank=5),
            c.h2("Projects this quarter"),
            c.table(["Project (link)", "Goal", "Milestone due", "Status"], [],
                    widths=[220, 150, 150, 120], blank=4),
            c.p("All projects: [[Project Portfolio|projects.portfolio]]"),
            c.h2("Milestones"),
            c.table(["Date", "Milestone", "Project / goal", "Done"], [],
                    widths=[80, 300, 200, 60], blank=6),
            c.h2("Months"),
            c.table(["Month", "Focus", "Review"], mrows, widths=[140, 380, 120]),
            c.h2("Life area focus"),
            c.table(["Life area", "Focus this quarter"], [[a, ""] for a in LIFE_AREAS],
                    widths=[160, 480], shade_first=True),
        ]
    return body


def quarter_review_body(cal: Optional[Calendar], y: Optional[int], q: Optional[int]):
    def body(c: Ctx):
        return [
            c.note("45 minutes in the last week of the quarter. Read the Quarter Plan and three "
                   "Month Reviews first."),
            c.h2("Objective results"),
            c.table(["Objective", "Measure", "Result", "Score 1–10"], [],
                    widths=[230, 150, 170, 90], blank=3),
            c.h2("Projects"),
            c.table(["Project", "Status now", "Next step"], [], widths=[220, 150, 270], blank=4),
            c.h2("Life Area Scorecard"),
            c.p("Rate each area 1–10 on the [[Life Area Scorecard|reviews.scorecard]] and note the "
                "lowest two here:"),
            c.lines(["Lowest area", "One change next quarter"]),
            c.h2("Top 5 wins"), c.numbered([""] * 5),
            c.h2("Keep · change · stop"),
            c.table(["Keep", "Change", "Stop"], [], widths=[213, 213, 214], blank=3),
            c.h2("Next quarter draft"),
            c.lines(["Objective 1", "Objective 2", "Objective 3"]),
            c.h2("Close the quarter"),
            c.todos(["Move finished projects to Archive › Completed Projects",
                     "Update [[Goals Dashboard|goals.dashboard]] status",
                     "Business Review (if you run a business): [[Business Reviews|work.bizreviews]]",
                     "Log this review in the [[Review Hub|reviews.hub]]"]),
        ]
    return body


# --------------------------------------------------------------- month pages
def month_dashboard_body(cal: Optional[Calendar], m: Optional[Month]):
    def body(c: Ctx):
        rows = []
        if m:
            for week in calendar.Calendar(0).monthdatescalendar(m.year, m.month):
                iy, iw, _ = week[0].isocalendar()
                w = Week(iy, iw)
                wk = f"[[{w.code}|{w.key}]]" if w in cal.weeks else w.code
                rows.append([wk] + [f"**{d.day}**" if d.month == m.month else "" for d in week])
        else:
            rows = [[""] * 8 for _ in range(5)]
        return [
            c.h2("Calendar"),
            c.table(["Week", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], rows,
                    widths=[50] + [84] * 7),
            c.h2("Month targets (3)"),
            c.table(["Target", "Serves goal", "Measure", "Done"],
                    [["", "", "", "[ ]"]] * 3, widths=[250, 160, 160, 60]),
            c.h2("Key dates"),
            c.table(["Date", "Event"], [], widths=[100, 540], blank=4),
            c.p(f"From [[Important Dates|{_k(cal, f'plan.{m.year}.dates') if m else None}]]"),
            c.h2("Due this month"),
            c.small("Move dated items from the Action List's Next 30 Days block, or paste links to them."),
            c.blank_todos(5),
            c.h2("Project milestones this month"),
            c.table(["Milestone", "Project", "Due"], [], widths=[300, 220, 120], blank=3),
            c.h2("This month's systems"),
            c.bullets([
                f"[[Habit tracker|{_k(cal, m.habits_key) if m else 'habits.dashboard'}]]",
                f"[[Budget|{_k(cal, m.budget_key) if m else 'money.dashboard'}]]",
                f"[[Month Review|{_k(cal, m.review_key) if m else None}]]",
                "[[Action List|tasks.actions]] · [[Content Calendar|work.content]] · [[Meetings|work.meetings]]",
            ]),
            c.h2("Notes"), c.p(), c.p(),
        ]
    return body


def month_review_body(cal: Optional[Calendar], m: Optional[Month]):
    def body(c: Ctx):
        tracker = _k(cal, m.habits_key) if m else "habits.dashboard"
        budget = _k(cal, m.budget_key) if m else "money.dashboard"
        return [
            c.note("30 minutes on the last day of the month. Update the dashboards as you go; "
                   "they do not update themselves."),
            c.lines(["This month in one line", "Overall score (1–10)"]),
            c.h2("Goals"),
            c.table(["Goal", "% done now", "Status", "Note"], [], widths=[230, 90, 110, 210], blank=5),
            c.p("Copy the % into the [[Goals Dashboard|goals.dashboard]]."),
            c.h2("Month targets"),
            c.table(["Target", "Hit?", "Why / why not"], [["", "[ ]", ""]] * 3, widths=[250, 60, 330]),
            c.h2("Habits"),
            c.table(["Habit", "Days done", "Consistency %", "Keep / adjust / drop"], [],
                    widths=[200, 90, 110, 240], blank=5),
            c.p(f"From the [[habit tracker|{tracker}]]; copy % into the [[Habit Dashboard|habits.dashboard]]."),
            c.h2("Money check-in"),
            c.lines(["Income vs plan", "Spending vs plan", "Saved this month", "One money lesson"]),
            c.p(f"Details: [[this month's budget|{budget}]]"),
            c.h2("Growth"), c.lines(["What I learned", "What I'll apply"]),
            c.h2("Work & business"), c.lines(["Biggest result", "Biggest blocker", "Revenue (if any)"]),
            c.h2("Clear the decks"),
            c.todos(["Scan [[Someday / Maybe|tasks.someday]] – promote or delete",
                     "Scan [[Next 30 Days|tasks.actions]] – move dated items to next month's dashboard",
                     "Move best wins to the [[Wins & Gratitude Log|journal.wins]]",
                     "Log this review in the [[Review Hub|reviews.hub]]"]),
            c.h2("Next month's 3 targets"), c.numbered(["", "", ""]),
        ]
    return body


# ---------------------------------------------------------------- week pages
def week_body(cal: Optional[Calendar], w: Optional[Week]):
    def body(c: Ctx):
        if w:
            dates = [f"{MON3[d.month]} {d.day}" for d in w.days]
            intro = (f"{w.title}. Plan it on Sunday; each morning, add a day page under this page "
                     "from [[TEMPLATE · Daily – Standard|tpl.daily]] (Windows: + Page).")
        else:
            dates = [""] * 7
            intro = "Copy this page under its month, rename it YYYY-Www · dates, and fill the dates."
        tracker = _k(cal, w.home.habits_key) if w else "habits.dashboard"
        return [
            c.note(intro),
            c.h2("Big 3"), c.blank_todos(3),
            c.lines(["Focus of the week", "Goal it moves", "One thing I'll say no to"]),
            c.h2("Schedule"),
            c.table(["Day", "Date", "Personal", "Work lane", "Fixed appointments"],
                    [[d, dates[i], "", "", ""] for i, d in enumerate(DAY_NAMES)],
                    widths=[90, 60, 170, 170, 150], shade_first=True),
            c.h2("Commitments"),
            c.small("Moved from the [[Action List|tasks.actions]] (This Week block). Move, don't copy."),
            c.todo_table(["Task", "Area", "Due"], blank=7, widths=[30, 380, 130, 100]),
            c.h2("Work lane"),
            c.table(["Work priority", "Project / client", "Due"], [], widths=[320, 200, 120], blank=4),
            c.table(["Day", "Meeting (link)", "Prep done"], [], widths=[90, 450, 100], blank=3),
            c.h2("Recurring this week"),
            c.small("Copied from [[Recurring Tasks|tasks.recurring]] during the Weekly Review."),
            c.blank_todos(4),
            c.h2("Habits & routines"),
            c.p(f"Tick habits daily in the [[habit tracker|{tracker}]] · [[Routines|habits.routines]]"),
            c.h2("Notes"), c.p(), c.p(),
            c.h2("Weekly review"),
            c.small("Follow the [[Weekly Review Checklist|reviews.weekly]]. Short answers are fine."),
            c.table(["Question", "Answer"],
                    [["What went well?", ""], ["What didn't?", ""], ["What did I learn?", ""],
                     ["Best win (→ Wins Log)", ""], ["Next week's Big 3 (draft)", ""]],
                    widths=[200, 440], shade_first=True),
        ]
    return body


# --------------------------------------------------------------- assembling
def _year_bar(cal: Calendar, y: int):
    bar = [("◀ PREV YEAR", f"plan.{y - 1}.year")]
    for q in range(1, 5):
        bar.append((f"Q{q}", quarter_key(y, q)))
    bar += [("AT A GLANCE", f"plan.{y}.glance"), ("NEXT YEAR ▶", f"plan.{y + 1}.year")]
    return bar


def year_section(cal: Calendar, y: int) -> Section:
    bar = _year_bar(cal, y)
    return Section(f"plan.{y}.sec", f"{y} Year", [
        Page(f"plan.{y}.year", f"{y} · Year Dashboard", year_dashboard_body(cal, y), bar=bar),
        Page(f"plan.{y}.glance", f"{y} · Year at a Glance", glance_body(cal, y), bar=bar),
        Page(f"plan.{y}.dates", f"{y} · Important Dates & Events", important_dates_body(cal, y), bar=bar),
        Page(f"plan.{y}.review", f"{y} · Year-End Review", year_review_body(cal, y), bar=bar),
    ])


def quarter_section(cal: Calendar, y: int, q: int) -> Section:
    qk = quarter_key(y, q)
    months = cal.months_in_quarter(y, q)
    pq, nq = cal.prev_quarter(y, q), cal.next_quarter(y, q)
    qbar = ([(str(y), f"plan.{y}.year"), (f"Q{q}", qk)] +
            [(m.name.upper(), m.key) for m in months] +
            [("QUARTER REVIEW", qk + ".review"),
             ("◀ PREV", quarter_key(*pq) if pq else None), ("NEXT ▶", quarter_key(*nq) if nq else None)])
    pages = [Page(qk, f"Q{q} {y} · Quarter Plan", quarter_plan_body(cal, y, q), bar=qbar)]
    for m in months:
        weeks = cal.weeks_in(m)
        pm, nm = cal.prev_month(m), cal.next_month(m)
        crumbs = [(str(y), f"plan.{y}.year"), (f"Q{q}", qk), (m.name.upper(), m.key)]
        mbar = (crumbs + [(w.code, w.key) for w in weeks] +
                [("HABITS", m.habits_key), ("BUDGET", m.budget_key), ("REVIEW", m.review_key),
                 ("◀ PREV", pm.key if pm else None), ("NEXT ▶", nm.key if nm else None)])
        pages.append(Page(m.key, m.label, month_dashboard_body(cal, m), bar=mbar))
        for w in weeks:
            pw, nw = cal.prev_week(w), cal.next_week(w)
            wbar = crumbs + [(w.code, w.key), ("ACTION LIST", "tasks.actions"),
                             ("◀ PREV WEEK", pw.key if pw else None),
                             ("NEXT WEEK ▶", nw.key if nw else None)]
            pages.append(Page(w.key, w.title, week_body(cal, w), level=2, bar=wbar))
        pages.append(Page(m.review_key, f"{m.label} Review", month_review_body(cal, m), level=2,
                          bar=crumbs + [("REVIEW HUB", "reviews.hub")]))
    pages.append(Page(qk + ".review", f"Q{q} {y} · Quarter Review", quarter_review_body(cal, y, q),
                      bar=qbar))
    return Section(qk + ".sec", f"Q{q} {y}", pages)


def plan_groups(cal: Calendar, first_number: int) -> list[Group]:
    groups = []
    for i, y in enumerate(cal.years):
        sections = [year_section(cal, y)] + [quarter_section(cal, y, q) for q in cal.quarters_of(y)]
        groups.append(Group(f"plan.{y}", f"{first_number + i:02d} PLAN {y}", sections))
    return groups
