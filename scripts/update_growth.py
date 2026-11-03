"""Publish public repository and package trends as portable, theme-aware SVGs."""

import argparse
from datetime import date, datetime, timedelta, timezone
from html import escape
import json
import math
import os
from pathlib import Path
import re
import textwrap
from urllib.error import HTTPError
from urllib.parse import quote, urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "data/growth-config.json"
DATA = ROOT / "data/growth.json"
ASSETS = ROOT / "assets/growth"
ANONYMOUS = False


def fetch_json(url, accept="application/json"):
    headers = {"Accept": accept, "User-Agent": "public-project-growth-charts"}
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token and not ANONYMOUS and urlsplit(url).hostname == "api.github.com":
        headers["Authorization"] = f"Bearer {token}"
    request = Request(url, headers=headers)
    with urlopen(request, timeout=20) as response:
        return json.load(response)


def valid_count(value):
    if type(value) is not int or value < 0:
        raise ValueError("Expected a non-negative integer count")
    return value


def normalize_daily(rows, start, end):
    values = {}
    for row in rows:
        day = date.fromisoformat(row["day"])
        value = valid_count(row["downloads"])
        if day < start or day > end:
            continue
        key = day.isoformat()
        if key in values:
            raise ValueError(f"Duplicate statistics date: {key}")
        values[key] = value
    return [{"date": day, "value": value} for day, value in sorted(values.items())]


def star_points(rows, today):
    daily = {}
    for row in rows:
        start = datetime.fromtimestamp(valid_count(row["week"]), timezone.utc).date()
        days = row["days"]
        if not isinstance(days, list) or len(days) != 7:
            raise ValueError("Expected seven daily counts in each GitHub aggregate week")
        counts = [valid_count(value) for value in days]
        if valid_count(row["total"]) != sum(counts):
            raise ValueError("GitHub weekly total does not match its daily counts")
        for offset, count in enumerate(counts):
            day = (start + timedelta(days=offset)).isoformat()
            if day in daily:
                raise ValueError(f"Duplicate GitHub aggregate date: {day}")
            daily[day] = count
    total = 0
    points = []
    for day, count in sorted(daily.items()):
        if day > today.isoformat():
            continue
        total += count
        points.append({"date": day, "value": total})
    return points


def collect_stars(owner, repo, today):
    rows = []
    base = f"https://api.github.com/repos/{quote(owner)}/{quote(repo)}/stargazers"
    source = f"{base}/history"
    for page in range(1, 101):
        batch = fetch_json(f"{source}?per_page=30&page={page}")
        if not isinstance(batch, list):
            raise ValueError("Unexpected GitHub aggregate history response")
        rows.extend(batch)
        if len(batch) < 30:
            break
    else:
        raise ValueError("History exceeds the pagination budget; retain the previous chart")
    total = valid_count(fetch_json(f"{base}/count")["count"])
    points = star_points(rows, today)
    if not points:
        if total:
            raise ValueError("GitHub history is empty while the current Star count is nonzero")
        points = [{"date": today.isoformat(), "value": 0}]
    return {"status": "ok", "source": source, "count_source": f"{base}/count",
            "points": points, "total": total}

def collect_downloads(package, today, window_days):
    start = today - timedelta(days=window_days)
    end = today - timedelta(days=1)
    name = package["name"]
    registry = package["registry"]
    if registry == "npm":
        metadata = fetch_json(f"https://registry.npmjs.org/{quote(name, safe='')}")
        created = date.fromisoformat(metadata["time"]["created"][:10])
        start = max(start, created)
        source = f"https://api.npmjs.org/downloads/range/{start}:{end}/{quote(name, safe='')}"
        if created > end:
            return {"status": "pending", "source": source, "points": [], "published": created.isoformat()}
        try:
            response = fetch_json(source)
        except HTTPError as error:
            if error.code == 404:
                return {"status": "pending", "source": source, "points": [], "published": created.isoformat()}
            raise
        if response.get("package") != name:
            raise ValueError("The npm response does not match the configured package")
        points = normalize_daily(response["downloads"], start, end)
    elif registry == "pypi":
        source = f"https://pypistats.org/api/packages/{quote(name, safe='')}/overall?mirrors=false"
        response = fetch_json(source)
        if response.get("package", "").lower() != name.lower():
            raise ValueError("The PyPI Stats response does not match the configured package")
        rows = [{"day": row["date"], "downloads": row["downloads"]}
                for row in response["data"] if row["category"] == "without_mirrors"]
        points = normalize_daily(rows, start, end)
    else:
        raise ValueError("Unsupported package registry")
    return {"status": "ok" if points else "pending", "source": source, "points": points}


def refresh(previous, producer, stamp):
    try:
        result = producer()
        result["checked_at"] = stamp
        result["last_success_at"] = stamp
        return result
    except Exception as error:
        result = dict(previous or {})
        result.update({"status": "stale" if result.get("points") else "unavailable",
                       "checked_at": stamp, "error": f"{type(error).__name__}: {error}"})
        return result


def nice_step(maximum):
    raw = max(maximum / 4, 1)
    power = 10 ** math.floor(math.log10(raw))
    return next(unit * power for unit in (1, 2, 5, 10) if unit * power >= raw)


def render_chart(project, series, kind, theme, mobile, today):
    width, height = (480, 400) if mobile else (960, 400)
    pad = 24 if mobile else 40
    left, right = (54, 456) if mobile else (68, 920)
    top, bottom = (104, 300) if mobile else (110, 315)
    colors = ({"bg": "#f7f9f8", "fg": "#18322f", "muted": "#536963", "grid": "#dce6e2",
               "star": "#1b806b", "download": "#326fb3"} if theme == "light" else
              {"bg": "#101b1c", "fg": "#e5f0eb", "muted": "#a3b9b1", "grid": "#2c4541",
               "star": "#7bd4b8", "download": "#8fc2ff"})
    status = series.get("status", "unavailable")
    points = [dict(point) for point in series.get("points", [])]
    if kind == "stars" and points:
        through = series.get("last_success_at", today.isoformat())[:10]
        if points[-1]["date"] < through:
            points.append({"date": through, "value": points[-1]["value"]})
    package = project.get("package", {})
    registry_label = "npm" if package.get("registry") == "npm" else "PyPI"
    subtitle = "GitHub star history" if kind == "stars" else f"{registry_label} daily download requests"
    total = series.get("total", points[-1]["value"] if points else None) if kind == "stars" else (sum(p["value"] for p in points) if points else None)
    value = f"{total:,}" if total is not None else "—"
    value_label = "current stars" if kind == "stars" else "requests in shown period"
    title = f"{project['name']} — {subtitle}"
    description = ("Cumulative counts from GitHub public daily aggregates. API day boundaries may differ from UTC." if kind == "stars" else
                   "Daily package download requests from reported dates. Repeated or automated requests may be included; these are not unique users.")
    checked = series.get("last_success_at" if status == "stale" else "checked_at", today.isoformat())[:10]
    update = f"Last success {checked} UTC · update unavailable" if status == "stale" else f"Updated {checked} UTC"
    source_note = ("GitHub REST · public daily aggregates; API day boundaries." if kind == "stars" else
                   ("npm download-counts · requests, not unique users." if package.get("registry") == "npm" else
                    "PyPI Stats · known mirrors excluded; requests, not unique users."))
    if status == "unavailable":
        update = f"Checked {series.get('checked_at', today.isoformat())[:10]} UTC · data unavailable"
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title description">',
           f'<title id="title">{escape(title)}</title><desc id="description">{escape(description)} {escape(update)}</desc>',
           f'<rect width="{width}" height="{height}" rx="18" fill="{colors["bg"]}"/>',
           '<g font-family="Segoe UI,Arial,sans-serif">',
           f'<text x="{pad}" y="{38 if mobile else 44}" font-size="{20 if mobile else 24}" font-weight="600" fill="{colors["fg"]}">{escape(project["name"])}</text>',
           f'<text x="{pad}" y="{61 if mobile else 72}" font-size="{12 if mobile else 14}" fill="{colors["muted"]}">{escape(subtitle)}</text>',
           f'<text x="{right}" y="{38 if mobile else 45}" text-anchor="end" font-size="{24 if mobile else 30}" font-weight="600" fill="{colors["fg"]}">{value}</text>',
           f'<text x="{right}" y="{61 if mobile else 72}" text-anchor="end" font-size="{10 if mobile else 12}" fill="{colors["muted"]}">{value_label}</text>']
    if points:
        ordinals = [date.fromisoformat(p["date"]).toordinal() for p in points]
        first, last = min(ordinals), max(ordinals)
        step = nice_step(max(p["value"] for p in points))
        ymax = max(step, math.ceil(max(p["value"] for p in points) / step) * step)
        xpos = lambda day: (left + right) / 2 if first == last else left + (day - first) / (last - first) * (right - left)
        ypos = lambda count: bottom - count / ymax * (bottom - top)
        for tick in range(0, int(ymax) + 1, int(step)):
            y = ypos(tick)
            out.append(f'<path d="M {left} {y:.2f} H {right}" stroke="{colors["grid"]}" stroke-width="1"/>')
            out.append(f'<text x="{left-10}" y="{y+4:.2f}" text-anchor="end" font-size="12" fill="{colors["muted"]}">{tick:,}</text>')
        ticks = sorted({first, last, (first + last) // 2})
        for day in ticks:
            anchor = "middle" if first == last or first < day < last else ("start" if day == first else "end")
            out.append(f'<text x="{xpos(day):.2f}" y="{bottom+23}" text-anchor="{anchor}" font-size="12" fill="{colors["muted"]}">{date.fromordinal(day).isoformat()}</text>')
        segments, segment = [], []
        previous = None
        for point, day in zip(points, ordinals):
            if kind == "downloads" and previous is not None and day - previous > 1:
                segments.append(segment)
                segment = []
            segment.append(f'{xpos(day):.2f},{ypos(point["value"]):.2f}')
            previous = day
        segments.append(segment)
        color = colors["star" if kind == "stars" else "download"]
        for segment in segments:
            if len(segment) > 1:
                out.append(f'<polyline points="{" ".join(segment)}" fill="none" stroke="{color}" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>')
        for point, day in zip(points, ordinals):
            out.append(f'<circle cx="{xpos(day):.2f}" cy="{ypos(point["value"]):.2f}" r="3.2" fill="{color}"><title>{point["date"]}: {point["value"]:,}</title></circle>')
    else:
        message = "Awaiting first daily statistics" if status == "pending" else "Statistics temporarily unavailable"
        out.append(f'<text x="{width/2}" y="200" text-anchor="middle" font-size="16" fill="{colors["fg"]}">{message}</text>')
        if series.get("published"):
            out.append(f'<text x="{width/2}" y="226" text-anchor="middle" font-size="13" fill="{colors["muted"]}">Package published {series["published"]}</text>')
    out.append(f'<text x="{pad}" y="{349 if mobile else 365}" font-size="{11 if mobile else 12}" fill="{colors["muted"]}">{escape(update)}</text>')
    for number, line in enumerate(textwrap.wrap(source_note, width=67 if mobile else 140)):
        out.append(f'<text x="{pad}" y="{370+14*number if mobile else 386+14*number}" font-size="11" fill="{colors["muted"]}">{escape(line)}</text>')
    out.append("</g></svg>\n")
    return "".join(out)


def write_assets(config, data, today):
    for project in config["projects"]:
        directory = ASSETS / project["repo"]
        directory.mkdir(parents=True, exist_ok=True)
        saved = data.get("projects", {}).get(project["repo"], {})
        for kind in ["stars"] + (["downloads"] if project.get("package") else []):
            for mobile in (False, True):
                for theme in ("light", "dark"):
                    suffix = f"-mobile-{theme}" if mobile else f"-{theme}"
                    image = render_chart(project, saved.get(kind, {}), kind, theme, mobile, today)
                    (directory / f"{kind}{suffix}.svg").write_text(image, encoding="utf-8")


def main():
    global ANONYMOUS
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--render-only", action="store_true", help="Rebuild SVGs from committed public data without network access")
    parser.add_argument("--today", type=date.fromisoformat, default=datetime.now(timezone.utc).date())
    parser.add_argument("--anonymous", action="store_true", help="Read public GitHub data without using ambient credentials")
    args = parser.parse_args()
    ANONYMOUS = args.anonymous
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    for project in config["projects"]:
        if not re.fullmatch(r"[A-Za-z0-9_.-]+", project["repo"]):
            raise ValueError("Unsafe repository identifier")
    data = json.loads(DATA.read_text(encoding="utf-8")) if DATA.exists() else {"projects": {}}
    failures = 0
    if not args.render_only:
        stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
        for project in config["projects"]:
            repo = project["repo"]
            previous = data["projects"].get(repo, {})
            saved = {"stars": refresh(previous.get("stars"), lambda: collect_stars(config["owner"], repo, args.today), stamp)}
            if project.get("package"):
                saved["downloads"] = refresh(previous.get("downloads"), lambda: collect_downloads(project["package"], args.today, config["window_days"]), stamp)
            data["projects"][repo] = saved
            for kind, series in saved.items():
                if series["status"] in {"stale", "unavailable"}:
                    failures += 1
                    print(f"::warning::{repo}/{kind}: {series['status']}; previous values retained when available")
                else:
                    print(f"{repo}/{kind}: {series['status']} ({len(series.get('points', []))} reported dates)")
        data["generated_at"] = stamp
        DATA.parent.mkdir(parents=True, exist_ok=True)
        DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_assets(config, data, args.today)
    return 1 if failures == sum(1 + bool(p.get("package")) for p in config["projects"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
