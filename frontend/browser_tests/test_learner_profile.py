import unittest
from pathlib import Path
from playwright.sync_api import sync_playwright

PAGE = (
    Path(__file__).resolve().parents[1]
    / "pages"
    / "learner-profile.html"
)

class LearnerProfileTests(unittest.TestCase):

    def test_missing_ol_grades(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            try:
                page = browser.new_page()
                api_requests = []

                page.on(
                    "request",
                    lambda request: api_requests.append(request.url)
                    if "personalised-recommendations" in request.url
                    else None
                )

                page.goto(PAGE.as_uri())
                page.locator("#educationLevel").select_option("O_LEVEL")

                page.locator("#learnerProfileForm").evaluate(
                    "(form) => form.dispatchEvent("
                    "new Event('submit', {bubbles:true, cancelable:true}))"
                )

                message = page.locator("#statusMessage").inner_text()

                self.assertIn("Please select grades for:", message)
                self.assertEqual(api_requests, [])
            finally:
                browser.close()


    def test_missing_al_grades(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            try:
                page = browser.new_page()
                requests = []
                page.on("request", lambda r: requests.append(r.url)
                        if "personalised-recommendations" in r.url else None)

                page.goto(PAGE.as_uri())
                page.locator("#educationLevel").select_option("A_LEVEL")
                page.locator("#learnerProfileForm").evaluate(
                    "(form) => form.requestSubmit()"
                )

                message = page.locator("#statusMessage").inner_text()
                self.assertIn("Please select grades for:", message)
                self.assertEqual(requests, [])
            finally:
                browser.close()


    def test_duplicate_ol_subjects(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            try:
                page = browser.new_page()
                requests = []
                page.on(
                    "request",
                    lambda r: requests.append(r.url)
                    if "personalised-recommendations" in r.url
                    else None
                )

                page.goto(PAGE.as_uri())
                page.locator("#educationLevel").select_option("O_LEVEL")

                for field in (
                    "olMathematics", "olEnglish",
                    "olGrade3", "olGrade4",
                    "olGrade5", "olGrade6"
                ):
                    page.locator("#" + field).select_option("C")

                duplicate = page.locator("#olSubject3").input_value()
                page.locator("#olSubject4").select_option(duplicate)

                page.locator("#learnerProfileForm").evaluate(
                    "(form) => form.requestSubmit()"
                )

                message = page.locator("#statusMessage").inner_text()
                self.assertIn("more than once", message)
                self.assertEqual(requests, [])
            finally:
                browser.close()

if __name__ == "__main__":
    unittest.main()
