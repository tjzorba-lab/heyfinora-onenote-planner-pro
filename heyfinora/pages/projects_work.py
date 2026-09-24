"""07 PROJECTS and 08 WORK & BUSINESS."""
from __future__ import annotations

from ..core import Ctx, Group, Page, Section

# ------------------------------------------------------------------ PROJECTS
HUB_BAR = [("PORTFOLIO", "projects.portfolio"), ("PIPELINE", "projects.pipeline"),
           ("HOW TO START", "projects.howto")]
KIT_BAR = [("PORTFOLIO", "projects.portfolio"), ("TASKS", "tasks.actions"),
           ("MEETINGS", "work.meetings"), ("GOALS", "goals.dashboard")]


def portfolio(c: Ctx):
    head = ["Project (link)", "Area", "Goal", "Status", "Priority", "Next milestone", "Due", "% done"]
    w = [140, 70, 90, 70, 60, 110, 60, 50]
    return [
        c.note("Every project on one page. Keep 3–5 active. Update in the Weekly Review."),
        c.h2("Active"),
        c.table(head, [["[[EXAMPLE – Website Launch|projects.example.home]]", "Business", "Side income",
                        "On track", "High", "Site live", "Oct 2026", "40%"]], widths=w, blank=4),
        c.h2("On hold"), c.table(head, [], widths=w, blank=2),
        c.h2("Completed"), c.table(["Project", "Finished", "Result"], [], widths=[240, 100, 300], blank=2),
        c.p("Finished project sections move to [[Archive › Completed Projects|archive.projects]]."),
    ]


def pipeline(c: Ctx):
    return [
        c.note("Candidate projects. Score value, effort (5 = easy) and fit with your goals from 1–5, "
               "then add them up. Start the top of the queue only when an active project finishes."),
        c.table(["Project idea", "Goal", "Value", "Effort", "Fit", "Total", "Queue #"], [],
                widths=[200, 130, 55, 55, 55, 55, 60], blank=8),
    ]


def howto(c: Ctx):
    return [
        c.h2("Start a project in 4 steps"),
        c.numbered([
            "Right-click the **Project Kit** section in the [[Template Library|tpl.kit.home]] → Move or Copy → "
            "choose the PROJECTS group → Copy. (Web: copy the 5 pages one by one into a new section.)",
            "Rename the new section to the project name.",
            "Fill in Project Home: brief, objectives, scope, linked goal.",
            "Add a row to the [[Project Portfolio|projects.portfolio]] and link it (right-click Project Home → "
            "Copy Link to Page).",
        ]),
        c.h2("Each week"),
        c.bullets(["Update the Status Log on Project Home.",
                   "Move 1–3 next actions from Plan & Timeline to the Week page.",
                   "Put this month's milestones on the Month Dashboard."]),
        c.p("See a filled-in project: [[EXAMPLE – Website Launch|projects.example.home]]"),
    ]


def kit_pages(prefix: str, key: str, example: bool) -> list[Page]:
    """The 5-page Project Kit, as a filled example or a blank template."""
    def v(s: str) -> str:
        return s if example else ""

    def home(c: Ctx):
        out = [c.note("EXAMPLE project – study it, then archive it.")] if example else []
        return out + [
            c.table(["Status", "% done", "Next milestone", "Due"],
                    [[v("On track"), v("40%"), v("Site live"), v("Oct 31, 2026")]], widths=[160, 120, 220, 140],
                    header_bg=c.t["teal"]),
            c.h2("Brief"),
            c.p(v("Launch a simple 5-page website for my side business, with an email sign-up.")),
            c.h2("Objectives & success measures"),
            c.table(["Objective", "Measure"],
                    [[v("Site live"), v("Published by Oct 31")], [v("Grow list"), v("50 subscribers by Dec 31")],
                     ["", ""]], widths=[320, 320]),
            c.h2("Scope"),
            c.table(["In", "Out"], [[v("Home, About, Services, Contact, Blog"), v("Online shop (phase 2)")],
                                    ["", ""]], widths=[320, 320]),
            c.lines(["Linked goal", "Stakeholders"]),
            c.p("Goal: [[EXAMPLE – Goal page|goals.example]]") if example else c.p(),
            c.h2("Status log (weekly)"),
            c.table(["Week", "Status", "Progress / blockers"],
                    [[v("W38"), v("On track"), v("Platform chosen, domain bought")],
                     [v("W39"), v("At risk"), v("Photos late – asked a friend to help")], ["", "", ""]],
                    widths=[80, 100, 460]),
        ]

    def plan(c: Ctx):
        return [
            c.h2("Action plan by phase"),
            c.table(["Phase", "Goal of the phase", "Dates"],
                    [[v("1 Setup"), v("Platform, domain, look"), v("Sep 14–27")],
                     [v("2 Content"), v("Write and photograph 5 pages"), v("Sep 28–Oct 18")],
                     [v("3 Launch"), v("Test, publish, announce"), v("Oct 19–31")]], widths=[120, 360, 160]),
            c.h2("Task breakdown"),
            c.small("Move this week's 1–3 next actions to the Week page."),
            c.table(["Done", "Task", "Owner", "Due", "Status"],
                    [["[x]", v("Choose platform"), v("Me"), v("Sep 18"), v("Done")],
                     ["[ ]", v("Write About page"), v("Me"), v("Oct 2"), v("Doing")],
                     ["[ ]", v("Product photos"), v("Sam"), v("Oct 9"), v("Waiting")]] if example else [],
                    widths=[40, 280, 100, 100, 120], blank=5),
            c.h2("Milestones"),
            c.table(["Milestone", "Date", "Done"], [[v("Design approved"), v("Sep 27"), "[x]" if example else "[ ]"],
                                                    [v("Site live"), v("Oct 31"), "[ ]"]], widths=[380, 160, 100]),
            c.h2("Timeline"),
            c.table(["Week / month", "What happens"], [[v("W38–W39"), v("Setup")], [v("W40–W42"), v("Content")],
                                                       [v("W43–W44"), v("Launch")]], widths=[140, 500]),
        ]

    def log(c: Ctx):
        return [
            c.note("Dated notes and decisions. Link meeting pages from Work & Business › Meetings."),
            c.table(["Date", "Note / decision", "Link"],
                    [[v("Sep 16"), v("Decided: no online shop in phase 1"), ""],
                     [v("Sep 22"), v("Kick-off call with Sam"), v("(meeting page)")]] if example else [],
                    widths=[90, 420, 130], blank=6),
        ]

    def risks(c: Ctx):
        return [
            c.h2("Risk register"),
            c.table(["Risk", "Likelihood", "Impact", "Response", "Owner"],
                    [[v("Photos late"), v("Medium"), v("High"), v("Use stock photos as backup"), v("Me")]]
                    if example else [], widths=[170, 80, 70, 220, 100], blank=3),
            c.h2("Issue log"),
            c.table(["Issue", "Date", "Action", "Resolved"], [], widths=[220, 90, 250, 80], blank=3),
        ]

    def closeout(c: Ctx):
        return [
            c.h2("Completion checklist"),
            c.todos(["All tasks done or moved", "Results recorded below", "Portfolio row moved to Completed",
                     "Section moved to [[Archive › Completed Projects|archive.projects]]"]),
            c.h2("Results vs objectives"),
            c.table(["Objective", "Result"], [], widths=[320, 320], blank=3),
            c.h2("Lessons learned"),
            c.table(["Keep", "Change", "Stop"], [], widths=[213, 213, 214], blank=3),
            c.h2("Handover notes"), c.p(),
        ]

    names = [("home", "Project Home", home), ("plan", "Plan & Timeline", plan), ("log", "Project Log", log),
             ("risks", "Risks & Issues", risks), ("close", "Close-out", closeout)]
    return [Page(f"{key}.{k}", f"{prefix}{title}", fn, bar=KIT_BAR) for k, title, fn in names]


def projects_group() -> Group:
    return Group("projects", "07 PROJECTS", [
        Section("projects.hub", "Projects Hub", [
            Page("projects.portfolio", "Project Portfolio", portfolio, bar=HUB_BAR),
            Page("projects.pipeline", "Project Pipeline", pipeline, bar=HUB_BAR),
            Page("projects.howto", "How to Start a Project", howto, bar=HUB_BAR),
        ]),
        Section("projects.example", "EXAMPLE – Website Launch", kit_pages("", "projects.example", True)),
    ])


# ------------------------------------------------------------ WORK & BUSINESS
WORK_BAR = [("WORK DASHBOARD", "work.dashboard"), ("MEETINGS", "work.meetings"), ("CLIENTS", "work.clients"),
            ("CONTENT", "work.content"), ("SOPS", "work.sops")]


def work_dashboard(c: Ctx):
    return [
        c.h2("This week's work priorities"),
        c.small("Planned in the Work lane of this week's page: [[This Week|@week]]"),
        c.table(["Priority", "Project / client", "Due"], [], widths=[320, 200, 120], blank=3),
        c.h2("Active clients"),
        c.table(["Client (link)", "Next step", "Date"], [], widths=[240, 280, 120], blank=3),
        c.h2("Upcoming meetings"),
        c.table(["Date", "Meeting (link)", "Prep"], [["", "", "[ ]"]] * 3, widths=[100, 440, 100]),
        c.h2("Links"),
        c.bullets(["Business goals: [[Goals Dashboard|goals.dashboard]] (tag them to Business or Work & Career)",
                   "Business projects: [[Project Portfolio|projects.portfolio]]",
                   "[[Business Snapshot|work.snapshot]] · [[Opportunity Lab|work.opportunity]] · "
                   "[[Decision Log|work.decisions]] · [[Business Reviews|work.bizreviews]]",
                   "Business money: [[Business Money|money.business]]"]),
    ]


def snapshot(c: Ctx):
    return [
        c.note("Your business on one page. Revisit every quarter."),
        c.lines(["Mission (one sentence)", "Offers / products", "Ideal customer", "Problem I solve",
                 "Channels", "Price points"]),
        c.h2("12-month priorities"), c.numbered(["", "", ""]),
        c.h2("Key numbers to watch"),
        c.table(["Number", "Now", "Target", "Check"], [["Monthly revenue", "", "", "Monthly"],
                                                        ["Customers", "", "", "Monthly"],
                                                        ["Email list", "", "", "Monthly"],
                                                        ["Profit margin", "", "", "Quarterly"]],
                widths=[200, 140, 140, 160], shade_first=True),
    ]


def opportunity(c: Ctx):
    return [
        c.note("Business ideas worth evaluating. Score each 1–5 and decide: Test · Park · Drop. "
               "Ideas start in the [[Idea Vault|notes.ideas]]; a full evaluation uses "
               "[[TEMPLATE · Opportunity Scorecard|tpl.opportunity]]."),
        c.table(["Idea", "Problem", "Audience", "Effort", "Revenue potential", "Score", "Decision"], [],
                widths=[120, 110, 100, 60, 90, 60, 100], blank=8),
    ]


def decisions(c: Ctx):
    return [
        c.note("Record important decisions so you remember why. Review the date column monthly."),
        c.table(["Date", "Decision", "Options considered", "Reason", "Owner", "Review date"], [],
                widths=[70, 140, 140, 140, 70, 80], blank=10),
    ]


def biz_reviews(c: Ctx):
    return [
        c.note("Each quarter, copy [[TEMPLATE · Business Review|tpl.bizreview]] as a subpage under this page "
               "and name it e.g. Q4 2026 · Business Review."),
        c.table(["Quarter", "Review (link)", "Key insight"], [], widths=[100, 200, 340], blank=6),
    ]


def meeting_index(c: Ctx):
    return [
        c.note("One row per meeting. Create meeting pages from [[TEMPLATE · Meeting Notes|tpl.meeting]] "
               "and 1:1 or series pages from [[TEMPLATE · Recurring Meeting / 1:1|tpl.oneonone]] in this section. "
               "In the Weekly Review, move action items to the [[Action List|tasks.actions]] or "
               "[[Waiting For|tasks.waiting]]."),
        c.table(["Date", "Meeting (link)", "Type", "Project / client", "Actions sent to Tasks"],
                [["", "", "", "", "[ ]"]] * 10, widths=[80, 200, 90, 150, 120]),
    ]


def client_directory(c: Ctx):
    return [
        c.note("Create client pages from [[TEMPLATE · Client Page|tpl.client]] in this section."),
        c.table(["Client (link)", "Contact", "Service", "Status", "Start", "Value band"], [],
                widths=[140, 130, 120, 80, 70, 100], blank=8),
    ]


def client_pipeline(c: Ctx):
    out = [c.note("Lead → Proposal → Active → Complete. Move a row down as the client moves on.")]
    for stage in ["Lead", "Proposal", "Active", "Complete"]:
        out += [c.h2(stage), c.table(["Client", "Next step", "Date", "Value"], [],
                                     widths=[200, 260, 90, 90], blank=3)]
    return out


def content_strategy(c: Ctx):
    return [
        c.lines(["Audience", "What they want from me", "Content pillars (3–5)", "Channels", "Posting cadence",
                 "Voice / style"]),
        c.p("Monthly calendars: copy [[TEMPLATE · Content Calendar|tpl.contentcal]] into this section. "
            "Big pieces: [[TEMPLATE · Content Brief|tpl.brief]]."),
    ]


def content_ideas(c: Ctx):
    return [c.table(["Idea", "Pillar", "Format", "Channel", "Status"], [],
                    widths=[240, 110, 100, 100, 90], blank=15),
            c.small("Status: Idea · Drafting · Scheduled · Published")]


def sop_library(c: Ctx):
    return [
        c.note("Index of repeatable procedures. Write each one from [[TEMPLATE · SOP|tpl.sop]] in this section."),
        c.table(["SOP (link)", "Trigger (when to use it)", "Owner", "Last updated"], [],
                widths=[200, 250, 90, 100], blank=10),
    ]


def work_group() -> Group:
    b = WORK_BAR
    return Group("work", "08 WORK & BUSINESS", [
        Section("work.hq", "Work HQ", [
            Page("work.dashboard", "Work Dashboard", work_dashboard, bar=b),
            Page("work.snapshot", "Business Snapshot", snapshot, bar=b),
            Page("work.opportunity", "Opportunity Lab", opportunity, bar=b),
            Page("work.decisions", "Decision Log", decisions, bar=b),
            Page("work.bizreviews", "Business Reviews", biz_reviews, bar=b),
        ]),
        Section("work.meetings.sec", "Meetings", [Page("work.meetings", "Meeting Index", meeting_index, bar=b)]),
        Section("work.clients.sec", "Clients", [
            Page("work.clients", "Client Directory", client_directory, bar=b),
            Page("work.pipeline", "Client Pipeline", client_pipeline, bar=b),
        ]),
        Section("work.content.sec", "Content", [
            Page("work.content", "Content Strategy", content_strategy, bar=b),
            Page("work.ideas", "Content Ideas Bank", content_ideas, bar=b),
        ]),
        Section("work.sops.sec", "SOPs", [Page("work.sops", "SOP Library", sop_library, bar=b)]),
    ])
