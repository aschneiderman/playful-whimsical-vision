#!/usr/bin/env python3
"""
generate_gallery.py

Recursively walks the repo, and writes an index.html into every folder
(including the root) showing:
  - a breadcrumb trail back to the root
  - chips linking down into any subfolders
  - a grid of every image in that folder, with the filename shown below it

Usage:
    python3 generate_gallery.py

Run it from anywhere inside the repo, or pass a path:
    python3 generate_gallery.py /path/to/repo

Requires: template.html at the repo root, with {{TITLE}} and {{CONTENT}}
placeholders.
"""

import sys
from pathlib import Path
from html import escape

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp"}
SKIP_DIRS = {".git", "node_modules", ".github", "assets"}
TEMPLATE_NAME = "template.html"
INDEX_NAME = "index.html"
ASSETS_DIR = "assets"
HERO_CANDIDATES = ["hero.jpg", "hero.jpeg", "hero.png", "hero.svg", "hero.webp"]


def find_hero(root: Path):
    """Look for assets/hero.* at the repo root. Returns the relative path (as a
    string, e.g. 'assets/hero.jpg') or None if no hero image is present."""
    assets_dir = root / ASSETS_DIR
    if not assets_dir.is_dir():
        return None
    for candidate in HERO_CANDIDATES:
        if (assets_dir / candidate).exists():
            return f"{ASSETS_DIR}/{candidate}"
    return None


def format_name(name: str) -> str:
    """my-folder-name -> My Folder Name"""
    return " ".join(word.capitalize() for word in name.replace("_", "-").split("-"))


def find_root(start: Path) -> Path:
    """Walk upward from `start` until we find the folder containing template.html."""
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / TEMPLATE_NAME).exists():
            return candidate
    sys.exit(f"Couldn't find {TEMPLATE_NAME} in {start} or any parent directory.")


def list_subdirs(folder: Path):
    return sorted(
        [d for d in folder.iterdir() if d.is_dir() and d.name not in SKIP_DIRS and not d.name.startswith(".")],
        key=lambda d: d.name.lower(),
    )


def list_images(folder: Path):
    return sorted(
        [f for f in folder.iterdir() if f.is_file() and f.suffix.lower() in IMAGE_EXTS],
        key=lambda f: f.name.lower(),
    )


def build_breadcrumb(folder: Path, root: Path) -> str:
    rel = folder.relative_to(root)
    parts = rel.parts  # empty tuple if folder == root

    crumbs = []
    # Root crumb
    depth = len(parts)
    root_link = "/".join([".."] * depth + [INDEX_NAME]) if depth else INDEX_NAME
    crumbs.append(f'<a href="{root_link}">{escape(format_name(root.name))}</a>')

    for i, part in enumerate(parts):
        remaining = len(parts) - i - 1
        if remaining == 0:
            crumbs.append(escape(format_name(part)))
        else:
            link = "/".join([".."] * remaining + [INDEX_NAME])
            crumbs.append(f'<a href="{link}">{escape(format_name(part))}</a>')

    return '<div class="breadcrumb">' + " / ".join(crumbs) + "</div>"


def build_content(folder: Path, root: Path, hero: str = None) -> str:
    subdirs = list_subdirs(folder)
    images = list_images(folder)
    title = format_name(folder.name) if folder != root else format_name(root.name)

    parts = [f"<h1>{escape(title)}</h1>"]

    if folder == root and hero:
        parts.append(f'<div class="hero"><img src="{escape(hero)}" alt=""></div>')

    parts.append(build_breadcrumb(folder, root))

    if subdirs:
        chips = "\n".join(
            f'<a class="folder-chip" href="{d.name}/{INDEX_NAME}">{escape(format_name(d.name))}</a>'
            for d in subdirs
        )
        parts.append(f'<div class="folders">\n{chips}\n</div>')

    if images:
        cards = "\n".join(
            f'<figure>\n'
            f'  <a class="thumb-wrap" href="{escape(img.name)}" target="_blank" rel="noopener">'
            f'<img src="{escape(img.name)}" alt="{escape(img.name)}" loading="lazy"></a>\n'
            f'  <figcaption>{escape(img.name)}</figcaption>\n'
            f'</figure>'
            for img in images
        )
        parts.append(f'<div class="grid">\n{cards}\n</div>')
    elif not subdirs:
        parts.append('<p class="empty">Nothing here yet.</p>')

    return "\n".join(parts)


def generate(root: Path):
    template_text = (root / TEMPLATE_NAME).read_text(encoding="utf-8")
    hero = find_hero(root)
    count = 0

    for folder in [root, *[p for p in root.rglob("*") if p.is_dir()]]:
        if any(part in SKIP_DIRS or part.startswith(".") for part in folder.relative_to(root).parts):
            continue

        title = format_name(folder.name) if folder != root else format_name(root.name)
        content = build_content(folder, root, hero)
        html = template_text.replace("{{TITLE}}", escape(title)).replace("{{CONTENT}}", content)

        (folder / INDEX_NAME).write_text(html, encoding="utf-8")
        count += 1

    print(f"Wrote {count} index.html file(s), rooted at {root}")


if __name__ == "__main__":
    start = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    root = find_root(start)
    generate(root)
