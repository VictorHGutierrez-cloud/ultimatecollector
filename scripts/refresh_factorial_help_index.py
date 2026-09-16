#!/usr/bin/env python3
"""Refresh docs/factorial-help/catalog.json and INDEX.md from Factorial Help Center.

Uses category Atom feeds (Helpjuice) plus homepage/subcategory discovery.
Does NOT copy full article bodies — only titles, URLs, and short snippets.

Usage (from repo root):
  python scripts/refresh_factorial_help_index.py
"""
from __future__ import annotations

import json
import re
import time
import urllib.request
from html import unescape
from pathlib import Path
from urllib.parse import urlparse, unquote

BASE = "https://help.factorialhr.com"
ATOM_BASE = "https://factorial.helpjuice.com"
LOCALE = "en_US"
HOME = f"{BASE}/{LOCALE}"
UA = "Mozilla/5.0 (compatible; UltimateCollectorHelpIndex/1.0)"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "factorial-help"

# Sidebar / nav noise that appears as a fake "see-more" on many parent pages
NOISE_SUBCATEGORY_SLUGS = {
    "new-to-factorial-start-here",
    "search",
    "support",
    "login",
    "contact",
}

# Extra leaf slugs to probe if missing from parent discovery
EXTRA_LEAVES = [
    "time-tracking",
    "absences-approvals",
    "time-off-settings",
    "shift-management",
    "time-off-deductions",
    "performance-review",
    "competencies-goals",
    "surveys-enps",
    "organisation",
    "organization",
    "managing-my-company-account",
    "device-management",
    "job-catalog",
    "permissions",
    "automations",
]


def fetch(url: str, retries: int = 3) -> str:
    last_err: Exception | None = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.read().decode("utf-8", "replace")
        except Exception as err:  # noqa: BLE001
            last_err = err
            time.sleep(1.2 * (attempt + 1))
    raise RuntimeError(f"Failed to fetch {url}: {last_err}")


def strip_tags(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    text = unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def normalize_public_url(url: str) -> str:
    url = url.split("?")[0].rstrip("/")
    if "help.factorialhr.com" in url:
        return url
    path = urlparse(url).path
    parts = [unquote(p) for p in path.split("/") if p]
    if parts and parts[0] == LOCALE:
        parts = parts[1:]
    if not parts:
        return url
    return f"{BASE}/{LOCALE}/{'/'.join(parts)}"


def extract_top_categories(home_html: str) -> list[dict]:
    cats: list[dict] = []
    seen: set[str] = set()
    for href, title in re.findall(
        r'<a[^>]+href="(/en_US/[a-z0-9\-]+/?)"[^>]*>.*?<[^>]*class="[^"]*category-name[^"]*"[^>]*>(.*?)</',
        home_html,
        flags=re.I | re.S,
    ):
        slug = href.strip("/").split("/")[-1]
        title = strip_tags(title)
        if slug in seen or not title:
            continue
        seen.add(slug)
        cats.append({"slug": slug, "title": title, "url": f"{BASE}/{LOCALE}/{slug}"})
    if cats:
        return cats

    # Fallback ordered list from Help Center homepage themes
    fallback = [
        ("new-to-factorial-start-here", "New to Factorial? Start here!"),
        ("one", "ONE"),
        ("time-tracking-absences", "Time tracking & Absences"),
        ("projects", "Projects"),
        ("payroll", "Compensation and benefits"),
        ("finance", "Finance"),
        ("documents-signatures", "Documents & E-Signatures"),
        ("recruitment-organization", "Recruitment & Organization"),
        ("permissions-workflows", "Permissions & Workflows"),
        ("performance-engagement", "Performance & Engagement"),
        ("training", "Training"),
        ("apps-integrations", "Apps & Integrations"),
        ("it-management", "IT Management"),
        ("notifications", "Notifications"),
        ("ticketing-and-policies", "Ticketing and policies"),
        ("billing-subscription-cancellation", "Billing, Subscription & Cancellation"),
        ("need-help-contact-support", "Need Help? Contact Support"),
    ]
    return [{"slug": s, "title": t, "url": f"{BASE}/{LOCALE}/{s}"} for s, t in fallback]


def extract_subcategories(html: str, parent_url: str) -> list[dict]:
    subs: list[dict] = []
    seen: set[str] = set()
    parent_slug = parent_url.rstrip("/").split("/")[-1]

    def add(slug: str, title: str) -> None:
        if not slug or slug == parent_slug or slug in NOISE_SUBCATEGORY_SLUGS:
            return
        if slug in seen:
            for s in subs:
                if s["slug"] == slug and title and len(title) > len(s["title"]):
                    s["title"] = title
            return
        seen.add(slug)
        subs.append(
            {
                "slug": slug,
                "title": title or slug.replace("-", " ").title(),
                "url": f"{BASE}/{LOCALE}/{slug}",
            }
        )

    for href in re.findall(
        r'href="(/en_US/[a-z0-9\-]+/?)"[^>]*class="[^"]*see-more[^"]*"',
        html,
        flags=re.I,
    ):
        add(href.strip("/").split("/")[-1], "")
    for href in re.findall(
        r'class="[^"]*see-more[^"]*"[^>]*href="(/en_US/[a-z0-9\-]+/?)"',
        html,
        flags=re.I,
    ):
        add(href.strip("/").split("/")[-1], "")

    for block in re.findall(
        r'<li[^>]*class="[^"]*subcategory-list-element[^"]*"[^>]*>(.*?)</li>',
        html,
        flags=re.I | re.S,
    ):
        m = re.search(r'<a[^>]+href="(/en_US/[a-z0-9\-]+/?)"[^>]*>(.*?)</a>', block, flags=re.I | re.S)
        if not m:
            continue
        href, title = m.group(1), strip_tags(m.group(2))
        if title.lower() in {"see more", "see all", "learn more"}:
            title = ""
        add(href.strip("/").split("/")[-1], title)

    return subs


def parse_atom(atom: str) -> list[dict]:
    articles: list[dict] = []
    for entry in re.findall(r"<entry>(.*?)</entry>", atom, flags=re.I | re.S):
        tm = re.search(r"<title[^>]*>(.*?)</title>", entry, flags=re.I | re.S)
        lm = re.search(r'<link[^>]+href="([^"]+)"', entry, flags=re.I)
        sm = re.search(r"<summary[^>]*>(.*?)</summary>", entry, flags=re.I | re.S)
        if not tm or not lm:
            continue
        title = strip_tags(tm.group(1))
        raw_url = lm.group(1)
        public = normalize_public_url(raw_url)
        snippet = strip_tags(sm.group(1))[:320] if sm else ""
        slug = public.rstrip("/").split("/")[-1]
        articles.append(
            {
                "title": title,
                "url": public,
                "atom_url": raw_url.split("?")[0],
                "slug": unquote(slug),
                "snippet": snippet,
            }
        )
    by_url = {a["url"]: a for a in articles}
    return sorted(by_url.values(), key=lambda x: x["title"].lower())


def fetch_atom_articles(slug: str) -> list[dict]:
    try:
        atom = fetch(f"{ATOM_BASE}/{LOCALE}/{slug}.atom")
    except Exception:
        return []
    if "<entry>" not in atom.lower():
        return []
    return parse_atom(atom)


def enrich_leaf_title(slug: str, fallback: str) -> str:
    try:
        html = fetch(f"{BASE}/{LOCALE}/{slug}")
        m = re.search(r"<h1[^>]*>(.*?)</h1>", html, flags=re.I | re.S)
        if m:
            t = strip_tags(m.group(1))
            if t:
                return t
    except Exception:
        pass
    return fallback


def write_index_md(catalog: dict) -> None:
    lines: list[str] = []
    lines.append("# Factorial Help Center — Index")
    lines.append("")
    lines.append(f"- Source: {catalog['source']}")
    lines.append(f"- Locale: `{catalog['locale']}`")
    lines.append(f"- Fetched at (UTC): `{catalog['fetched_at']}`")
    lines.append(
        f"- Leaf categories: **{catalog['stats']['leaf_category_count']}** | "
        f"Articles: **{catalog['stats']['article_count']}**"
    )
    lines.append("")
    lines.append("## Top categories (Help Center home)")
    lines.append("")
    for t in catalog.get("top_categories", []):
        subs = ", ".join(f"`{s}`" for s in t.get("subcategory_slugs") or []) or "_(leaf / own articles)_"
        title = t.get("title") or t["slug"]
        lines.append(f"- [{title}]({t['url']}) — subs: {subs}")
    lines.append("")
    lines.append("## Categories and articles")
    lines.append("")

    # Group by parent when possible
    by_slug = {c["slug"]: c for c in catalog["categories"]}
    parent_to_children: dict[str | None, list[dict]] = {}
    for c in catalog["categories"]:
        parent_to_children.setdefault(c.get("parent_slug"), []).append(c)

    # Print orphans / roots first ordered by title, then children under parents from top_categories
    printed: set[str] = set()
    for top in catalog.get("top_categories", []):
        lines.append(f"### {top.get('title') or top['slug']}")
        lines.append("")
        lines.append(f"Parent page: {top['url']}")
        lines.append("")
        child_slugs = list(top.get("subcategory_slugs") or [])
        if top["slug"] in by_slug and top["slug"] not in child_slugs:
            child_slugs = [top["slug"]] + child_slugs
        for slug in child_slugs:
            c = by_slug.get(slug)
            if not c or slug in printed:
                continue
            printed.add(slug)
            lines.append(f"#### {c['title']} (`{c['slug']}`) — {c['article_count']} articles")
            lines.append("")
            lines.append(f"Category: {c['url']}")
            lines.append("")
            if not c["articles"]:
                lines.append("_No articles in Atom feed (category may be a hub or empty)._")
                lines.append("")
                continue
            for a in c["articles"]:
                snip = f" — {a['snippet']}" if a.get("snippet") else ""
                lines.append(f"- [{a['title']}]({a['url']}){snip}")
            lines.append("")

    leftovers = [c for c in catalog["categories"] if c["slug"] not in printed]
    if leftovers:
        lines.append("### Other / discovered categories")
        lines.append("")
        for c in sorted(leftovers, key=lambda x: x["title"].lower()):
            lines.append(f"#### {c['title']} (`{c['slug']}`) — {c['article_count']} articles")
            lines.append("")
            lines.append(f"Category: {c['url']}")
            lines.append("")
            for a in c["articles"]:
                snip = f" — {a['snippet']}" if a.get("snippet") else ""
                lines.append(f"- [{a['title']}]({a['url']}){snip}")
            lines.append("")

    (OUT / "INDEX.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    print("Fetching homepage...")
    home = fetch(HOME)
    top = extract_top_categories(home)
    print(f"Top categories: {len(top)}")

    leaves: dict[str, dict] = {}
    parents: list[dict] = []

    for cat in top:
        print(f"Inspecting: {cat['slug']}")
        try:
            html = fetch(cat["url"])
        except Exception as err:
            print("  FAIL", err)
            continue
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html, flags=re.I | re.S)
        if h1:
            cat["title"] = strip_tags(h1.group(1)) or cat["title"]
        if not cat.get("title"):
            cat["title"] = cat["slug"].replace("-", " ").title()

        subs = extract_subcategories(html, cat["url"])
        atom_articles = fetch_atom_articles(cat["slug"])
        parents.append(
            {
                "slug": cat["slug"],
                "title": cat["title"],
                "url": cat["url"],
                "subcategory_slugs": [s["slug"] for s in subs],
                "is_leaf": bool(atom_articles) and not subs,
            }
        )

        if atom_articles and not subs:
            leaves[cat["slug"]] = {
                "slug": cat["slug"],
                "title": cat["title"],
                "url": cat["url"],
                "parent_slug": None,
                "articles": atom_articles,
            }
            print(f"  leaf {len(atom_articles)}")
        elif subs:
            print(f"  parent -> {len(subs)} subs")
            for s in subs:
                if s["slug"] in leaves:
                    continue
                arts = fetch_atom_articles(s["slug"])
                title = enrich_leaf_title(s["slug"], s["title"])
                leaves[s["slug"]] = {
                    "slug": s["slug"],
                    "title": title,
                    "url": s["url"],
                    "parent_slug": cat["slug"],
                    "articles": arts,
                }
                print(f"    {s['slug']}: {len(arts)} | {title}")
                time.sleep(0.2)
            if atom_articles:
                leaves[cat["slug"]] = {
                    "slug": cat["slug"],
                    "title": cat["title"],
                    "url": cat["url"],
                    "parent_slug": None,
                    "articles": atom_articles,
                }
                print(f"  own articles: {len(atom_articles)}")
        else:
            leaves[cat["slug"]] = {
                "slug": cat["slug"],
                "title": cat["title"],
                "url": cat["url"],
                "parent_slug": None,
                "articles": atom_articles,
            }
            print(f"  no subs; articles={len(atom_articles)}")
        time.sleep(0.25)

    for slug in EXTRA_LEAVES:
        if slug in leaves:
            continue
        arts = fetch_atom_articles(slug)
        if not arts:
            continue
        title = enrich_leaf_title(slug, slug.replace("-", " ").title())
        leaves[slug] = {
            "slug": slug,
            "title": title,
            "url": f"{BASE}/{LOCALE}/{slug}",
            "parent_slug": None,
            "articles": arts,
        }
        print(f"Extra {slug}: {len(arts)} | {title}")
        time.sleep(0.2)

    # Keep leaves with articles, top-level hubs, or parent-linked empty stubs.
    top_slugs = {p["slug"] for p in parents}
    categories = []
    for leaf in sorted(leaves.values(), key=lambda x: x["title"].lower()):
        keep = bool(leaf["articles"]) or leaf["slug"] in top_slugs or bool(leaf.get("parent_slug"))
        if not keep:
            continue
        categories.append(
            {
                "slug": leaf["slug"],
                "title": leaf["title"],
                "url": leaf["url"],
                "parent_slug": leaf.get("parent_slug"),
                "article_count": len(leaf["articles"]),
                "articles": leaf["articles"],
            }
        )

    catalog = {
        "source": HOME,
        "locale": LOCALE,
        "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "top_categories": parents,
        "categories": categories,
        "stats": {
            "top_category_count": len(parents),
            "leaf_category_count": len(categories),
            "article_count": sum(c["article_count"] for c in categories),
        },
    }

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "catalog.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    write_index_md(catalog)
    print("Wrote", OUT / "catalog.json")
    print("Wrote", OUT / "INDEX.md")
    print(json.dumps(catalog["stats"], indent=2))


if __name__ == "__main__":
    main()
