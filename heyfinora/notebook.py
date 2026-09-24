"""Assemble the full HEYFINORA notebook from the blueprint."""
from __future__ import annotations

import datetime as dt

from .core import Notebook
from .dates import Calendar
from .pages.life import archive_group, growth_section, journal_section, notes_group, reviews_section
from .pages.money import money_group
from .pages.plan import plan_groups
from .pages.projects_work import projects_group, work_group
from .pages.start_home import home_section, start_section
from .pages.systems import goals_section, habits_section, tasks_section
from .pages.templates import template_group

NOTEBOOK_NAME = "HEYFINORA Ultimate OneNote Planner PRO 2026–2027"


def build_notebook(start=(2026, 7), end=(2027, 12), today: dt.date | None = None,
                   name: str = NOTEBOOK_NAME) -> Notebook:
    cal = Calendar(start, end)
    plans = plan_groups(cal, first_number=2)
    items = [start_section(), home_section(), *plans,
             tasks_section(cal), goals_section(cal), habits_section(cal), projects_group(), work_group(),
             money_group(cal), growth_section(), journal_section(), notes_group(), reviews_section(cal),
             template_group(), archive_group()]
    # Areas after PLAN are numbered from 04 no matter how many PLAN years there are.
    number = 4
    for item in items[2 + len(plans):]:
        prefix, _, rest = item.name.partition(" ")
        if prefix.isdigit():
            item.name = f"{number:02d} {rest}"
            number += 1
    return Notebook(name, items, current=cal.current(today or dt.date.today()))
