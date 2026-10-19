#!/usr/bin/env python3
"""Render a rolling year of GitHub's public contribution calendar as an SVG.

Only the Python standard library is needed. No token or authenticated API is used.
GitHub currently returns whole calendar years, even for a cross-year query.
"""

from __future__ import annotations

import argparse
import calendar
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from html import escape
from html.parser import HTMLParser
import json
import math
import os
from pathlib import Path
import re
import sys
import tempfile
from urllib.error import URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen
from xml.etree import ElementTree
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


DEFAULT_USER = "Xinze-Li-Moqian"
DEFAULT_TIMEZONE = "America/Toronto"
DEFAULT_OUTPUT = Path(__file__).resolve().parents[1] / "assets/contributions.svg"
USERNAME = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?\Z")
NUMBER = r"(?:0|[1-9]\d*|[1-9]\d{0,2}(?:,\d{3})+)"
MONTHS = {name: number for number, name in enumerate(calendar.month_name) if name}
TOOLTIP = re.compile(
    rf"(No|{NUMBER}) contributions? on ({'|'.join(MONTHS)}) "
    r"([1-9]|[12]\d|3[01])(?:st|nd|rd|th)?(?:,? (\d{4}))?\.?\Z"
)


class CalendarError(ValueError):
    """The response cannot safely be treated as a complete contribution year."""


@dataclass(frozen=True)
class Day:
    day: date
    count: int


class ContributionParser(HTMLParser):
    """Associate dated calendar cells with their English accessible tooltips."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.cells: dict[str, tuple[date, int]] = {}
        self.tooltips: dict[str, str] = {}
        self.graph_ranges: list[tuple[str, str]] = []
        self.heading = ""
        self._tooltip_id: str | None = None
        self._tooltip_parts: list[str] = []
        self._in_heading = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        classes = (attributes.get("class") or "").split()
        if "js-calendar-graph" in classes:
            self.graph_ranges.append((attributes.get("data-from") or "", attributes.get("data-to") or ""))
        if "ContributionCalendar-day" in classes and attributes.get("data-date"):
            try:
                cell_id = attributes["id"]
                day = date.fromisoformat(attributes["data-date"] or "")
                level = int(attributes["data-level"] or "")
            except (KeyError, TypeError, ValueError) as exc:
                raise CalendarError("Invalid dated contribution cell") from exc
            if not cell_id or cell_id in self.cells or level not in range(5):
                raise CalendarError("Duplicate cell ID or invalid contribution level")
            self.cells[cell_id] = (day, level)
        if tag == "tool-tip" and attributes.get("for"):
            if self._tooltip_id is not None:
                raise CalendarError("Nested contribution tooltip")
            self._tooltip_id = attributes["for"]
            self._tooltip_parts = []
        if tag == "h2" and attributes.get("id") == "js-contribution-activity-description":
            self._in_heading = True

    def handle_data(self, data: str) -> None:
        if self._tooltip_id is not None:
            self._tooltip_parts.append(data)
        if self._in_heading:
            self.heading += data

    def handle_endtag(self, tag: str) -> None:
        if tag == "tool-tip" and self._tooltip_id is not None:
            if self._tooltip_id in self.tooltips:
                raise CalendarError("Duplicate contribution tooltip")
            self.tooltips[self._tooltip_id] = " ".join("".join(self._tooltip_parts).split())
            self._tooltip_id = None
        if tag == "h2":
            self._in_heading = False


def dates_between(start: date, end: date) -> list[date]:
    return [start + timedelta(days=offset) for offset in range((end - start).days + 1)]


def parse_year(html: str, year: int) -> dict[date, Day]:
    """Reject partial years, duplicates, missing counts and inconsistent totals."""
    parser = ContributionParser()
    parser.feed(html)
    parser.close()
    expected_range = [(f"{year}-01-01 00:00:00 UTC", f"{year}-12-31 23:59:59 UTC")]
    if parser.graph_ranges != expected_range:
        raise CalendarError(f"GitHub did not return the requested calendar year {year}")
    if not parser.cells or parser._tooltip_id is not None:
        raise CalendarError("Empty or truncated contribution calendar")
    days: dict[date, Day] = {}
    for cell_id, (day, level) in parser.cells.items():
        if day in days:
            raise CalendarError(f"Duplicate date: {day}")
        match = TOOLTIP.fullmatch(parser.tooltips.get(cell_id, ""))
        if not match:
            raise CalendarError(f"Missing or unrecognized count for {day}")
        count_text, month, day_text, tooltip_year = match.groups()
        if (day.month, day.day) != (MONTHS[month], int(day_text)) or (tooltip_year and int(tooltip_year) != day.year):
            raise CalendarError(f"Tooltip date does not match its cell: {day}")
        count = 0 if count_text == "No" else int(count_text.replace(",", ""))
        if (count == 0) != (level == 0):
            raise CalendarError(f"Count and color level disagree for {day}")
        days[day] = Day(day, count)
    expected = set(dates_between(date(year, 1, 1), date(year, 12, 31)))
    if set(days) != expected:
        raise CalendarError(f"Incomplete calendar for {year}: expected {len(expected)} dates, found {len(days)}")
    heading = " ".join(parser.heading.split())
    total = re.fullmatch(rf"({NUMBER}) contributions? in {year}", heading)
    if not total or int(total[1].replace(",", "")) != sum(item.count for item in days.values()):
        raise CalendarError(f"Calendar total for {year} does not match its daily counts")
    return days


def calendar_url(username: str, year: int) -> str:
    if not USERNAME.fullmatch(username):
        raise ValueError("Invalid GitHub username")
    query = urlencode({"from": f"{year}-01-01", "to": f"{year}-12-31"})
    return f"https://github.com/users/{username}/contributions?{query}"


def fetch_year(username: str, year: int) -> dict[date, Day]:
    request = Request(calendar_url(username, year), headers={
        "User-Agent": "MoqianProfileContributions/1.0",
        "Accept": "text/html",
        "Accept-Language": "en-US,en;q=0.9",
    })
    with urlopen(request, timeout=30) as response:
        actual = urlparse(response.url)
        if actual.scheme != "https" or actual.netloc != "github.com" or actual.path != f"/users/{username}/contributions":
            raise CalendarError("Unexpected redirect from public contribution calendar")
        body = response.read(2_000_001)
        if len(body) > 2_000_000:
            raise CalendarError("Contribution calendar exceeds the response size limit")
        return parse_year(body.decode("utf-8"), year)


def rolling_year(username: str, end: date) -> list[Day]:
    start = end - timedelta(days=364)
    available: dict[date, Day] = {}
    for year in range(start.year, end.year + 1):
        available.update(fetch_year(username, year))
    wanted = dates_between(start, end)
    if any(day not in available for day in wanted):
        raise CalendarError("The rolling year has missing dates")
    return [available[day] for day in wanted]


def project(x: float, y: float, z: float = 0) -> tuple[float, float]:
    """Equal-scale isometric axes, rotated so weeks run horizontally."""
    return (145 + x - (y + z) / 2, 230 + math.sqrt(3) / 2 * (y - z))


def points(vertices: list[tuple[float, float, float]]) -> str:
    return " ".join(f"{px:.2f},{py:.2f}" for px, py in (project(*vertex) for vertex in vertices))


def render_svg(username: str, days: list[Day], timezone: str) -> str:
    if len(days) != 365 or [item.day for item in days] != dates_between(days[0].day, days[-1].day):
        raise CalendarError("SVG requires 365 unique consecutive days in date order")
    if any(type(item.count) is not int or item.count < 0 for item in days):
        raise CalendarError("Contributions must be nonnegative integer counts")
    start, end = days[0].day, days[-1].day
    total = sum(item.count for item in days)
    peak = max(item.count for item in days)
    week_start = start - timedelta(days=(start.weekday() + 1) % 7)
    cells = [((item.day - week_start).days // 7, (item.day.weekday() + 1) % 7, item) for item in days]
    user = escape(username, quote=True)
    metadata = {"schema_version": 1, "username": username, "start": str(start), "end": str(end),
                "window_timezone": timezone, "days": len(days), "total": total,
                "source": [calendar_url(username, year) for year in range(start.year, end.year + 1)],
                "height_scale": "square root of daily count"}
    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="420" viewBox="0 0 1200 420" role="img" aria-labelledby="title description">',
        f'<title id="title">{user}: {total:,} GitHub contributions, {start} to {end}</title>',
        '<desc id="description">A 365-day isometric contribution calendar. Each tile is one day; column height uses the square root of its contribution count. Broken-out daily counts are available in each tile title.</desc>',
        f'<metadata>{escape(json.dumps(metadata, ensure_ascii=False, sort_keys=True))}</metadata>',
        '<rect width="1200" height="420" rx="16" fill="#090E16"/>',
        '<rect x="0.5" y="0.5" width="1199" height="419" rx="15.5" fill="none" stroke="#1C2B3D"/>',
        '<g font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Arial,sans-serif">',
        '<text x="48" y="36" fill="#C8AA6E" font-size="10" letter-spacing="2.2">ACTIVITY / GITHUB</text>',
        '<text x="48" y="76" fill="#D9E9F6" font-size="30" font-weight="600">A year of contributions.</text>',
        f'<text x="48" y="105" fill="#8FA6BA" font-size="18">{start} — {end} · {user}</text>',
        f'<text x="1152" y="74" text-anchor="end" fill="#D4B674" font-size="44" font-weight="500">{total:,}</text>',
        '<text x="1152" y="105" text-anchor="end" fill="#8FA6BA" font-size="18">GitHub contributions</text>',
        '<path d="M48 125H1152" stroke="#253245"/>',
    ]
    # Paint the ground first, then columns from far to near along the viewing axis.
    for week, weekday, item in cells:
        x, y, size = week * 18, weekday * 18, 13
        svg.append(f'<polygon points="{points([(x,y,0),(x+size,y,0),(x+size,y+size,0),(x,y+size,0)])}" fill="#142131" stroke="#24374B" stroke-width="0.65"/>')
    for week, weekday, item in sorted(cells, key=lambda cell: (cell[0] + cell[1], cell[0])):
        x, y, size = week * 18, weekday * 18, 13
        height = 8 + 72 * math.sqrt(item.count / peak) if item.count else 0
        ratio = item.count / peak if peak else 0
        top, front, side = ("#D4B674", "#8A7042", "#AF915A") if ratio >= 0.35 else ("#B4D3EA", "#3C607D", "#6B91AF")
        svg.append(f'<g data-date="{item.day}" data-count="{item.count}"><title>{item.day}: {item.count:,} GitHub contributions</title>')
        if height:
            svg.append(f'<polygon points="{points([(x+size,y,0),(x+size,y+size,0),(x+size,y+size,height),(x+size,y,height)])}" fill="{side}"/>')
            svg.append(f'<polygon points="{points([(x,y+size,0),(x+size,y+size,0),(x+size,y+size,height),(x,y+size,height)])}" fill="{front}"/>')
            svg.append(f'<polygon points="{points([(x,y,height),(x+size,y,height),(x+size,y+size,height),(x,y+size,height)])}" fill="{top}" stroke="#D9E9F6" stroke-opacity="0.25" stroke-width="0.45"/>')
        else:
            svg.append(f'<polygon points="{points([(x,y,0),(x+size,y,0),(x+size,y+size,0),(x,y+size,0)])}" fill="#142131" stroke="#24374B" stroke-width="0.65"/>')
        svg.append('</g>')
    for weekday, label in [(0, "SUN"), (3, "WED"), (6, "SAT")]:
        px, py = project(-17, weekday * 18 + 7)
        svg.append(f'<text x="{px:.2f}" y="{py+3:.2f}" text-anchor="end" fill="#73899E" font-size="12" letter-spacing="1">{label}</text>')
    for week, _, item in cells:
        if item.day.day == 1:
            px, py = project(week * 18 + 6, 7.6 * 18)
            svg.append(f'<text x="{px:.2f}" y="{py:.2f}" fill="#8FA6BA" font-size="18">{calendar.month_abbr[item.day.month]}</text>')
    svg.extend([
        '<path d="M48 370H1152" stroke="#253245"/>',
        '<text x="48" y="398" fill="#8FA6BA" font-size="18">365 days · one tile per day · √count height scale</text>',
        '<rect x="928" y="385" width="13" height="13" rx="1" fill="#142131" stroke="#3C5268"/>',
        '<rect x="949" y="385" width="13" height="13" rx="1" fill="#B4D3EA"/>',
        '<rect x="970" y="385" width="13" height="13" rx="1" fill="#D4B674"/>',
        '<text x="996" y="398" fill="#8FA6BA" font-size="18">Less → more</text>',
        '</g></svg>\n',
    ])
    rendered = "\n".join(svg)
    ElementTree.fromstring(rendered)
    return rendered


def atomic_write(path: Path, content: str) -> bool:
    """Replace only a complete successful render, and avoid identical rewrites."""
    if path.is_symlink():
        raise ValueError("Refusing to replace a symbolic-link output")
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(content)
        temporary.chmod(0o644)
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--user", default=DEFAULT_USER, help="GitHub username (default: %(default)s)")
    parser.add_argument("--timezone", default=DEFAULT_TIMEZONE, help="IANA timezone used to choose today's date (default: %(default)s)")
    parser.add_argument("--end", type=date.fromisoformat, help="Last included date, YYYY-MM-DD; defaults to today in --timezone")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="SVG output path")
    args = parser.parse_args(argv)
    try:
        today = datetime.now(ZoneInfo(args.timezone)).date()
        end = args.end or today
        if end > today:
            raise ValueError("The contribution window cannot end in the future")
        if args.output.suffix.lower() != ".svg":
            raise ValueError("Output must have an .svg extension")
        days = rolling_year(args.user, end)
        changed = atomic_write(args.output, render_svg(args.user, days, args.timezone))
    except (ValueError, OSError, URLError, UnicodeError, ZoneInfoNotFoundError) as exc:
        print(f"Contribution render failed; previous image preserved: {exc}", file=sys.stderr)
        return 1
    print(f"{'Updated' if changed else 'Unchanged'} {args.output}: {sum(item.count for item in days):,} contributions, {days[0].day} to {end} ({len(days)} days)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
