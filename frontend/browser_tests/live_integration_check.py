
"""Live WiseLanka browser/API check. Requires servers on ports 5500 and 8000."""

from playwright.sync_api import sync_playwright

PAGE_URL = "http://127.0.0.1:5500/frontend/pages/learner-profile.html"
API_PATH = "/personalised-recommendations"


def main():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)

        try:
            page = browser.new_page()
            page.goto(PAGE_URL, wait_until="load")

            page.locator("#educationLevel").select_option("O_LEVEL")

            for field in (
                "olMathematics",
                "olEnglish",
                "olGrade3",
                "olGrade4",
                "olGrade5",
                "olGrade6",
            ):
                page.locator("#" + field).select_option("C")

            with page.expect_response(
                lambda response: response.url.endswith(API_PATH)
            ) as response_info:
                page.locator("#learnerProfileForm").evaluate(
                    "(form) => form.requestSubmit()"
                )

            response = response_info.value

            assert response.status == 200, (
                f"API returned HTTP {response.status}"
            )

            data = response.json()
            recommendations = data["recommendations"]

            assert recommendations, "API returned no recommendations"

            expected_cards = len(recommendations)

            expected_pathways = sum(
                len(item.get("progression", {}).get("pathways", []))
                for item in recommendations
            )

            assert expected_pathways > 0, "No pathways in API response"

            page.wait_for_function(
                """([cards, pathways]) =>
                    document.querySelectorAll('.recommendation-card').length === cards &&
                    document.querySelectorAll('.progression-item').length === pathways""",
                arg=[expected_cards, expected_pathways],
                timeout=10000,
            )

            first_card_text = page.locator(
                ".recommendation-card"
            ).first.inner_text()

            assert recommendations[0]["programme_name"] in first_card_text, (
                "Displayed programme does not match API response"
            )

            print("PASS: Live browser-to-FastAPI integration")
            print(f"Recommendations rendered: {expected_cards}")
            print(f"Progression pathways rendered: {expected_pathways}")

        finally:
            browser.close()


if __name__ == "__main__":
    main()
