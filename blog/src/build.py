"""Build the blog HTML page from its Markdown source.

Usage: python3 blog/src/build.py [commit]  (requires: pip install markdown)

The Blogger version loads images from the given commit (default HEAD), so
push the images before pasting it into Blogger.
"""
import json
import pathlib
import re
import subprocess
import sys

import markdown

BLOG = pathlib.Path(__file__).resolve().parent.parent
SLUG = "debt-payoff-spreadsheet-snowball-vs-avalanche"
REPO = "tjzorba-lab/heyfinora-onenote-planner-pro"

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

# Blogger version: post body only, images served from the public repo via
# jsDelivr pinned to the commit given as the first argument (default: HEAD).
rev = sys.argv[1] if len(sys.argv) > 1 else subprocess.check_output(
    ["git", "rev-parse", "HEAD"], cwd=BLOG, text=True).strip()
cdn = f"https://cdn.jsdelivr.net/gh/{REPO}@{rev}/blog/images/"
bhtml = html.replace('src="images/', f'src="{cdn}')
bhtml = re.sub(r"(<table>.*?</table>)", r'<div class="hf-table">\1</div>', bhtml, flags=re.S)
intro, rest = bhtml.split("<h2", 1)
blogger = ((BLOG / "src" / "blogger.html").read_text(encoding="utf-8")
           .replace("{{schema}}", json.dumps(schema, indent=1))
           .replace("{{toc}}", toc)
           .replace("{{intro}}", intro.strip())
           .replace("{{rest}}", "<h2" + rest))
(BLOG / f"{SLUG}-blogger.html").write_text(blogger, encoding="utf-8")
print("wrote", BLOG / f"{SLUG}-blogger.html", "images @", rev[:7])
