#!/usr/bin/env python3
"""HEYFINORA Ultimate OneNote Planner PRO – notebook builder.

  python build.py stats                 # page counts per area
  python build.py preview               # offline HTML preview in ./preview
  python build.py publish               # create the notebook in your OneNote
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

from heyfinora.core import Group
from heyfinora.notebook import NOTEBOOK_NAME, build_notebook


def month(s: str) -> tuple[int, int]:
    y, m = s.split("-")
    return int(y), int(m)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["stats", "preview", "publish"])
    ap.add_argument("--start", type=month, default=(2026, 7), help="first month, YYYY-MM (default 2026-07)")
    ap.add_argument("--end", type=month, default=(2027, 12), help="last month, YYYY-MM (default 2027-12)")
    ap.add_argument("--today", type=dt.date.fromisoformat, default=None,
                    help="date the Master Dashboard's 'You are here' links point at (default: today)")
    ap.add_argument("--name", default=NOTEBOOK_NAME, help="notebook name")
    ap.add_argument("--out", type=Path, default=Path("preview"), help="preview folder")
    ap.add_argument("--client-id", default=None, help="Azure app (client) ID; see README")
    ap.add_argument("--tenant", default="common", help="'common', 'consumers' or your tenant ID")
    ap.add_argument("--links", choices=["client", "web"], default="client",
                    help="link type inside pages: OneNote app links (default) or web links")
    ap.add_argument("--state", type=Path, default=Path(".heyfinora-state.json"),
                    help="progress file used to resume an interrupted publish")
    a = ap.parse_args()

    nb = build_notebook(a.start, a.end, a.today, a.name)

    if a.command == "stats":
        total = 0
        for item in nb.items:
            sections = item.sections if isinstance(item, Group) else [item]
            n = sum(len(s.pages) for s in sections)
            total += n
            print(f"{item.name:<28}{len(sections):>3} section(s){n:>5} pages")
        print(f"{'TOTAL':<42}{total:>5} pages")
        return 0

    if a.command == "preview":
        from heyfinora.preview import write_preview
        print("Preview written to", write_preview(nb, a.out))
        return 0

    from heyfinora.graph import DEFAULT_CLIENT_ID, Graph, Publisher
    graph = Graph(a.client_id or DEFAULT_CLIENT_ID, Path(".heyfinora-token.json"), a.tenant)
    Publisher(graph, a.state, a.links).publish(nb)
    print_subpage_steps(nb)
    return 0


def print_subpage_steps(nb) -> None:
    """The Graph API cannot make subpages, so list the pages to indent by hand."""
    print("\nLast step in OneNote: make these pages subpages (select them, then Ctrl+Alt+] on Windows,"
          " or right-click → Make Subpage). Day pages you add later go one level deeper.")
    for group, s in nb.sections():
        sub = [p for p in s.pages if p.level > 1]
        if sub:
            where = f"{group.name} › {s.name}" if group else s.name
            print(f"  {where}: {len(sub)} pages – e.g. {sub[0].title}")


if __name__ == "__main__":
    sys.exit(main())
