import datetime as dt
import html
import re

import pytest

from heyfinora.core import Group, render_body, render_page, safe_name
from heyfinora.dates import Calendar, Week
from heyfinora.notebook import build_notebook


@pytest.fixture(scope="module")
def nb():
    return build_notebook(today=dt.date(2026, 9, 24))


def count(nb, prefix):
    return sum(len(s.pages) for item in nb.items if item.name.startswith(prefix)
               for s in (item.sections if isinstance(item, Group) else [item]))


def test_blueprint_page_counts(nb):
    assert sum(1 for _ in nb.pages()) == 284
    expected = {"00": 7, "01": 3, "02": 47, "03": 88, "04": 7, "05": 5, "06": 23, "07": 8, "08": 11,
                "09": 27, "10": 4, "11": 3, "12": 7, "13": 3, "14": 36, "15": 5}
    assert {k: count(nb, k) for k in expected} == expected
    assert len(nb.items) == 16


def test_keys_unique(nb):
    keys = [p.key for _, p in nb.pages()]
    assert len(keys) == len(set(keys))


def test_weeks_belong_to_thursday_month():
    cal = Calendar()
    assert cal.weeks[0] == Week(2026, 27) and cal.weeks[-1] == Week(2027, 52)
    assert len([w for w in cal.weeks if w.iso_year == 2026]) == 27
    assert len([w for w in cal.weeks if w.iso_year == 2027]) == 52
    assert Week(2026, 53).home.month == 12


def test_current_pointers(nb):
    assert nb.current == {"year": "plan.2026.year", "quarter": "plan.2026.q3",
                          "month": "plan.2026.m09", "week": "plan.2026.w39"}


# Links that are intentionally dead: periods outside the planner's range, template placeholders.
ALLOWED_MISSING = re.compile(r"^(None|plan\.(2025|2028)\.year|plan\.2026\.q[12])$")


def test_every_link_resolves(nb):
    keys = nb.page_keys()
    missing = set()

    def resolve(key):
        if key in keys:
            return "x"
        missing.add(key)
        return None

    for s, p in nb.pages():
        render_body(nb, s, p, resolve)
    assert {k for k in missing if not ALLOWED_MISSING.match(k)} == set()


def test_templates_link_only_to_fixed_pages(nb):
    # The global bar's PLAN link (current Year Dashboard) is a hub, so it is allowed.
    dated = re.compile(r"^(plan\.(?!\d{4}\.year$)|money\.budget\.|habits\.tracker\.)")
    keys = nb.page_keys()
    tpl = next(i for i in nb.items if i.key == "tpl")
    for s in tpl.sections:
        for p in s.pages:
            seen = set()
            render_body(nb, s, p, lambda k: seen.add(k) or ("x" if k in keys else None))
            assert not {k for k in seen if dated.match(k)}, p.title


def test_names_are_graph_safe(nb):
    for g, s in nb.sections():
        for name in [s.name] + ([g.name] if g else []):
            clean = safe_name(name)
            assert len(clean) <= 50 and not re.search(r"[?*\\/:<>|&#'\"%~]", clean)


def test_page_html_has_replaceable_body(nb):
    s, p = next(iter(nb.pages()))
    doc = render_page(nb, s, p, lambda k: None)
    assert '<div data-id="body">' in doc and f"<title>{html.escape(p.title)}</title>" in doc
