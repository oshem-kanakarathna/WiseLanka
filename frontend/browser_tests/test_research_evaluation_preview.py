"""The research questionnaire is a local preview; no responses leave the page."""
import unittest
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / "frontend/pages/research-evaluation.html"


class ResearchEvaluationPreviewTests(unittest.TestCase):
    def setUp(self):
        self.p = sync_playwright().start()
        self.browser = self.p.chromium.launch(channel="chrome", headless=True)
        self.page = self.browser.new_page()
        self.requests = []
        self.page.on("request", lambda request: self.requests.append(request.url) if request.url.startswith(("http://", "https://")) else None)
        self.page.add_init_script("""
            window.previewStorageWrites = [];
            for (const name of ['localStorage', 'sessionStorage']) {
                const store = window[name];
                const original = store.setItem.bind(store);
                store.setItem = (...args) => { window.previewStorageWrites.push(name); return original(...args); };
            }
            window.previewSubmitEvents = 0;
            document.addEventListener('submit', () => window.previewSubmitEvents++, true);
        """)

    def tearDown(self):
        self.browser.close()
        self.p.stop()

    def open(self, width=1280, height=900):
        self.page.set_viewport_size({"width": width, "height": height})
        self.page.goto(PAGE.as_uri())
        self.page.get_by_text("Research preview only — responses are not saved or transmitted.").wait_for()

    def adult_start(self):
        self.page.locator("#age-yes").check()
        self.page.get_by_role("button", name="Continue →").click()

    def advance_to_usability(self):
        self.adult_start()
        # The local preview permits omitted context answers.
        self.page.get_by_role("button", name="Continue →").click()

    def test_minor_is_blocked_and_adult_can_continue(self):
        self.open()
        self.page.locator("#age-no").check()
        self.assertIn("Please do not continue", self.page.locator("#app").inner_text())
        self.assertEqual(self.page.locator("#app h2").inner_text(), "Before you begin")
        self.page.locator("#age-yes").check()
        self.page.get_by_role("button", name="Continue →").click()
        self.assertIn("Evaluation context", self.page.locator("#app h2").inner_text())

    def test_navigation_progress_and_answers_survive_back(self):
        self.open()
        self.adult_start()
        self.assertIn("Section 2 of 6", self.page.locator("#app").inner_text())
        self.page.locator("#device-1").check()
        self.page.get_by_role("button", name="Continue →").click()
        self.assertIn("Section 3 of 6", self.page.locator("#app").inner_text())
        self.page.get_by_role("button", name="← Back").click()
        self.assertTrue(self.page.locator("#device-1").is_checked())
        self.assertEqual(self.page.locator(".bar").evaluate("e => e.style.width"), "20%")

    def test_rating_optional_text_and_keyboard_navigation(self):
        self.open()
        self.advance_to_usability()
        self.assertIn("Usability", self.page.locator("#app h2").inner_text())
        self.page.locator("#Q5-rating-3").focus()
        self.page.keyboard.press("Space")
        self.assertTrue(self.page.locator("#Q5-rating-3").is_checked())
        # Continue and Back are ordinary keyboard-focusable buttons.
        self.page.get_by_role("button", name="Continue →").focus()
        self.page.keyboard.press("Enter")
        self.assertIn("Clarity & pathways", self.page.locator("#app h2").inner_text())
        self.page.get_by_role("button", name="Continue →").click()
        self.assertIn("Understanding", self.page.locator("#app h2").inner_text())
        self.page.get_by_role("button", name="Continue →").click()
        self.assertIn("Feedback", self.page.locator("#app h2").inner_text())
        self.page.locator("#Q25").fill("Optional preview feedback")
        self.page.get_by_role("button", name="← Back").click()
        self.page.get_by_role("button", name="Continue →").click()
        self.assertEqual(self.page.locator("#Q25").input_value(), "Optional preview feedback")
        self.page.get_by_role("button", name="← Back").click()
        self.page.get_by_role("button", name="← Back").click()
        self.page.get_by_role("button", name="← Back").click()
        self.assertTrue(self.page.locator("#Q5-rating-3").is_checked())

    def test_completion_never_submits_downloads_transmits_or_persists(self):
        self.open()
        self.advance_to_usability()
        for _ in range(3):
            self.page.get_by_role("button", name="Continue →").focus()
            self.page.keyboard.press("Enter")
        self.page.get_by_role("button", name="Review responses →").click()
        self.assertIn("LOCAL PREVIEW COMPLETE", self.page.locator("#app").inner_text())
        self.assertIn("Responses transmitted", self.page.locator("#app").inner_text())
        self.assertFalse(self.page.get_by_role("button", name="Download test response (.json)").count())
        self.assertEqual(self.page.evaluate("window.previewSubmitEvents"), 0)
        self.assertEqual(self.page.evaluate("window.previewStorageWrites"), [])
        self.assertEqual(self.requests, [])
        self.assertFalse(self.page.evaluate("document.querySelector('form')"))

    def test_mobile_and_desktop_have_no_horizontal_overflow(self):
        for width, height in [(1280, 900), (390, 844), (320, 720)]:
            self.open(width, height)
            self.assertLessEqual(
                self.page.evaluate("document.documentElement.scrollWidth"),
                self.page.evaluate("document.documentElement.clientWidth"),
                msg=f"Horizontal overflow at viewport width {width}",
            )
            self.adult_start()
            self.assertLessEqual(
                self.page.evaluate("document.documentElement.scrollWidth"),
                self.page.evaluate("document.documentElement.clientWidth"),
                msg=f"Horizontal overflow after starting at width {width}",
            )


if __name__ == "__main__":
    unittest.main()
