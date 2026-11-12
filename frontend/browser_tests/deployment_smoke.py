"""HTTP browser check against a built frontend and the real API.

Build first, then serve dist on port 5501 and the API on port 8000.
"""
import os
import time
from playwright.sync_api import sync_playwright, expect


def main():
    base = os.getenv('WISELANKA_FRONTEND_URL', 'http://127.0.0.1:5501')
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, channel=os.getenv('WISELANKA_BROWSER_CHANNEL') or None)
        context = browser.new_context()
        page = context.new_page()
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        try:
            page.goto(base + '/', wait_until='networkidle')
            expect(page.locator('.wl-navigation .wl-nav-link')).to_have_count(6)
            page.locator('.wl-chat-launcher').focus()
            page.locator('.wl-chat-launcher').press('Enter')
            page.wait_for_function("document.querySelector('#wl-chat-programme').options.length > 1")
            programme = page.locator('#wl-chat-programme option').nth(1).get_attribute('value')
            page.select_option('#wl-chat-programme', programme)
            actual_status = []

            def hold_real_answer(route):
                response = route.fetch()
                actual_status.append(response.status)
                assert page.locator('.wl-chat').evaluate("el => el.classList.contains('is-thinking')")
                assert page.locator('.wl-chat-thinking').get_attribute('src').endswith('chatbot-thinking.mp4')
                time.sleep(.2)
                route.fulfill(response=response)

            page.route('**/assistant/guidance', hold_real_answer)
            page.locator('[data-intent="programme"]').click()
            expect(page.locator('.wl-chat')).not_to_have_class('wl-chat is-thinking', timeout=15000)
            expect(page.locator('.wl-chat-message')).to_have_count(5, timeout=15000)
            assert actual_status == [200]
            page.unroute('**/assistant/guidance', hold_real_answer)
            page.route('**/assistant/guidance', lambda route: route.abort())
            page.locator('[data-intent="help"]').click()
            expect(page.get_by_role('button', name='Retry question')).to_be_visible()
            page.unroute('**/assistant/guidance')
            page.get_by_role('button', name='Retry question').click()
            expect(page.get_by_role('button', name='Retry question')).to_have_count(0)
            expect(page.locator('.wl-chat-messages')).to_contain_text('Supported topics:')
            page.locator('.wl-chat-close').click()

            page.goto(base + '/frontend/pages/learner-profile.html', wait_until='networkidle')
            page.locator('[data-education-stage=ordinary]').click()
            for field in ['olMathematics', 'olEnglish', 'olGrade3', 'olGrade4', 'olGrade5', 'olGrade6']:
                page.select_option('#' + field, 'C')
            page.wait_for_function("JSON.parse(localStorage.getItem('wiselanka.profile.v1'))?.profile?.education?.O_LEVEL?.Mathematics === 'C'")
            page.reload(wait_until='networkidle')
            expect(page.locator('#olMathematics')).to_have_value('C')
            expect(page.locator('.wl-draft')).to_contain_text('restored')
            for _ in range(3):
                page.locator('.profile-step-actions .primary-button:visible').click()
            with page.expect_response(lambda response: response.url.endswith('/personalised-recommendations')) as result:
                page.locator('#submitProfile').click()
            assert result.value.status == 200
            expect(page.locator('.recommendation-card').first).to_be_visible(timeout=15000)

            page.goto(base + '/frontend/pages/recommendations.html', wait_until='networkidle')
            page.get_by_role('button', name='Use saved results').click()
            expect(page.locator('#olMathematics')).to_have_value('C')
            page.goto(base + '/frontend/pages/learner-profile.html', wait_until='networkidle')
            page.get_by_role('button', name='Clear saved draft').click()
            page.wait_for_load_state('networkidle')
            assert page.evaluate("localStorage.getItem('wiselanka.profile.v1')") is None
            for target in ['about', 'pathways', 'eligibility', 'scholarships']:
                page.goto(base + '/frontend/pages/' + target + '.html', wait_until='networkidle')
                expect(page.locator('.wl-navigation .wl-nav-link[aria-current=page]')).to_have_count(1)
            page.set_viewport_size({'width': 390, 'height': 844})
            for target in ['', 'frontend/pages/learner-profile.html', 'frontend/pages/about.html']:
                page.goto(base + '/' + target, wait_until='networkidle')
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), target
                assert page.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--wl-gutter').trim()") == '20px'
                page.locator('.wl-menu-toggle').click()
                expect(page.locator('.wl-navigation')).to_have_attribute('data-open', 'true')
                page.locator('.wl-menu-toggle').click()
            page.locator('.wl-chat-launcher').focus()
            page.locator('.wl-chat-launcher').press('Enter')
            expect(page.locator('#wl-chat-question')).to_be_visible()
            assert page.locator('.wl-chat-panel').bounding_box()['width'] <= 390
            assert not errors, errors
            print('PASS: built pages, live chat, thinking state, retry, profile restore, assessment, result reuse, draft clearing, navigation and mobile layout')
        finally:
            browser.close()


if __name__ == '__main__':
    main()
