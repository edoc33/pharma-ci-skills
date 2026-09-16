import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("vp_client", ROOT / "scripts/vp_client.py")
vp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vp)


class ClientTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.csv = Path(self.temp.name) / "watchlist.csv"

    def test_create_preview_has_required_public_schema_fields_without_network(self):
        with patch.object(vp, "request") as request, contextlib.redirect_stdout(io.StringIO()) as output:
            vp.create(123, "https://example.com/drug", "Drug page", "Price changes", delivery="all")
        request.assert_not_called()
        body = json.JSONDecoder().raw_decode(output.getvalue())[0]
        # Required fields from official JobCreateRequestJsonSchema.json, checked 2026-09-16.
        self.assertTrue({"active", "interval", "target_device", "trigger", "url", "wait_time"} <= body.keys())
        self.assertEqual(body["target_device"], "4")
        self.assertEqual(body["notification"]["config"], {})
        self.assertFalse(body["notification"]["onlyImportantAlerts"])

    def test_confirmed_create_skips_existing_url(self):
        with patch.object(vp, "list_jobs", return_value=[{"url": "https://example.com/drug"}]), \
                patch.object(vp, "request") as request, contextlib.redirect_stdout(io.StringIO()):
            vp.create(123, " https://example.com/drug ", "Drug page", "Price changes", confirm=True, delivery="all")
        request.assert_not_called()

    def test_bulk_deduplicates_csv_and_existing_urls_and_counts_only_creates(self):
        self.csv.write_text("url,title,rule,interval\nhttps://example.com/a,A,Price,1440\n"
                            "https://example.com/b,B,Status,720\nhttps://example.com/b,B again,Status,720\n")
        with patch.object(vp, "list_jobs", return_value=[{"url": "https://example.com/a"}]), \
                patch.object(vp, "request", return_value={"jobid": "234"}) as request, \
                patch.object(vp.time, "sleep"), contextlib.redirect_stdout(io.StringIO()) as output:
            vp.bulk(123, self.csv, confirm=True, delivery="all")
        self.assertEqual(request.call_count, 1)
        self.assertEqual(request.call_args.args[2]["url"], "https://example.com/b")
        self.assertIn("1 CREATE rows; roughly 60 checks", output.getvalue())
        self.assertIn("jobid=234", output.getvalue())

    def test_bad_later_row_stops_before_any_api_call(self):
        for bad_row in ("https://example.com/b,B,,1440", "https://example.com/b,B,Rule,0",
                        "not-a-url,B,Rule,1440", "https://example.com/b,B,Rule,-1"):
            with self.subTest(row=bad_row):
                self.csv.write_text("url,title,rule,interval\nhttps://example.com/a,A,Rule,1440\n" + bad_row + "\n")
                with patch.object(vp, "request") as request, patch.object(vp, "list_jobs") as jobs:
                    with self.assertRaises(SystemExit):
                        vp.bulk(123, self.csv, confirm=True, delivery="all")
                request.assert_not_called()
                jobs.assert_not_called()

    def test_bulk_preview_accepts_bom_and_calls_no_api(self):
        self.csv.write_text("\ufeffurl,title,rule\nhttps://example.com/a,A,Rule\n")
        with patch.object(vp, "request") as request, patch.object(vp, "list_jobs") as jobs, \
                contextlib.redirect_stdout(io.StringIO()):
            vp.bulk(123, self.csv)
        request.assert_not_called()
        jobs.assert_not_called()

    def test_whoami_uses_documented_email_address(self):
        with patch.object(vp, "whoami", return_value={"emailAddress": "user@example.com", "workspaces": []}), \
                patch.object(vp.sys, "argv", ["vp_client.py", "whoami"]), \
                contextlib.redirect_stdout(io.StringIO()) as output:
            vp.main()
        self.assertEqual(json.loads(output.getvalue())["user"], "user@example.com")

    def test_live_writes_require_explicit_delivery_before_api_access(self):
        self.csv.write_text("url,title,rule\nhttps://example.com/a,A,Rule\n")
        with patch.object(vp, "request") as request, patch.object(vp, "list_jobs") as jobs:
            with self.assertRaises(SystemExit):
                vp.create(123, "https://example.com/a", "A", "Rule", confirm=True)
            with self.assertRaises(SystemExit):
                vp.bulk(123, self.csv, confirm=True)
        request.assert_not_called()
        jobs.assert_not_called()

    def test_row_delivery_policy_overrides_common_policy(self):
        self.csv.write_text("url,title,rule,delivery_policy\nhttps://example.com/a,A,Rule,all\n"
                            "https://example.com/b,B,Rule,important\n")
        with patch.object(vp, "list_jobs", return_value=[]), patch.object(vp, "request", return_value={}) as request, \
                patch.object(vp.time, "sleep"), contextlib.redirect_stdout(io.StringIO()):
            vp.bulk(123, self.csv, confirm=True, delivery="important")
        policies = [call.args[2]["notification"]["onlyImportantAlerts"] for call in request.call_args_list]
        self.assertEqual(policies, [False, True])

    def test_feed_retains_minor_changes_unless_important_only_requested(self):
        response = {"items": [{"changeDetectionLevel": level} for level in
                               ("important", "regular", "minor-importance", "minor-threshold", "none", None)]}
        with patch.object(vp, "request", return_value=response):
            self.assertEqual([item["level"] for item in vp.feed(123)],
                             ["important", "regular", "minor-importance", "minor-threshold"])
            self.assertEqual([item["level"] for item in vp.feed(123, important_only=True)], ["important"])


if __name__ == "__main__":
    unittest.main()
