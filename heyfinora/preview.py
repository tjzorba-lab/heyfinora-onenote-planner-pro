"""Offline preview: one HTML file per page plus a clickable notebook tree."""
from __future__ import annotations

import html
from pathlib import Path

from .core import Group, Notebook, THEME, render_body

CSS = f"""
body {{ font-family: '{THEME["font"]}', Calibri, Arial, sans-serif; background:#FFFFFF; color:{THEME["ink"]};
       margin:0 auto; padding:16px; max-width:820px; }}
table {{ border-collapse:collapse; margin:4px 0; max-width:100%; }}
td {{ vertical-align:top; padding:2px 6px; border-color:{THEME["line"]}; }}
td p, li {{ margin:2px 0; }}
p[data-tag^="to-do"]::before {{ content:"☐ "; color:{THEME["teal"]}; }}
p[data-tag="to-do:completed"]::before {{ content:"☑ "; }}
.title {{ font-size:22pt; color:{THEME["navy"]}; border-bottom:1px solid {THEME["line"]}; margin:12px 0; }}
.l2 {{ margin-left:18px; }} .l3 {{ margin-left:36px; }}
"""


def _file(key: str) -> str:
    return key.replace("/", "_") + ".html"


def write_preview(nb: Notebook, out: Path) -> Path:
    out.mkdir(parents=True, exist_ok=True)
    keys = nb.page_keys()

    def resolve(key: str):
        return _file(key) if key in keys else None

    for section, page in nb.pages():
        body = render_body(nb, section, page, resolve)
        doc = (f"<!DOCTYPE html><html><head><meta charset='utf-8'><title>{html.escape(page.title)}</title>"
               f"<meta name='viewport' content='width=device-width, initial-scale=1'><style>{CSS}</style></head>"
               f"<body><p><a href='index.html'>☰ Notebook</a> · {html.escape(section.name)}</p>"
               f"<div class='title'>{html.escape(page.title)}</div>{body}</body></html>")
        (out / _file(page.key)).write_text(doc, encoding="utf-8")

    tree = [f"<h1>{html.escape(nb.name)}</h1>"]
    for item in nb.items:
        sections = item.sections if isinstance(item, Group) else [item]
        tree.append(f"<h2>{html.escape(item.name)}</h2>")
        for s in sections:
            if isinstance(item, Group):
                tree.append(f"<h3>{html.escape(s.name)}</h3>")
            tree.append("<ul>" + "".join(
                f"<li class='l{p.level}'><a href='{_file(p.key)}'>{html.escape(p.title)}</a></li>"
                for p in s.pages) + "</ul>")
    total = sum(1 for _ in nb.pages())
    index = (f"<!DOCTYPE html><html><head><meta charset='utf-8'><title>{html.escape(nb.name)}</title>"
             f"<meta name='viewport' content='width=device-width, initial-scale=1'><style>{CSS}</style></head>"
             f"<body><p>{total} pages</p>{''.join(tree)}</body></html>")
    (out / "index.html").write_text(index, encoding="utf-8")
    return out / "index.html"
