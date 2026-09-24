"""Create the notebook in the signed-in user's OneNote through Microsoft Graph.

Pass 1 creates the notebook, section groups, sections and pages (in order).
Pass 2 rewrites every page body once all page links are known, so the
navigation bars, breadcrumbs and prev/next links point at real pages.
Progress is saved to a state file, so an interrupted run can be resumed.
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Callable, Optional

import msal
import requests

from .core import Group, Notebook, render_body, render_page, safe_name

API = "https://graph.microsoft.com/v1.0/me/onenote"
# "Microsoft Graph Command Line Tools", Microsoft's public client for scripts.
DEFAULT_CLIENT_ID = "14d82eec-204b-4c2f-b7e8-296a70dab67e"
SCOPES = ["Notes.ReadWrite"]
RETRY_STATUS = {429, 500, 502, 503, 504}


class GraphError(RuntimeError):
    pass


class Graph:
    def __init__(self, client_id: str, cache_path: Path, tenant: str = "common",
                 log: Callable[[str], None] = print):
        self.log = log
        self.cache_path = cache_path
        self.cache = msal.SerializableTokenCache()
        if cache_path.exists():
            self.cache.deserialize(cache_path.read_text())
        self.app = msal.PublicClientApplication(
            client_id, authority=f"https://login.microsoftonline.com/{tenant}", token_cache=self.cache)
        self.session = requests.Session()

    def _save_cache(self) -> None:
        if self.cache.has_state_changed:
            self.cache_path.write_text(self.cache.serialize())

    def token(self) -> str:
        accounts = self.app.get_accounts()
        result = self.app.acquire_token_silent(SCOPES, account=accounts[0]) if accounts else None
        if not result:
            flow = self.app.initiate_device_flow(scopes=SCOPES)
            if "user_code" not in flow:
                raise GraphError(f"Could not start sign-in: {flow.get('error_description', flow)}")
            self.log("\n" + flow["message"] + "\n")
            result = self.app.acquire_token_by_device_flow(flow)
        self._save_cache()
        if "access_token" not in result:
            raise GraphError(f"Sign-in failed: {result.get('error_description', result)}")
        return result["access_token"]

    def request(self, method: str, path: str, *, json_body=None, html: Optional[str] = None,
                ok=(200, 201, 204)) -> Optional[dict]:
        url = path if path.startswith("http") else API + path
        for attempt in range(8):
            headers = {"Authorization": f"Bearer {self.token()}"}
            kwargs = {}
            if html is not None:
                headers["Content-Type"] = "text/html"
                kwargs["data"] = html.encode("utf-8")
            elif json_body is not None:
                kwargs["json"] = json_body
            try:
                r = self.session.request(method, url, headers=headers, timeout=120, **kwargs)
            except requests.RequestException as e:
                wait = min(60, 2 ** attempt)
                self.log(f"  network error ({e.__class__.__name__}); retrying in {wait}s")
                time.sleep(wait)
                continue
            if r.status_code in ok:
                return r.json() if r.content else None
            if r.status_code in RETRY_STATUS:
                wait = int(r.headers.get("Retry-After", min(60, 2 ** (attempt + 1))))
                self.log(f"  Graph busy ({r.status_code}); waiting {wait}s")
                time.sleep(wait)
                continue
            raise GraphError(f"{method} {url} failed: {r.status_code} {r.text[:500]}")
        raise GraphError(f"{method} {url} kept failing after retries")

    def find(self, path: str, name: str) -> Optional[dict]:
        safe = name.replace("'", "''")
        res = self.request("GET", f"{path}?$filter=displayName eq '{safe}'")
        items = (res or {}).get("value", [])
        return items[0] if items else None


def _links(obj: dict) -> dict:
    links = obj.get("links", {})
    return {"id": obj["id"],
            "client": links.get("oneNoteClientUrl", {}).get("href"),
            "web": links.get("oneNoteWebUrl", {}).get("href")}


class Publisher:
    def __init__(self, graph: Graph, state_path: Path, link_style: str = "client",
                 log: Callable[[str], None] = print):
        self.g, self.state_path, self.link_style, self.log = graph, state_path, link_style, log
        self.state = (json.loads(state_path.read_text()) if state_path.exists() else
                      {"notebook": None, "groups": {}, "sections": {}, "pages": {}, "linked": []})

    def save(self) -> None:
        self.state_path.write_text(json.dumps(self.state, indent=1))

    def resolve(self, key: str) -> Optional[str]:
        page = self.state["pages"].get(key)
        return page.get(self.link_style) or page.get("web") if page else None

    # ---- containers --------------------------------------------------------
    def _notebook(self, name: str) -> str:
        if self.state["notebook"]:
            return self.state["notebook"]
        if self.g.find("/notebooks", name):
            raise GraphError(f"A notebook called “{name}” already exists but this state file doesn't know it. "
                             "Delete or rename that notebook, or use --name for a new one.")
        nb = self.g.request("POST", "/notebooks", json_body={"displayName": name})
        self.state["notebook"] = nb["id"]
        self.save()
        self.log(f"Created notebook: {name}")
        return nb["id"]

    def _container(self, bucket: str, key: str, parent: str, kind: str, name: str) -> str:
        if key in self.state[bucket]:
            return self.state[bucket][key]["id"]
        path = f"{parent}/{kind}"
        obj = self.g.find(path, name) or self.g.request("POST", path, json_body={"displayName": name})
        self.state[bucket][key] = _links(obj)
        self.save()
        self.log(f"  {kind[:-1]}: {name}")
        return obj["id"]

    # ---- pages ---------------------------------------------------------------
    def _create_page(self, nb: Notebook, section, page, section_id: str) -> None:
        html = render_page(nb, section, page, self.resolve)
        try:
            obj = self.g.request("POST", f"/sections/{section_id}/pages", html=html)
        except GraphError:
            # The page may have been created before the error; adopt it rather than duplicate.
            obj = self._find_page(section_id, page.title)
            if not obj:
                raise
        self.state["pages"][page.key] = _links(obj)
        self.save()

    def _find_page(self, section_id: str, title: str) -> Optional[dict]:
        res = self.g.request("GET", f"/sections/{section_id}/pages?$select=id,title,links&$top=100")
        for p in (res or {}).get("value", []):
            if p.get("title") == title:
                return p
        return None

    def publish(self, nb: Notebook) -> None:
        nb_id = self._notebook(nb.name)
        total = sum(1 for _ in nb.pages())
        done = len(self.state["pages"])
        self.log(f"Pass 1/2 – creating sections and {total} pages ({done} already done)")
        for item in nb.items:
            if isinstance(item, Group):
                parent = "/sectionGroups/" + self._container(
                    "groups", item.key, f"/notebooks/{nb_id}", "sectionGroups", safe_name(item.name))
                sections = item.sections
            else:
                parent, sections = f"/notebooks/{nb_id}", [item]
            for s in sections:
                sid = self._container("sections", s.key, parent, "sections", safe_name(s.name))
                for p in s.pages:
                    if p.key in self.state["pages"]:
                        continue
                    self._create_page(nb, s, p, sid)
                    done += 1
                    self.log(f"    [{done}/{total}] {p.title}")

        self.log("Pass 2/2 – adding links to every page")
        linked = set(self.state["linked"])
        n = len(linked)
        for s, p in nb.pages():
            if p.key in linked:
                continue
            body = render_body(nb, s, p, self.resolve)
            page_id = self.state["pages"][p.key]["id"]
            self.g.request("PATCH", f"/pages/{page_id}/content", json_body=[
                {"target": "#body", "action": "replace", "content": f'<div data-id="body">{body}</div>'}])
            linked.add(p.key)
            self.state["linked"].append(p.key)
            self.save()
            n += 1
            self.log(f"    [{n}/{total}] linked {p.title}")
        self.log("Done. Open OneNote and look for the notebook: " + nb.name)
