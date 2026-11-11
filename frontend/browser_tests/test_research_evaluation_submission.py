"""Browser contract checks with a mocked API; all data is synthetic."""
import json
import unittest
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / "frontend/pages/research-evaluation.html"
TOKEN = "synthetic-invitation-token-" + ("z" * 40)


class ResearchEvaluationSubmissionTests(unittest.TestCase):
    def setUp(self):
        self.p = sync_playwright().start()
        self.browser = self.p.chromium.launch(channel="chrome", headless=True)
        self.page = self.browser.new_page(viewport={"width": 390, "height": 844})
        self.posts = []
        self.errors = []
        self.page.on("pageerror", lambda error: self.errors.append(str(error)))
        self.page.route("http://127.0.0.1:8000/research/responses", self.handle_api)

    def tearDown(self):
        self.browser.close()
        self.p.stop()

    def handle_api(self, route):
        request = route.request
        cors = {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "content-type"}
        if request.method == "OPTIONS":
            route.fulfill(status=204, headers=cors)
            return
        payload = request.post_data_json
        self.posts.append(payload)
        if len(self.posts) == 1 and getattr(self, "fail_first", False):
            route.abort()
            return
        route.fulfill(status=201, headers={**cors, "Content-Type": "application/json"},
                      body=json.dumps({"status": "received", "duplicate_retry": False}))

    def open_invitation(self):
        self.page.goto(PAGE.as_uri() + "#invite=" + TOKEN)
        self.page.get_by_text("Research invitation active").wait_for()
        self.assertNotIn("invite=", self.page.url)

    def complete_form(self):
        self.page.locator("#age-yes").check()
        self.page.get_by_role("button", name="Continue →").click()
        self.page.locator("#device-1").check()
        self.page.locator("#tasks-0").check()
        self.page.locator("#route-0").check()
        self.page.get_by_role("button", name="Continue →").click()
        self.page.locator("#Q5-rating-3").check()
        self.page.locator("#Q6-rating-4").check()
        self.page.get_by_role("button", name="Continue →").click()
        self.page.get_by_role("button", name="Continue →").click()
        self.page.get_by_role("button", name="Continue →").click()
        self.page.locator("#Q25").fill("SYNTHETIC: retryable local browser test comment.")
        self.page.get_by_role("button", name="Review and submit →").click()

    def test_synthetic_invitation_submits_after_server_confirmation(self):
        self.open_invitation()
        self.complete_form()
        self.page.get_by_text("The server confirmed that your questionnaire response was stored.").wait_for()
        self.assertEqual(len(self.posts), 1)
        payload = self.posts[0]
        self.assertEqual(payload["invitation_token"], TOKEN)
        self.assertTrue(payload["age_18_plus"])
        self.assertNotIn("consent_confirmed", payload)
        self.assertEqual(payload["instrument_version"], "evaluation-prototype-v2-2026-10-31")
        self.assertEqual(payload["tasks"], ["Task 1 — A/L learner profile"])
        self.assertIn("Q6", payload["answers"])
        self.assertEqual(len(payload["idempotency_key"]), 36)
        self.assertLessEqual(self.page.evaluate("document.documentElement.scrollWidth"), 390)
        self.assertEqual(self.errors, [])

    def test_network_failure_keeps_answers_and_retry_reuses_idempotency_key(self):
        self.fail_first = True
        self.open_invitation()
        self.complete_form()
        self.page.get_by_text("Network error. Your answers remain in this page; check the connection and retry.").wait_for()
        self.assertNotIn("RESPONSE RECEIVED", self.page.locator("#app").inner_text())
        self.page.get_by_role("button", name="← Edit answers").click()
        self.assertEqual(self.page.locator("#Q25").input_value(), "SYNTHETIC: retryable local browser test comment.")
        self.page.get_by_role("button", name="Review and submit →").click()
        self.page.get_by_text("The server confirmed that your questionnaire response was stored.").wait_for()
        self.assertEqual(len(self.posts), 2)
        self.assertEqual(self.posts[0]["idempotency_key"], self.posts[1]["idempotency_key"])
        self.assertEqual(self.posts[0]["answers"], self.posts[1]["answers"])
        self.assertEqual(self.errors, [])


if __name__ == "__main__":
    unittest.main()
