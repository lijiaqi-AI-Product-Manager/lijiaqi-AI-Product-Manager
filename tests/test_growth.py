"""Protect public metrics against false zeroes and mixed download categories."""

from datetime import date
from contextlib import nullcontext
import importlib.util
import io
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

    def test_stars_store_only_aggregated_dates(self):
        rows = [{"starred_at": "2026-11-02T10:00:00Z", "user": {"login": "public-user"}},
                {"starred_at": "2026-11-01T10:00:00Z", "user": {"login": "another-user"}}]
        self.assertEqual(growth.star_points(rows), [{"date": "2026-11-01", "value": 1}, {"date": "2026-11-02", "value": 2}])


if __name__ == "__main__":
    unittest.main()
