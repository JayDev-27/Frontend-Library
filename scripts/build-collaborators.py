#!/usr/bin/env python3
"""Generate a single circular-avatar collaborators SVG and update README.md.

    python3 scripts/build-collaborators.py

Reads collaborators (accepted) and pending invitations from the GitHub REST API
(via ``gh api`` if available, or HTTPS API using ``GITHUB_TOKEN``) so both accepted
collaborators and newly invited members appear in one combined 12-column circular avatar grid.
"""
from __future__ import annotations

import base64
import json
import os
import re
import shutil
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
OUT_SVG = ROOT / ".github/assets/generated/collaborators.svg"
README_PATH = ROOT / "README.md"
REPO = os.environ.get("GITHUB_REPOSITORY", "JayDev-27/Frontend-Library")

LIVE_URL = "https://frontendlibrary.vercel.app/api/collaborators/"

START_MARKER = "<!-- COLLABORATORS:START -->"
END_MARKER = "<!-- COLLABORATORS:END -->"

AVATAR_SIZE = 64
GAP = 8
COLUMNS = 12

FALLBACK_MEMBERS = [
    {"login": "satiricalguru", "status": "collaborator", "avatar_url": "https://avatars.githubusercontent.com/u/227462757?v=4", "is_owner": True},
    {"login": "auroraeye-dev", "status": "collaborator", "avatar_url": "https://avatars.githubusercontent.com/u/191999359?v=4", "is_owner": False},
    {"login": "eshikaatreya", "status": "collaborator", "avatar_url": "https://avatars.githubusercontent.com/u/317296881?v=4", "is_owner": False},
    {"login": "JayDev-27", "status": "collaborator", "avatar_url": "https://avatars.githubusercontent.com/u/279688498?v=4", "is_owner": False},
    {"login": "Mxhi-04", "status": "collaborator", "avatar_url": "https://avatars.githubusercontent.com/u/249584456?v=4", "is_owner": False},
    {"login": "Phantom-lj", "status": "collaborator", "avatar_url": "https://avatars.githubusercontent.com/u/86778112?v=4", "is_owner": False},
    {"login": "pratejash", "status": "collaborator", "avatar_url": "https://avatars.githubusercontent.com/u/320674383?v=4", "is_owner": False},
    {"login": "Rashmi-builds", "status": "collaborator", "avatar_url": "https://avatars.githubusercontent.com/u/317297793?v=4", "is_owner": False},
    {"login": "Vedant275", "status": "collaborator", "avatar_url": "https://avatars.githubusercontent.com/u/218742536?v=4", "is_owner": False},
    {"login": "Aaravcodesss", "status": "invited", "avatar_url": "https://avatars.githubusercontent.com/u/212439928?v=4", "is_owner": False},
    {"login": "arsh-WINsingh", "status": "invited", "avatar_url": "https://avatars.githubusercontent.com/u/275754707?v=4", "is_owner": False},
    {"login": "ChetasLua", "status": "invited", "avatar_url": "https://avatars.githubusercontent.com/u/140589714?v=4", "is_owner": False},
    {"login": "jasroopbhinder", "status": "invited", "avatar_url": "https://avatars.githubusercontent.com/u/305776386?v=4", "is_owner": False},
    {"login": "jassi-mocking-it", "status": "invited", "avatar_url": "https://avatars.githubusercontent.com/u/259535430?v=4", "is_owner": False},
    {"login": "nullprsn", "status": "invited", "avatar_url": "https://avatars.githubusercontent.com/u/78124544?v=4", "is_owner": False},
    {"login": "pedroiff0", "status": "invited", "avatar_url": "https://avatars.githubusercontent.com/u/137837852?v=4", "is_owner": False},
    {"login": "prabhakarkavyansh", "status": "invited", "avatar_url": "https://avatars.githubusercontent.com/u/318371832?v=4", "is_owner": False},
    {"login": "ravindrasinghp933-blip", "status": "invited", "avatar_url": "https://avatars.githubusercontent.com/u/343925505?v=4", "is_owner": False},
    {"login": "Saket-code40", "status": "invited", "avatar_url": "https://avatars.githubusercontent.com/u/185668607?v=4", "is_owner": False},
    {"login": "yashadityaixd7544-oss", "status": "invited", "avatar_url": "https://avatars.githubusercontent.com/u/244797493?v=4", "is_owner": False},
]


def github_get_json(endpoint: str):
    """Fetch JSON from GitHub API via gh CLI or urllib."""
    if shutil.which("gh"):
        try:
            res = subprocess.run(
                ["gh", "api", f"/repos/{REPO}/{endpoint}?per_page=100"],
                capture_output=True,
                text=True,
                check=True,
            )
            return json.loads(res.stdout)
        except Exception:
            pass

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    url = f"https://api.github.com/repos/{REPO}/{endpoint}?per_page=100"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "Frontend-Library-Collaborators-Builder",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None


def fetch_avatar_data_uri(avatar_url: str) -> str:
    """Download an avatar image over HTTPS and return a data URI."""
    if not avatar_url or not avatar_url.startswith("https://"):
        return ""
    sep = "&" if "?" in avatar_url else "?"
    sized_url = f"{avatar_url}{sep}s=96"
    req = urllib.request.Request(
        sized_url,
        headers={"User-Agent": "Frontend-Library-Collaborators-Builder"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            ctype = resp.headers.get_content_type() or "image/png"
            if not ctype.startswith("image/"):
                ctype = "image/png"
            encoded = base64.b64encode(resp.read()).decode("ascii")
            return f"data:{ctype};base64,{encoded}"
    except Exception:
        return ""


def gather_members() -> list[dict]:
    """Collect all accepted collaborators and pending invitees."""
    people: dict[str, dict] = {}
    owner = "JayDev-27".lower()

    collabs = github_get_json("collaborators")
    if collabs and isinstance(collabs, list):
        for c in collabs:
            login = c.get("login")
            if not login:
                continue
            people[login.lower()] = {
                "login": login,
                "avatar_url": c.get("avatar_url", ""),
                "status": "collaborator",
                "is_owner": login.lower() == owner,
            }

    invites = github_get_json("invitations")
    if invites and isinstance(invites, list):
        for inv in invites:
            invitee = inv.get("invitee")
            if not invitee or not invitee.get("login"):
                continue
            login = invitee["login"]
            if login.lower() not in people:
                people[login.lower()] = {
                    "login": login,
                    "avatar_url": invitee.get("avatar_url", ""),
                    "status": "invited",
                    "is_owner": False,
                }

    if not people:
        for f in FALLBACK_MEMBERS:
            people[f["login"].lower()] = dict(f)
    elif owner not in people:
        people[owner] = {
            "login": "satiricalguru",
            "avatar_url": "https://avatars.githubusercontent.com/u/227462757?v=4",
            "status": "collaborator",
            "is_owner": True,
        }

    entries = list(people.values())
    entries.sort(
        key=lambda x: (
            0 if x.get("is_owner") else (1 if x.get("status") == "collaborator" else 2),
            x["login"].lower(),
        )
    )

    for entry in entries:
        entry["data_uri"] = fetch_avatar_data_uri(entry["avatar_url"])

    return entries


def render_grid_svg(items: list[dict], title: str) -> str:
    """Render a 12-column circular avatar grid SVG matching contributors."""
    cols = min(COLUMNS, max(1, len(items)))
    rows = max(1, (len(items) + COLUMNS - 1) // COLUMNS)
    width = cols * AVATAR_SIZE + (cols - 1) * GAP
    height = rows * AVATAR_SIZE + (rows - 1) * GAP
    radius = AVATAR_SIZE / 2 - 1

    defs = []
    nodes = []
    for idx, item in enumerate(items):
        col = idx % COLUMNS
        row = idx // COLUMNS
        x = col * (AVATAR_SIZE + GAP)
        y = row * (AVATAR_SIZE + GAP)
        cx = AVATAR_SIZE / 2
        cy = AVATAR_SIZE / 2
        clip_id = f"c{idx}"
        role_label = (
            "Owner"
            if item.get("is_owner")
            else "Invited Member"
            if item.get("status") == "invited"
            else "Collaborator"
        )
        label = f"{item['login']} ({role_label})"
        defs.append(f'<clipPath id="{clip_id}"><circle cx="{cx}" cy="{cy}" r="{radius}"/></clipPath>')
        img_tag = (
            f'<image x="1" y="1" width="{AVATAR_SIZE - 2}" height="{AVATAR_SIZE - 2}" '
            f'xlink:href="{item["data_uri"]}" clip-path="url(#{clip_id})" preserveAspectRatio="xMidYMid slice"/>'
            if item.get("data_uri")
            else f'<text x="{cx}" y="{cy + 7}" text-anchor="middle" font-family="Arial,sans-serif" font-size="20" fill="#d0d7de">{escape(item["login"][:2].upper())}</text>'
        )
        nodes.append(
            f'<g transform="translate({x},{y})">'
            f"<title>{escape(label)}</title>"
            f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="#0d1117"/>'
            f"{img_tag}"
            f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="#d0d7de" stroke-opacity="0.7" stroke-width="1.5"/>'
            f"</g>"
        )

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">'
        f"<title>{escape(title)}</title>"
        f"<defs>{''.join(defs)}</defs>"
        f"{''.join(nodes)}"
        f"</svg>\n"
    )


def update_readme() -> None:
    """Ensure the Collaborators marker block in README.md is present and up to date."""
    text = README_PATH.read_text(encoding="utf-8")
    block = (
        f"{START_MARKER}\n"
        f'<a href="https://github.com/{REPO}">\n'
        f'  <img src="{LIVE_URL}" alt="Frontend Library collaborators and invited members (updates automatically)">\n'
        f"</a>\n"
        f"{END_MARKER}"
    )

    if START_MARKER in text and END_MARKER in text:
        pattern = re.compile(
            re.escape(START_MARKER) + r"[\s\S]*?" + re.escape(END_MARKER),
            re.MULTILINE,
        )
        updated = pattern.sub(lambda _: block, text, count=1)
    else:
        # Insert after CONTRIBUTORS:END block
        contrib_end = "<!-- CONTRIBUTORS:END -->"
        if contrib_end not in text:
            raise RuntimeError("Could not find <!-- CONTRIBUTORS:END --> in README.md")
        addition = f"\n\n## 🤝 Collaborators\n\n{block}"
        updated = text.replace(contrib_end, f"{contrib_end}{addition}", 1)

    README_PATH.write_text(updated, encoding="utf-8")


def main() -> None:
    OUT_SVG.parent.mkdir(parents=True, exist_ok=True)
    members = gather_members()
    OUT_SVG.write_text(
        render_grid_svg(members, f"Frontend Library collaborators and invited members ({len(members)})"),
        encoding="utf-8",
    )
    update_readme()
    print(f"updated collaborators: {len(members)} total")


if __name__ == "__main__":
    main()
