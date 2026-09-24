"""The planner's calendar: months, ISO weeks (Monday start) and quarters.

A week belongs to the month that contains its Thursday, so every week has
exactly one home.
"""
from __future__ import annotations

import calendar
import datetime as dt
from dataclasses import dataclass

MONTHS = list(calendar.month_name)
MON3 = list(calendar.month_abbr)


@dataclass(frozen=True)
class Month:
    year: int
    month: int

    @property
    def quarter(self) -> int:
        return (self.month - 1) // 3 + 1

    @property
    def name(self) -> str:
        return MONTHS[self.month]

    @property
    def key(self) -> str:
        return f"plan.{self.year}.m{self.month:02d}"

    @property
    def review_key(self) -> str:
        return self.key + ".review"

    @property
    def quarter_key(self) -> str:
        return f"plan.{self.year}.q{self.quarter}"

    @property
    def budget_key(self) -> str:
        return f"money.budget.{self.year}.{self.month:02d}"

    @property
    def habits_key(self) -> str:
        return f"habits.tracker.{self.year}.{self.month:02d}"

    @property
    def label(self) -> str:
        return f"{self.year}-{self.month:02d} · {self.name}"

    @property
    def days(self) -> int:
        return calendar.monthrange(self.year, self.month)[1]

    def date(self, day: int) -> dt.date:
        return dt.date(self.year, self.month, day)


@dataclass(frozen=True)
class Week:
    iso_year: int
    iso_week: int

    @property
    def monday(self) -> dt.date:
        return dt.date.fromisocalendar(self.iso_year, self.iso_week, 1)

    @property
    def days(self) -> list[dt.date]:
        return [self.monday + dt.timedelta(d) for d in range(7)]

    @property
    def home(self) -> Month:
        th = self.monday + dt.timedelta(3)
        return Month(th.year, th.month)

    @property
    def key(self) -> str:
        return f"plan.{self.iso_year}.w{self.iso_week:02d}"

    @property
    def code(self) -> str:
        return f"W{self.iso_week:02d}"

    @property
    def title(self) -> str:
        a, b = self.monday, self.monday + dt.timedelta(6)
        return f"{self.iso_year}-W{self.iso_week:02d} · {MON3[a.month]} {a.day} – {MON3[b.month]} {b.day}"


def quarter_key(year: int, q: int) -> str:
    return f"plan.{year}.q{q}"


class Calendar:
    def __init__(self, start: tuple[int, int] = (2026, 7), end: tuple[int, int] = (2027, 12)):
        self.months: list[Month] = []
        y, m = start
        while (y, m) <= end:
            self.months.append(Month(y, m))
            y, m = (y + 1, 1) if m == 12 else (y, m + 1)
        mset = set(self.months)
        first = self.months[0].date(1) - dt.timedelta(7)
        last = self.months[-1].date(self.months[-1].days)
        weeks, d = [], first - dt.timedelta(first.weekday())
        while d <= last:
            iy, iw, _ = d.isocalendar()
            w = Week(iy, iw)
            if w.home in mset:
                weeks.append(w)
            d += dt.timedelta(7)
        self.weeks: list[Week] = weeks
        self.years: list[int] = sorted({m.year for m in self.months})

    def months_of(self, year: int) -> list[Month]:
        return [m for m in self.months if m.year == year]

    def quarters_of(self, year: int) -> list[int]:
        return sorted({m.quarter for m in self.months_of(year)})

    def months_in_quarter(self, year: int, q: int) -> list[Month]:
        return [m for m in self.months_of(year) if m.quarter == q]

    def weeks_in(self, month: Month) -> list[Week]:
        return [w for w in self.weeks if w.home == month]

    def all_quarters(self) -> list[tuple[int, int]]:
        return [(y, q) for y in self.years for q in self.quarters_of(y)]

    @staticmethod
    def _neighbor(seq: list, item, step: int):
        i = seq.index(item) + step
        return seq[i] if 0 <= i < len(seq) else None

    def prev_month(self, m: Month):
        return self._neighbor(self.months, m, -1)

    def next_month(self, m: Month):
        return self._neighbor(self.months, m, 1)

    def prev_week(self, w: Week):
        return self._neighbor(self.weeks, w, -1)

    def next_week(self, w: Week):
        return self._neighbor(self.weeks, w, 1)

    def prev_quarter(self, y: int, q: int):
        return self._neighbor(self.all_quarters(), (y, q), -1)

    def next_quarter(self, y: int, q: int):
        return self._neighbor(self.all_quarters(), (y, q), 1)

    def current(self, today: dt.date) -> dict[str, str]:
        """Keys for the 'You are here' pointers, clamped into the planner's range."""
        first, last = self.months[0].date(1), self.months[-1].date(self.months[-1].days)
        today = min(max(today, first), last)
        m = Month(today.year, today.month)
        iy, iw, _ = today.isocalendar()
        week = Week(iy, iw)
        if week not in self.weeks:
            week = self.weeks[0] if today <= first + dt.timedelta(6) else self.weeks[-1]
        return {"year": f"plan.{m.year}.year", "quarter": m.quarter_key,
                "month": m.key, "week": week.key}
