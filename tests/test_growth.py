"""Protect public metrics against false zeroes and mixed download categories."""

from datetime import date
from contextlib import nullcontext
import importlib.util
import io
import json
import sys
from tempfile import TemporaryDirectory
from pathlib import Path
import unittest
from unittest.mock import patch

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts/update_growth.py"
SPEC = importlib.util.spec_from_file_location("growth", MODULE_PATH)
growth = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(growth)


class GrowthDataTests(unittest.TestCase):
    def test_github_token_is_not_forwarded_to_package_services(self):
        with patch.dict(growth.os.environ, {"GH_TOKEN": "synthetic-test-token"}), \
                patch.object(growth, "urlopen", return_value=nullcontext(io.StringIO("{}"))) as request:
            growth.fetch_json("https://api.npmjs.org/downloads/point/last-month/demo")
        self.assertIsNone(request.call_args.args[0].get_header("Authorization"))

    def test_anonymous_public_read_ignores_ambient_credentials(self):
        with patch.dict(growth.os.environ, {"GH_TOKEN": "synthetic-test-token"}), \
                patch.object(growth, "ANONYMOUS", True), \
                patch.object(growth, "urlopen", return_value=nullcontext(io.StringIO("{}"))) as request:
            growth.fetch_json("https://api.github.com/repos/example/demo/stargazers")
        self.assertIsNone(request.call_args.args[0].get_header("Authorization"))

    def test_failed_refresh_keeps_last_known_counts_instead_of_zero(self):
        previous = {"status": "ok", "points": [{"date": "2026-11-01", "value": 41}], "last_success_at": "2026-11-02T00:00:00+00:00"}
        def unavailable():
            raise OSError("statistics service unavailable")
        result = growth.refresh(previous, unavailable, "2026-11-03T00:00:00+00:00")
        self.assertEqual(result["points"], previous["points"])
        self.assertEqual(result["status"], "stale")
        self.assertEqual(result["last_success_at"], previous["last_success_at"])
        self.assertEqual(previous["status"], "ok")

    def test_pypi_excludes_mirrors_and_does_not_fill_unreported_days(self):
        response = {"package": "demo", "data": [
            {"category": "with_mirrors", "date": "2026-11-01", "downloads": 900},
            {"category": "without_mirrors", "date": "2026-11-01", "downloads": 12},
            {"category": "without_mirrors", "date": "2026-11-03", "downloads": 18},
        ]}
        with patch.object(growth, "fetch_json", return_value=response):
            result = growth.collect_downloads({"registry": "pypi", "name": "demo"}, date(2026, 11, 4), 90)
        self.assertEqual(result["points"], [{"date": "2026-11-01", "value": 12}, {"date": "2026-11-03", "value": 18}])

    def test_new_npm_package_is_pending_not_zero_downloads(self):
        with patch.object(growth, "fetch_json", return_value={"time": {"created": "2026-11-03T10:00:00Z"}}) as request:
            result = growth.collect_downloads({"registry": "npm", "name": "demo"}, date(2026, 11, 3), 90)
        self.assertEqual(request.call_count, 1)
        self.assertEqual(result["status"], "pending")
        self.assertEqual(result["points"], [])
        svg = growth.render_chart({"name": "Demo", "package": {"registry": "npm"}}, result, "downloads", "light", True, date(2026, 11, 3))
        self.assertIn("Awaiting first daily statistics", svg)
        self.assertNotIn("<polyline", svg)

    def test_invalid_or_duplicate_daily_counts_are_rejected(self):
        for rows in ([{"day": "2026-11-01", "downloads": -1}],
                     [{"day": "2026-11-01", "downloads": True}],
                     [{"day": "2026-11-01", "downloads": 2}, {"day": "2026-11-01", "downloads": 3}]):
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                growth.normalize_daily(rows, date(2026, 10, 1), date(2026, 11, 2))

    def test_public_weekly_star_aggregates_are_sorted_and_cumulative(self):
        rows = [
            {"week": 1793491200, "total": 1, "days": [0, 0, 1, 0, 0, 0, 0]},
            {"week": 1792886400, "total": 2, "days": [0, 0, 1, 1, 0, 0, 0]},
        ]
        points = growth.star_points(rows, date(2026, 11, 3))
        self.assertEqual(points[0], {"date": "2026-10-25", "value": 0})
        self.assertEqual(points[-1], {"date": "2026-11-03", "value": 3})
        self.assertEqual(next(p["value"] for p in points if p["date"] == "2026-10-28"), 2)
        self.assertEqual(len(points), 10)
        self.assertNotIn("user", repr(points))

    def test_invalid_or_duplicate_star_aggregate_weeks_are_rejected(self):
        valid = {"week": 1793491200, "total": 1, "days": [0, 0, 1, 0, 0, 0, 0]}
        for rows in ([valid, valid], [{"week": 1793491200, "total": 1, "days": [0]}],
                     [{"week": 1793491200, "total": 4, "days": [0, 0, 1, 0, 0, 0, 0]}]):
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                growth.star_points(rows, date(2026, 11, 3))

    def test_star_collection_uses_public_history_and_count_endpoints(self):
        rows = [{"week": 1793491200, "total": 1, "days": [0, 0, 1, 0, 0, 0, 0]}]
        with patch.object(growth, "fetch_json", side_effect=[rows, {"count": 1}]) as request:
            result = growth.collect_stars("example", "demo", date(2026, 11, 3))
        urls = [call.args[0] for call in request.call_args_list]
        self.assertTrue(urls[0].endswith("/stargazers/history?per_page=30&page=1"))
        self.assertTrue(urls[1].endswith("/stargazers/count"))
        self.assertEqual(result["total"], 1)

    def test_same_day_unchanged_refresh_does_not_rewrite_timestamps(self):
        previous = {"status": "ok", "points": [{"date": "2026-11-03", "value": 4}],
                    "total": 4, "checked_at": "2026-11-04T01:17:00+00:00",
                    "last_success_at": "2026-11-04T01:17:00+00:00"}
        payload = {"status": "ok", "points": previous["points"], "total": 4}
        result = growth.refresh(previous, lambda: payload, "2026-11-04T02:17:00+00:00")
        self.assertEqual(result, previous)

    def test_pypi_is_read_once_daily_after_its_update_window(self):
        package = {"registry": "pypi", "name": "demo"}
        previous = {"checked_at": "2026-11-03T01:17:00+00:00"}
        self.assertFalse(growth.download_refresh_due(package, previous, "2026-11-04T00:17:00+00:00"))
        self.assertTrue(growth.download_refresh_due(package, previous, "2026-11-04T01:17:00+00:00"))
        previous["checked_at"] = "2026-11-04T01:17:00+00:00"
        self.assertFalse(growth.download_refresh_due(package, previous, "2026-11-04T02:17:00+00:00"))
        self.assertTrue(growth.download_refresh_due({"registry": "npm"}, previous, "2026-11-04T02:17:00+00:00"))

    def test_unchanged_hourly_check_preserves_the_committed_snapshot(self):
        series = {"status": "ok", "points": [{"date": "2026-11-04", "value": 4}], "total": 4,
                  "checked_at": "2026-11-04T01:17:00+00:00", "last_success_at": "2026-11-04T01:17:00+00:00"}
        original = {"projects": {"demo": {"stars": series}}, "generated_at": "2026-11-04T01:17:00+00:00"}
        config = {"owner": "example", "window_days": 90, "projects": [{"repo": "demo", "name": "Demo"}]}
        payload = {k: v for k, v in series.items() if k not in {"checked_at", "last_success_at"}}
        with patch.object(growth, "collect_stars", return_value=payload):
            result, failures = growth.update_data(config, original, date(2026, 11, 4), "2026-11-04T02:17:00+00:00")
        self.assertEqual(result, original)
        self.assertEqual(failures, 0)

    def test_npm_range_ends_at_the_latest_reported_day(self):
        responses = [
            {"time": {"created": "2026-11-01T10:00:00Z"}},
            {"package": "demo", "downloads": 8, "start": "2026-11-02", "end": "2026-11-02"},
            {"package": "demo", "downloads": [{"day": "2026-11-01", "downloads": 3},
                                              {"day": "2026-11-02", "downloads": 8}]},
        ]
        with patch.object(growth, "fetch_json", side_effect=responses) as request:
            result = growth.collect_downloads({"registry": "npm", "name": "demo"}, date(2026, 11, 4), 90)
        self.assertIn("/2026-11-01:2026-11-02/demo", request.call_args_list[-1].args[0])
        self.assertEqual(result["points"][-1], {"date": "2026-11-02", "value": 8})

    def test_refresh_publishes_new_data_and_all_image_variants_together(self):
        config = {"owner": "example", "window_days": 90, "projects": [{"repo": "demo", "name": "Demo"}]}
        with TemporaryDirectory(dir=Path(__file__).parent) as directory:
            root = Path(directory)
            config_path, data_path, assets = root / "config.json", root / "data.json", root / "assets"
            config_path.write_text(json.dumps(config), encoding="utf-8")
            payload = {"status": "ok", "points": [{"date": "2026-11-04", "value": 9}], "total": 9}
            with patch.object(growth, "CONFIG", config_path), patch.object(growth, "DATA", data_path), \
                    patch.object(growth, "ASSETS", assets), patch.object(growth, "collect_stars", return_value=payload), \
                    patch.object(sys, "argv", ["update_growth.py", "--today", "2026-11-04"]):
                self.assertEqual(growth.main(), 0)
            stored = json.loads(data_path.read_text(encoding="utf-8"))
            self.assertEqual(stored["projects"]["demo"]["stars"]["total"], 9)
            images = list(assets.rglob("*.svg"))
            self.assertEqual(len(images), 4)
            for path in images:
                self.assertIn("2026-11-04: 9", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
