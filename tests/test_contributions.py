"""Focused, offline tests for public calendar parsing and faithful SVG rendering."""

from datetime import date, timedelta
import importlib.util
import math
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from xml.etree import ElementTree


SOURCE = Path(__file__).resolve().parents[1] / "scripts/render_contributions.py"
SPEC = importlib.util.spec_from_file_location("render_contributions", SOURCE)
renderer = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = renderer
SPEC.loader.exec_module(renderer)


def calendar_html(year=2026, counts=None):
    counts = counts or {date(year, 1, 1): 1, date(year, 1, 2): 1234}
    dates = renderer.dates_between(date(year, 1, 1), date(year, 12, 31))
    parts = [f'<h2 id="js-contribution-activity-description">{sum(counts.values()):,} contributions in {year}</h2>',
             f'<div class="js-calendar-graph" data-from="{year}-01-01 00:00:00 UTC" data-to="{year}-12-31 23:59:59 UTC">']
    # Like GitHub's table, deliberately not in chronological order.
    for day in sorted(dates, key=lambda value: (value.weekday(), value)):
        count = counts.get(day, 0)
        text = f'{count:,} contribution' + ("s" if count != 1 else "") if count else "No contributions"
        parts.append(f'<td class="ContributionCalendar-day" data-date="{day}" id="day-{day}" data-level="{1 if count else 0}"></td>')
        parts.append(f'<tool-tip for="day-{day}">{text} on {day.strftime("%B")} {day.day}th.</tool-tip>')
    return "\n".join(parts) + "</div>"


class CalendarTests(unittest.TestCase):
    def test_counts_are_tooltip_values_not_color_levels(self):
        days = renderer.parse_year(calendar_html(), 2026)
        self.assertEqual(len(days), 365)
        self.assertEqual(days[date(2026, 1, 2)].count, 1234)
        self.assertEqual(days[date(2026, 1, 3)].count, 0)

    def test_leap_year_has_all_366_dates(self):
        days = renderer.parse_year(calendar_html(2024), 2024)
        self.assertEqual(len(days), 366)
        self.assertIn(date(2024, 2, 29), days)

    def test_missing_day_or_tooltip_rejected(self):
        html = calendar_html()
        for malformed in [html.replace('data-date="2026-01-02"', ''),
                          html.replace('for="day-2026-01-02"', 'for="missing"')]:
            with self.subTest(malformed=malformed[:80]), self.assertRaises(renderer.CalendarError):
                renderer.parse_year(malformed, 2026)

    def test_wrong_year_empty_unknown_text_and_total_rejected(self):
        html = calendar_html()
        for malformed in ["", html.replace('2026-12-31 23:59:59 UTC', '2025-12-31 23:59:59 UTC'),
                          html.replace('1,234 contributions on', 'Many contributions on'),
                          html.replace('1,235 contributions in', '1,236 contributions in'),
                          html.replace('January 2th.', 'January 3rd.')]:
            with self.subTest(malformed=malformed[:80]), self.assertRaises(renderer.CalendarError):
                renderer.parse_year(malformed, 2026)

    def test_duplicate_date_id_or_tooltip_rejected(self):
        html = calendar_html()
        for malformed in [html.replace('data-date="2026-01-03"', 'data-date="2026-01-02"'),
                          html.replace('id="day-2026-01-03"', 'id="day-2026-01-02"'),
                          html + '<tool-tip for="day-2026-01-02">1 contribution on January 2nd.</tool-tip>']:
            with self.subTest(malformed=malformed[-80:]), self.assertRaises(renderer.CalendarError):
                renderer.parse_year(malformed, 2026)

    def test_color_level_and_count_disagreement_rejected(self):
        html = calendar_html().replace('id="day-2026-01-02" data-level="1"', 'id="day-2026-01-02" data-level="0"')
        with self.assertRaises(renderer.CalendarError):
            renderer.parse_year(html, 2026)

    def test_rolling_window_fetches_both_years_then_trims(self):
        def fetch(user, year):
            return renderer.parse_year(calendar_html(year, {date(year, 1, 1): 50, date(year, 12, 31): 2}), year)
        with patch.object(renderer, 'fetch_year', side_effect=fetch) as mocked:
            days = renderer.rolling_year('example', date(2026, 10, 19))
        self.assertEqual([call.args[1] for call in mocked.call_args_list], [2025, 2026])
        self.assertEqual((days[0].day, days[-1].day), (date(2025, 10, 20), date(2026, 10, 19)))
        self.assertEqual(len(days), 365)
        self.assertEqual(sum(day.count for day in days), 52)

    def test_invalid_username_rejected(self):
        with self.assertRaises(ValueError):
            renderer.calendar_url('../private', 2026)


class RenderingTests(unittest.TestCase):
    def setUp(self):
        self.days = [renderer.Day(date(2025, 10, 20) + timedelta(days=i), 100 if i == 364 else i % 4) for i in range(365)]

    def test_projection_has_equal_axes_at_120_degrees(self):
        origin = renderer.project(0, 0, 0)
        vectors = [tuple(v - o for v, o in zip(renderer.project(*axis), origin)) for axis in [(1, 0, 0), (0, 1, 0), (0, 0, 1)]]
        for vector in vectors:
            self.assertAlmostEqual(math.hypot(*vector), 1)
        for left, right in [(vectors[0], vectors[1]), (vectors[1], vectors[2]), (vectors[0], vectors[2])]:
            self.assertAlmostEqual(sum(a * b for a, b in zip(left, right)), -0.5)

    def test_svg_exact_dates_counts_and_bounded_geometry(self):
        svg = renderer.render_svg('example', self.days, 'America/Toronto')
        root = ElementTree.fromstring(svg)
        cells = root.findall('.//{*}g[@data-date]')
        self.assertEqual({cell.attrib['data-date']: int(cell.attrib['data-count']) for cell in cells}, {str(day.day): day.count for day in self.days})
        self.assertEqual(len(cells), 365)
        for polygon in root.findall('.//{*}polygon'):
            for pair in polygon.attrib['points'].split():
                x, y = map(float, pair.split(','))
                self.assertTrue(32 <= x <= 1168 and 135 <= y <= 360, (x, y))
        self.assertIn(f'{sum(day.count for day in self.days):,} GitHub contributions', svg)

    def test_zero_counts_valid_and_bad_data_rejected(self):
        zero_days = [renderer.Day(day.day, 0) for day in self.days]
        ElementTree.fromstring(renderer.render_svg('example', zero_days, 'America/Toronto'))
        for days in [[], self.days[:-1], list(reversed(self.days)), [renderer.Day(self.days[0].day, -1)] + self.days[1:]]:
            with self.assertRaises(renderer.CalendarError):
                renderer.render_svg('example', days, 'America/Toronto')

    def test_metadata_is_xml_escaped(self):
        svg = renderer.render_svg('example', self.days, 'A&B<test>')
        root = ElementTree.fromstring(svg)
        self.assertIn('A&B<test>', root.find('{*}metadata').text)
        self.assertEqual(root.findall('.//test'), [])

    def test_atomic_write_is_stable_and_fetch_failure_preserves_previous(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'contributions.svg'
            self.assertTrue(renderer.atomic_write(path, '<svg>previous</svg>'))
            self.assertFalse(renderer.atomic_write(path, '<svg>previous</svg>'))
            with patch.object(renderer, 'rolling_year', side_effect=renderer.CalendarError('incomplete calendar')):
                with patch('sys.stderr'):
                    self.assertEqual(renderer.main(['--output', str(path)]), 1)
            self.assertEqual(path.read_text(), '<svg>previous</svg>')


if __name__ == '__main__':
    unittest.main()
