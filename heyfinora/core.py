"""Notebook model and the HTML building blocks every page is made from.

Pages are rendered to the subset of HTML that the OneNote API accepts
(headings, paragraphs, lists, tables, links, data-tag checkboxes, inline
styles). The same HTML is used for the offline preview.
"""
from __future__ import annotations

import html
import re
from dataclasses import dataclass, field
from typing import Callable, Iterator, Optional, Union

THEME = {
    "navy": "#1F2A44",
    "teal": "#2A7F7A",
    "gold": "#B8912F",
    "coral": "#C8553D",
    "cream": "#F6F1E7",
    "ink": "#26262B",
    "muted": "#8A8A93",
    "line": "#D9D4C7",
    "font": "Segoe UI",
}

Resolver = Callable[[str], Optional[str]]
BarItem = tuple[str, Optional[str]]


@dataclass
class Page:
    key: str
    title: str
    body: Callable[["Ctx"], list[str]]
    level: int = 1
    bar: list[BarItem] = field(default_factory=list)


@dataclass
class Section:
    key: str
    name: str
    pages: list[Page]


@dataclass
class Group:
    key: str
    name: str
    sections: list[Section]


Item = Union[Section, Group]


@dataclass
class Notebook:
    name: str
    items: list[Item]
    # Keys the global bar and "You are here" box point at.
    current: dict[str, str] = field(default_factory=dict)

    def sections(self) -> Iterator[tuple[Optional[Group], Section]]:
        for item in self.items:
            if isinstance(item, Group):
                for s in item.sections:
                    yield item, s
            else:
                yield None, item

    def pages(self) -> Iterator[tuple[Section, Page]]:
        for _, s in self.sections():
            for p in s.pages:
                yield s, p

    def page_keys(self) -> set[str]:
        return {p.key for _, p in self.pages()}


# Section and section-group names: the OneNote API rejects ? * \ / : < > | & # ' " % ~
_BAD_NAME = re.compile(r"[?*\\/:<>|#'\"%~]")


def safe_name(name: str) -> str:
    return _BAD_NAME.sub("", name.replace("&", "+")).strip()[:50]


GLOBAL_BAR = [
    ("HOME", "home.dashboard"),
    ("PLAN", "@year"),
    ("TASKS", "tasks.dashboard"),
    ("GOALS", "goals.dashboard"),
    ("PROJECTS", "projects.portfolio"),
    ("WORK", "work.dashboard"),
    ("MONEY", "money.dashboard"),
    ("NOTES", "notes.quick"),
    ("REVIEWS", "reviews.hub"),
    ("MORE", "home.map"),
]

_LINK = re.compile(r"\[\[([^\]|]+)\|([^\]]+)\]\]")
_BOLD = re.compile(r"\*\*(.+?)\*\*")


class Ctx:
    """Rendering context for one page: resolves keys to links and builds blocks."""

    def __init__(self, nb: Notebook, section: Section, page: Page, resolve: Resolver):
        self.nb, self.section, self.page, self._resolve = nb, section, page, resolve
        self.t = THEME

    # ---- links -----------------------------------------------------------
    def href(self, key: Optional[str]) -> Optional[str]:
        if not key:
            return None
        if key.startswith("@"):
            key = self.nb.current.get(key[1:], "")
        return self._resolve(key) if key else None

    def link(self, label: str, key: Optional[str], color: Optional[str] = None) -> str:
        url = self.href(key)
        text = html.escape(label)
        if url is None:
            return f'<span style="color:{self.t["muted"]}">{text}</span>'
        style = f' style="color:{color}"' if color else ""
        return f'<a href="{html.escape(url, quote=True)}"{style}>{text}</a>'

    def rich(self, s: str) -> str:
        """Escape text, then turn [[label|key]] into links and **x** into bold."""
        out, pos = [], 0
        for m in _LINK.finditer(s):
            out.append(_BOLD.sub(r"<b>\1</b>", html.escape(s[pos:m.start()])))
            out.append(self.link(m.group(1), m.group(2)))
            pos = m.end()
        out.append(_BOLD.sub(r"<b>\1</b>", html.escape(s[pos:])))
        return "".join(out)

    # ---- text blocks -----------------------------------------------------
    def _font(self, size: int, color: Optional[str] = None, bold: bool = False) -> str:
        st = f"font-family:{self.t['font']};font-size:{size}pt;color:{color or self.t['ink']}"
        return st + (";font-weight:bold" if bold else "")

    def h1(self, s: str) -> str:
        return f'<h1 style="{self._font(20, self.t["navy"], True)}">{self.rich(s)}</h1>'

    def h2(self, s: str) -> str:
        return f'<h2 style="{self._font(15, self.t["teal"], True)}">{self.rich(s)}</h2>'

    def h3(self, s: str) -> str:
        return f'<h3 style="{self._font(12, self.t["navy"], True)}">{self.rich(s)}</h3>'

    def p(self, s: str = "", size: int = 11, color: Optional[str] = None, italic: bool = False) -> str:
        st = self._font(size, color) + (";font-style:italic" if italic else "")
        return f'<p style="{st}">{self.rich(s) if s else "&nbsp;"}</p>'

    def small(self, s: str) -> str:
        return self.p(s, size=9, color=self.t["muted"], italic=True)

    def todo(self, s: str = "", done: bool = False) -> str:
        tag = "to-do:completed" if done else "to-do"
        return f'<p data-tag="{tag}" style="{self._font(11)}">{self.rich(s) if s else "&nbsp;"}</p>'

    def todos(self, items: list[str]) -> str:
        return "".join(self.todo(i) for i in items)

    def blank_todos(self, n: int) -> str:
        return "".join(self.todo() for _ in range(n))

    def bullets(self, items: list[str]) -> str:
        lis = "".join(f'<li style="{self._font(11)}">{self.rich(i)}</li>' for i in items)
        return f"<ul>{lis}</ul>"

    def numbered(self, items: list[str]) -> str:
        lis = "".join(f'<li style="{self._font(11)}">{self.rich(i)}</li>' for i in items)
        return f"<ol>{lis}</ol>"

    def lines(self, labels: list[str]) -> str:
        """Fill-in fields: a two-column table of label / blank."""
        return self.table(["", ""], [[f"**{l}**", ""] for l in labels], widths=[180, 460], header=False)

    def note(self, s: str, color: Optional[str] = None) -> str:
        bg = color or self.t["cream"]
        return (f'<table style="border-collapse:collapse"><tr>'
                f'<td style="background-color:{bg};width:640px;padding:6px">'
                f'<p style="{self._font(10)}">{self.rich(s)}</p></td></tr></table>')

    # ---- tables ------------------------------------------------------------
    def cell(self, v: str) -> str:
        if v == "[ ]":
            return self.todo()
        if v == "[x]":
            return self.todo(done=True)
        if v.startswith("[ ] "):
            return self.todo(v[4:])
        return f'<p style="{self._font(10)}">{self.rich(v) if v else "&nbsp;"}</p>'

    def table(self, headers: list[str], rows: list[list[str]], widths: Optional[list[int]] = None,
              blank: int = 0, header: bool = True, header_bg: Optional[str] = None,
              shade_first: bool = False) -> str:
        n = len(headers)
        widths = widths or [max(60, 640 // n)] * n
        hb = header_bg or self.t["navy"]
        out = ['<table border="1" style="border-collapse:collapse">']
        if header:
            ths = "".join(
                f'<td style="background-color:{hb};width:{w}px">'
                f'<p style="{self._font(10, "#FFFFFF", True)}">{html.escape(h) or "&nbsp;"}</p></td>'
                for h, w in zip(headers, widths))
            out.append(f"<tr>{ths}</tr>")
        for row in list(rows) + [[""] * n for _ in range(blank)]:
            tds = []
            for i, (v, w) in enumerate(zip(row, widths)):
                bg = f"background-color:{self.t['cream']};" if shade_first and i == 0 else ""
                tds.append(f'<td style="{bg}width:{w}px">{self.cell(v)}</td>')
            out.append(f"<tr>{''.join(tds)}</tr>")
        out.append("</table>")
        return "".join(out)

    def todo_table(self, headers: list[str], rows: list[list[str]] = (), blank: int = 5,
                   widths: Optional[list[int]] = None) -> str:
        """A task table whose first column is a checkbox."""
        rows = [["[ ]"] + list(r) for r in rows]
        return self.table(["✓"] + headers, rows + [["[ ]"] + [""] * len(headers)] * blank,
                          widths=widths or [30] + [max(60, 610 // len(headers))] * len(headers))

    # ---- chrome --------------------------------------------------------------
    def bar(self, items: list[BarItem], bg: str, fg: str, size: int = 9) -> str:
        sep = f'<span style="color:{fg}"> · </span>'
        links = sep.join(self.link(label, key, color=fg) for label, key in items)
        return (f'<table style="border-collapse:collapse"><tr>'
                f'<td style="background-color:{bg};width:760px">'
                f'<p style="{self._font(size, fg, True)}">{links}</p></td></tr></table>')

    def section_dashboard_key(self) -> str:
        return self.section.pages[0].key


def render_body(nb: Notebook, section: Section, page: Page, resolve: Resolver) -> str:
    """The page's content: global bar, context bar, body blocks and footer."""
    c = Ctx(nb, section, page, resolve)
    parts = [c.bar(GLOBAL_BAR, c.t["navy"], "#FFFFFF")]
    if page.bar:
        parts.append(c.bar(page.bar, c.t["cream"], c.t["navy"]))
    parts.extend(page.body(c))
    parts.append(c.p())
    parts.append(c.bar([("▲ TOP", page.key), ("HOME", "home.dashboard"),
                        ("SECTION DASHBOARD", c.section_dashboard_key())],
                       "#FFFFFF", c.t["muted"], size=8))
    parts.append(c.p("HEYFINORA · Ultimate OneNote Planner PRO", size=8, color=c.t["gold"]))
    return "".join(parts)


def render_page(nb: Notebook, section: Section, page: Page, resolve: Resolver) -> str:
    """Full HTML document for the OneNote API (body wrapped in a replaceable div)."""
    body = render_body(nb, section, page, resolve)
    return (f"<!DOCTYPE html><html><head><title>{html.escape(page.title)}</title>"
            f'<meta charset="utf-8" /></head><body>'
            f'<div data-id="body">{body}</div></body></html>')
