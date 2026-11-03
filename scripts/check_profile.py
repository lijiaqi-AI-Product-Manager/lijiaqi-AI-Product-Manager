"""Check README portability and internal documentation links without network access."""

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
errors = []
links = 0
images = 0


def fail(file, message):
    errors.append(f"{file.relative_to(ROOT)}: {message}")


def anchors(file):
    source = file.read_text(encoding="utf-8")
    found = set(re.findall(r'<a\s+id="([^"]+)"', source))
    counts = {}
    for title in re.findall(r"^#{1,6}\s+(.+)$", source, re.M):
        slug = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
        count = counts.get(slug, 0)
        counts[slug] = count + 1
        found.add(slug if count == 0 else f"{slug}-{count}")
    return found


for file in sorted(ROOT.rglob("*.md")):
    source = file.read_text(encoding="utf-8")
    destinations = re.findall(r'\[[^\]\n]*\]\(([^\s)]+)\)', source)
    destinations += re.findall(r'(?:href|src|srcset)="([^"]+)"', source)
    for dest in destinations:
        links += 1
        parsed = urlsplit(dest.strip("<>"))
        if parsed.scheme or dest.startswith("//"):
            continue
        target = (file.parent / unquote(parsed.path)).resolve() if parsed.path else file
        if not target.is_relative_to(ROOT):
            fail(file, f"link leaves repository: {dest}")
        elif not target.is_file():
            fail(file, f"missing local target: {dest}")
        elif parsed.fragment and target.suffix == ".md" and unquote(parsed.fragment) not in anchors(target):
            fail(file, f"missing anchor: {dest}")
    for img in re.findall(r"<img\b[^>]*>", source):
        images += 1
        alt = re.search(r'alt="([^"]+)"', img)
        if not alt or not alt[1].strip():
            fail(file, "image is missing meaningful alt text")
    if re.search(r"<script\b|<iframe\b|<style\b", source, re.I):
        fail(file, "README/document contains unsupported active HTML")
    if file.name in {"README.md", "README.en.md"} and file.parent == ROOT:
        visible = re.sub(r"https?://[^\s\"<>)]*", "", source)
        if re.search(r"\bv?\d+\.\d+\.\d+(?:[-+][\w.-]+)?\b", visible):
            fail(file, "project version appears in profile copy")

svgs = list((ROOT / "assets").glob("*.svg"))
for file in svgs:
    try:
        doc = ET.parse(file).getroot()
        ns = {"s": "http://www.w3.org/2000/svg"}
        if not doc.findtext("s:title", namespaces=ns) or not doc.findtext("s:desc", namespaces=ns):
            fail(file, "SVG needs a title and description")
        if not doc.get("viewBox"):
            fail(file, "SVG needs a viewBox")
        for node in doc.iter():
            if node.tag.rsplit("}", 1)[-1] in {"script", "foreignObject", "image"}:
                fail(file, "SVG must stay self-contained and portable")
    except ET.ParseError as exc:
        fail(file, str(exc))

for slug in ["hero", "hero-mobile", "job-radar", "qgauss", "agent-compare", "bug-gps", "skill-healthcheck", "unremember", "process", "process-mobile", "footer"]:
    for theme in ["light", "dark"]:
        if not (ROOT / "assets" / f"{slug}-{theme}.svg").is_file():
            errors.append(f"missing themed artwork: {slug}-{theme}")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"Profile checks passed: {links} links, {images} HTML images, {len(svgs)} SVG assets")
