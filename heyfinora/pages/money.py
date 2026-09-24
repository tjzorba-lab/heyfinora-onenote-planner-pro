"""09 MONEY: Money HQ and the monthly budget sections."""
from __future__ import annotations

from typing import Optional

from ..core import Ctx, Group, Page, Section
from ..dates import Calendar, Month

MONEY_BAR = [("FINANCIAL DASHBOARD", "money.dashboard"), ("BILLS", "money.bills"),
             ("SAVINGS", "money.savings"), ("DEBT", "money.debt")]

PRIVACY = ("Private section: right-click the section tab → Password Protect This Section. "
           "Never store account numbers, card numbers or passwords here.")

BUDGET_LINES = {
    "Income": ["Salary", "Business / side income", "Other"],
    "Fixed": ["Rent / mortgage", "Utilities", "Phone & internet", "Insurance", "Subscriptions", "Transport"],
    "Variable": ["Groceries", "Eating out", "Shopping", "Health", "Fun", "Gifts", "Other"],
    "Savings": ["Emergency fund", "Sinking funds", "Investments"],
    "Debt": ["Card / loan payments"],
}


def financial_dashboard(cal: Calendar):
    def body(c: Ctx):
        links = " · ".join(f"[[{m.label}|{m.budget_key}]]" for m in cal.months)
        return [
            c.note(PRIVACY),
            c.h2("This month"), c.p("Budget: [[This Month|@month]] → BUDGET in the bar"),
            c.table(["", "Planned", "Actual", "Difference"],
                    [["Income", "", "", ""], ["Spending", "", "", ""], ["Saved", "", "", ""]],
                    widths=[160, 160, 160, 160], shade_first=True),
            c.h2("Progress"),
            c.table(["Area", "Now", "Target", "Page"],
                    [["Savings", "", "", "[[Savings Goals|money.savings]]"],
                     ["Debt", "", "", "[[Debt Payoff|money.debt]]"],
                     ["Net worth", "", "", "[[Net Worth Snapshot|money.networth]]"]],
                    widths=[160, 140, 140, 200], shade_first=True),
            c.h2("Upcoming bills"),
            c.table(["Bill", "Amount", "Due"], [], widths=[320, 160, 160], blank=4),
            c.h2("All budgets"), c.p(links),
            c.h2("Money pages"),
            c.bullets(["Plans: " + " · ".join(f"[[{y} Money Plan & Review|money.plan.{y}]]" for y in cal.years),
                       "[[Income Streams|money.income]] · [[Bills & Subscriptions|money.bills]] · "
                       "[[Business Money|money.business]]"]),
            c.small("Tables do not calculate. On Windows type 1250+380+95= and press Enter. "
                    "Want automatic totals? Use the HEYFINORA Excel / Google Sheets budget."),
        ]
    return body


def money_plan(y: Optional[int]):
    def body(c: Ctx):
        yl = str(y) if y else "YYYY"
        return [
            c.note(PRIVACY),
            c.h2(f"Plan (start of {yl})"),
            c.table(["", "Target"], [["Income target", ""], ["Savings target", ""], ["Debt paid off", ""],
                                     ["Giving", ""]], widths=[240, 400], shade_first=True),
            c.h3("Planned big expenses"),
            c.table(["Expense", "Month", "Amount"], [], widths=[340, 150, 150], blank=4),
            c.h3("Sinking funds"),
            c.table(["Fund", "Target", "Per month"], [["Holidays", "", ""], ["Car", "", ""], ["Gifts", "", ""]],
                    widths=[340, 150, 150], blank=2),
            c.h2(f"Review (end of {yl})"),
            c.table(["", "Plan", "Actual", "Lesson"], [["Income", "", "", ""], ["Savings", "", "", ""],
                                                        ["Debt paid", "", "", ""], ["Big expenses", "", "", ""]],
                    widths=[140, 120, 120, 260], shade_first=True),
            c.lines(["Best money decision", "Change next year"]),
        ]
    return body


def simple_tracker(note: str, head: list[str], blank: int = 8, rows=()):
    def body(c: Ctx):
        return [c.note(note), c.table(head, [list(r) for r in rows], blank=blank)]
    return body


def networth(cal: Calendar):
    def body(c: Ctx):
        return [
            c.note("Month-end totals by type. No account numbers."),
            c.table(["Month", "Cash", "Investments", "Property", "Other assets", "Debts", "Net worth"],
                    [[m.label, "", "", "", "", "", ""] for m in cal.months],
                    widths=[130, 80, 90, 80, 90, 80, 90]),
        ]
    return body


def debt_payoff(cal: Calendar):
    def body(c: Ctx):
        return [
            c.note("Snowball: smallest balance first. Avalanche: highest rate first. Pick one and write it down."),
            c.lines(["My method"]),
            c.table(["Debt", "Balance", "Rate", "Minimum", "Payoff order"], [],
                    widths=[200, 110, 80, 110, 140], blank=5),
            c.h2("Month-by-month balance"),
            c.table(["Month", "Debt 1", "Debt 2", "Debt 3", "Debt 4", "Total"],
                    [[m.label, "", "", "", "", ""] for m in cal.months], widths=[140, 100, 100, 100, 100, 100]),
        ]
    return body


def business_money(cal: Calendar):
    def body(c: Ctx):
        return [
            c.table(["Month", "Revenue", "Expenses", "Profit", "Tax set-aside", "Notes"],
                    [[m.label, "", "", "", "", ""] for m in cal.months], widths=[130, 90, 90, 90, 100, 140]),
            c.h2("Notes for the accountant"), c.p(), c.p(),
        ]
    return body


def budget_body(m: Optional[Month]):
    def body(c: Ctx):
        rows = []
        for group, items in BUDGET_LINES.items():
            rows.append([f"**{group}**", "", "", ""])
            rows += [[f"   {i}", "", "", ""] for i in items]
            rows.append([f"**Total {group.lower()}**", "", "", ""])
        return [
            c.note(PRIVACY),
            c.h2("Planned vs actual"),
            c.table(["Category", "Planned", "Actual", "Difference"], rows, widths=[240, 130, 130, 140]),
            c.h2("Expense log"),
            c.small("Log weekly, then add up each category at month-end."),
            c.table(["Date", "Item", "Category", "Amount"], [], widths=[80, 300, 140, 120], blank=15),
            c.h2("Month-end check-in"),
            c.lines(["Did I stay on plan?", "Biggest surprise", "One thing to change next month",
                     "Moved to savings"]),
            c.p(f"Then fill the money block of the [[Month Review|{m.review_key if m else None}]]."
                if m else "Then fill the money block of the Month Review."),
        ]
    return body


def money_group(cal: Calendar) -> Group:
    b = MONEY_BAR
    hq = [Page("money.dashboard", "Financial Dashboard", financial_dashboard(cal), bar=b)]
    hq += [Page(f"money.plan.{y}", f"{y} Money Plan & Review", money_plan(y), bar=b) for y in cal.years]
    hq += [
        Page("money.networth", "Net Worth Snapshot", networth(cal), bar=b),
        Page("money.income", "Income Streams", simple_tracker(
            "Each source of income and what you expect from it. Review quarterly.",
            ["Source", "Type", "Expected / month", "Notes"], 6,
            [["Salary", "Job", "", ""], ["Side business", "Business", "", ""]]), bar=b),
        Page("money.bills", "Bills & Subscriptions", simple_tracker(
            "Every bill and subscription. Check monthly; add renewal dates to Important Dates.",
            ["Name", "Amount", "Frequency", "Due day", "Renewal", "Personal / business", "Keep / cancel"], 14),
            bar=b),
        Page("money.savings", "Savings Goals", simple_tracker(
            "Link a savings goal to its goal page if it's one of your annual goals.",
            ["Goal", "Target", "Target date", "Saved to date", "Monthly contribution"], 6,
            [["Emergency fund", "", "", "", ""]]), bar=b),
        Page("money.debt", "Debt Payoff", debt_payoff(cal), bar=b),
        Page("money.business", "Business Money", business_money(cal), bar=b),
    ]
    sections = [Section("money.hq", "Money HQ", hq)]
    for y in cal.years:
        pages = []
        for m in cal.months_of(y):
            pm, nm = cal.prev_month(m), cal.next_month(m)
            pages.append(Page(m.budget_key, f"{m.label} Budget", budget_body(m),
                              bar=b + [("MONTH", m.key), ("◀ PREV", pm.budget_key if pm else None),
                                       ("NEXT ▶", nm.budget_key if nm else None)]))
        sections.append(Section(f"money.budgets.{y}", f"Budgets {y}", pages))
    return Group("money", "09 MONEY", sections)
