"""Build the blog HTML page from its Markdown source.

Usage: python3 blog/src/build.py  (requires: pip install markdown)
"""
import json
import pathlib
import re

import markdown

BLOG = pathlib.Path(__file__).resolve().parent.parent
SLUG = "debt-payoff-spreadsheet-snowball-vs-avalanche"

raw = (BLOG / f"{SLUG}.md").read_text(encoding="utf-8")
_, front, body = raw.split("---\n", 2)
meta = dict(re.findall(r'^(\w+): "?(.*?)"?$', front, re.M))

md = markdown.Markdown(extensions=["tables", "toc", "attr_list"])
html = md.convert(body)
# The page template renders the H1 itself.
html = re.sub(r"<h1[^>]*>.*?</h1>\s*", "", html, count=1, flags=re.S)
html = html.replace('<a href="http', '<a rel="noopener" target="_blank" href="http')

toc = "".join(
    f'<li><a href="#{t["id"]}">{t["name"]}</a></li>'
    for t in md.toc_tokens[0]["children"]
)

# FAQ structured data for search engines.
faq = re.findall(r"^### (.+\?)\n\n(.+?)$", body.split("## Frequently Asked Questions")[1], re.M)
schema = {
    "@context": "https://schema.org",
    "@graph": [
        {"@type": "Article", "headline": meta["title"], "description": meta["description"],
         "author": {"@type": "Organization", "name": "HEYFINORA"}},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
    ],
}

template = (BLOG / "src" / "template.html").read_text(encoding="utf-8")
out = (template
       .replace("{{title}}", meta["title"])
       .replace("{{description}}", meta["description"])
       .replace("{{schema}}", json.dumps(schema, indent=1))
       .replace("{{toc}}", toc)
       .replace("{{body}}", html))
(BLOG / f"{SLUG}.html").write_text(out, encoding="utf-8")
print("wrote", BLOG / f"{SLUG}.html")
