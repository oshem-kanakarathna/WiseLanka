# Accessibility review

Measured with axe-core 4.10.3 (pinned SHA256 in audit script), Chromium headless, WCAG 2A/AA and 2.1AA tagged rules. See accessibility-baseline.json and accessibility-final.json, including incomplete checks. This is automated evidence, not WCAG certification or disabled-user evaluation.

Initial findings: two generic learner-page divs used prohibited aria-label attributes; text contrast failures affected learner-profile, eligibility, recommendations and scholarships pages. Added region semantics and targeted darker text/accent colours. No framework/layout rewrite.

Final scan covers nine states: English/Sinhala/Tamil learner-profile empty and populated, plus three older English pages. Zero detected violations; all 320px and 390px horizontal-reflow probes pass. This only measures those rendered states and the selected rule set. Browser tests cover specific keyboard activation, removal focus, translated labels and mocked voice error feedback.

Manual screen-reader navigation, full keyboard journeys, 200%/400% zoom, dynamic-state contrast, native mobile/browser operation, fluent Sinhala/Tamil review and real microphone/language support remain PENDING in study/manual-checklist.csv. Headless speech capability detection and mocked permission/error events do not establish native recognition accuracy or offline processing.
