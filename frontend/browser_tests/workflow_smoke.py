"""Exercise the visual starting cards, optional steps, tool wizard and mobile flow."""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright, expect


def main():
    base = os.getenv('WISELANKA_FRONTEND_URL', 'http://127.0.0.1:5501')
    artifacts = Path(__file__).resolve().parents[2] / '.cache' / 'workflow'
    artifacts.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, channel=os.getenv('WISELANKA_BROWSER_CHANNEL') or None)
        page = browser.new_page(viewport={'width': 1440, 'height': 1000})
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        try:
            page.goto(base + '/', wait_until='networkidle')
            expect(page.locator('.un-actions .un-button')).to_have_count(2)
            expect(page.locator('.ux-route')).to_have_count(0)
            page.screenshot(path=str(artifacts / 'home.png'))
            page.locator('.wl-navigation').get_by_role('link', name='Pathways', exact=True).click()
            expect(page.locator('.ux-stage-link')).to_have_count(4)
            page.locator('.ux-stage-link').first.click()
            expect(page.locator('.ux-current-stage')).to_contain_text('O/L results')
            expect(page.locator('.ux-education-options')).to_be_hidden()
            page.screenshot(path=str(artifacts / 'profile.png'))
            page.locator('.ux-current-stage').click()
            expect(page.locator('.ux-education-options')).to_be_visible()
            page.locator('[data-education-stage=ordinary]').click()
            for field in ['olMathematics', 'olEnglish', 'olGrade3', 'olGrade4', 'olGrade5', 'olGrade6']:
                page.select_option('#' + field, 'C')
            page.get_by_role('button', name='Next: Interests').click()
            expect(page.locator('.ux-step-count')).to_have_text('Step 2 of 4')
            page.get_by_role('button', name='Skip for now').click()
            expect(page.locator('.ux-step-count')).to_have_text('Step 3 of 4')
            page.get_by_role('button', name='Skip for now').click()
            expect(page.locator('.ux-step-count')).to_have_text('Step 4 of 4')
            expect(page.locator('#submitProfile')).to_be_visible()
            with page.expect_response(lambda response: response.url.endswith('/personalised-recommendations')) as result:
                page.locator('#submitProfile').click()
            assert result.value.status == 200
            expect(page.locator('.ux-next-steps')).to_be_visible()
            page.locator('.ux-next-steps').get_by_role('link', name='Check a course').click()
            expect(page.locator('.tool-progress')).to_be_visible()
            expect(page.locator('.ux-selection-summary')).to_contain_text('Information Technology')
            expect(page.locator('#grade1')).to_have_value('')
            expect(page.locator('.ux-step-count')).to_have_text('Step 1 of 2')
            page.evaluate("async () => { if (document.activeViewTransition) await document.activeViewTransition.finished; }")
            page.screenshot(path=str(artifacts / 'eligibility.png'), animations='disabled')
            for i, subject in enumerate(['Physics', 'Chemistry', 'Combined Mathematics'], 1):
                page.select_option('#subject' + str(i), subject)
                page.select_option('#grade' + str(i), 'C')
            page.get_by_role('button', name='Review my choices').click()
            with page.expect_response(lambda response: response.url.endswith('/eligibility')) as result:
                page.locator('#checkButton').click()
            assert result.value.status == 200
            expect(page.locator('#resultCard')).to_be_visible()
            page.goto(base + '/frontend/pages/scholarships.html', wait_until='networkidle')
            expect(page.locator('.ux-selection-summary')).to_contain_text('Stipendium')
            expect(page.locator('.ux-step-count')).to_have_text('Step 1 of 3')
            page.screenshot(path=str(artifacts / 'scholarships.png'))
            page.select_option('#citizenship', 'Sri Lanka')
            page.fill('#age', '20')
            page.get_by_role('button', name='Next: Education').click()
            page.select_option('#olEnglish', 'C')
            page.get_by_role('button', name='Review my choices').click()
            with page.expect_response(lambda response: '/scholarships/' in response.url and response.url.endswith('/eligibility')) as result:
                page.locator('#checkButton').click()
            assert result.value.status == 200
            expect(page.locator('#scholarshipResults')).to_be_visible()
            page.set_viewport_size({'width': 390, 'height': 844})
            page.goto(base + '/frontend/pages/learner-profile.html', wait_until='networkidle')
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1')
            icon = page.locator('.wl-chat-launcher').bounding_box()
            stage = page.locator('.ux-current-stage').bounding_box()
            assert icon['y'] + icon['height'] < stage['y']
            page.screenshot(path=str(artifacts / 'profile-mobile.png'))
            page.goto(base + '/', wait_until='networkidle')
            expect(page.locator('.un-actions .un-button')).to_have_count(2)
            page.goto(base + '/frontend/pages/pathways.html', wait_until='networkidle')
            page.locator('.ux-stage-link').nth(1).click()
            expect(page.locator('.ux-current-stage')).to_contain_text('A/L results')
            expect(page.locator('#educationLevel')).to_have_value('A_LEVEL')
            assert not errors, errors
            print('PASS: restored home, profile layout, stage changing, optional steps, course and scholarship assessments, next actions and mobile layout')
        finally:
            browser.close()


if __name__ == '__main__':
    main()
