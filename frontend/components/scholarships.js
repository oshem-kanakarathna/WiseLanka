
"use strict";

/*
 * WiseLanka — Scholarship Intelligence
 *
 * Frontend integration for the deterministic
 * scholarship eligibility engine.
 *
 * Scholarship eligibility and application
 * availability are separate concepts.
 *
 * An eligible assessment does not guarantee
 * nomination, selection, admission, or an award.
 */

const SCHOLARSHIP_API = "http://127.0.0.1:8000";

// ----------------------------------------
// DOM references
// ----------------------------------------

const scholarshipForm = document.getElementById("scholarshipForm");
const checkButton = document.getElementById("checkButton");

const emptyResult = document.getElementById("emptyResult");
const loadingResult = document.getElementById("loadingResult");
const errorResult = document.getElementById("errorResult");
const scholarshipResults = document.getElementById("scholarshipResults");

const resultName = document.getElementById("resultName");
const resultProvider = document.getElementById("resultProvider");
const eligibilityBadge = document.getElementById("eligibilityBadge");
const eligibilityExplanation = document.getElementById("eligibilityExplanation");
const applicationStatus = document.getElementById("applicationStatus");

const scholarshipDetails = document.getElementById("scholarshipDetails");
const fieldEvaluation = document.getElementById("fieldEvaluation");
const requirementsList = document.getElementById("requirementsList");

const resultDisclaimer = document.getElementById("resultDisclaimer");
const officialLink = document.getElementById("officialLink");

// ----------------------------------------
// Default disclaimer
// ----------------------------------------

const DEFAULT_DISCLAIMER =
    "This result indicates apparent eligibility to apply " +
    "based on the rules recorded in the WiseLanka knowledge base. " +
    "It does not guarantee nomination, selection, admission, " +
    "or a scholarship award.";

// ----------------------------------------
// Form value helpers
// ----------------------------------------

function valueOf(id) {
    return document.getElementById(id).value;
}

function optionalNumber(id) {
    const value = valueOf(id);

    if (value === "") {
        return null;
    }

    return Number(value);
}

function optionalBoolean(id) {
    const value = valueOf(id);

    if (value === "") {
        return null;
    }

    return value === "true";
}

function optionalString(id) {
    const value = valueOf(id).trim();

    return value === "" ? null : value;
}

// ----------------------------------------
// Build learner profile
//
// Field names must match the scholarship
// eligibility engine's expected input.
// ----------------------------------------

function createLearnerProfile() {
    return {
        citizenship: optionalString("citizenship"),

        age_on_reference_date: optionalNumber("age"),

        a_level_exam_year: optionalNumber("alYear"),

        a_level_pass_count: optionalNumber("alPasses"),

        o_level_english_grade: optionalString("olEnglish"),

        a_level_english_grade: optionalString("alEnglish"),

        state_university_internal_student:
            optionalBoolean("stateStudent"),

        field: optionalString("field")
    };
}

// ----------------------------------------
// Result visibility
// ----------------------------------------

function showSection(section) {
    [
        emptyResult,
        loadingResult,
        errorResult,
        scholarshipResults
    ].forEach(element => {
        element.classList.add("hidden");
    });

    section.classList.remove("hidden");
}

// ----------------------------------------
// Status labels
// ----------------------------------------

function readableStatus(status) {
    const labels = {
        ELIGIBLE_TO_APPLY: "Eligible to apply",
        POTENTIALLY_ELIGIBLE: "Potentially eligible",
        REQUIREMENTS_NOT_MET: "Requirements not met",
        PASSED: "Passed",
        FAILED: "Failed",
        UNKNOWN: "Unknown",
        NOT_FOUND: "Not found"
    };

    return labels[status] ||
        String(status || "Unknown").replace(/_/g, " ");
}

function statusClass(status) {
    if (
        status === "PASSED" ||
        status === "ELIGIBLE_TO_APPLY"
    ) {
        return "status-passed";
    }

    if (
        status === "FAILED" ||
        status === "REQUIREMENTS_NOT_MET"
    ) {
        return "status-failed";
    }

    return "status-unknown";
}

// ----------------------------------------
// Safe text formatting
// ----------------------------------------

function textOrFallback(value, fallback = "Not recorded") {
    if (
        value === undefined ||
        value === null ||
        value === ""
    ) {
        return fallback;
    }

    return String(value);
}

// ----------------------------------------
// Detail row component
// ----------------------------------------

function appendDetail(container, label, value) {
    const row = document.createElement("div");
    row.className = "detail-row";

    const labelElement = document.createElement("span");
    labelElement.className = "detail-label";
    labelElement.textContent = label;

    const valueElement = document.createElement("span");
    valueElement.className = "detail-value";
    valueElement.textContent = textOrFallback(value);

    row.append(labelElement, valueElement);
    container.appendChild(row);
}

// ----------------------------------------
// Requirement status badge
// ----------------------------------------

function appendStatus(container, status) {
    const badge = document.createElement("span");

    badge.className =
        "requirement-status " + statusClass(status);

    badge.textContent = readableStatus(status);

    container.appendChild(badge);
}

// ----------------------------------------
// Requirement-by-requirement evaluation
// ----------------------------------------

function renderRequirements(requirements) {
    requirementsList.replaceChildren();

    if (
        !Array.isArray(requirements) ||
        requirements.length === 0
    ) {
        requirementsList.textContent =
            "No requirement evaluations were returned.";

        return;
    }

    requirements.forEach(requirement => {
        const item = document.createElement("div");
        item.className = "requirement-item";

        const information = document.createElement("div");

        const description = document.createElement("div");
        description.className = "requirement-description";

        description.textContent = textOrFallback(
            requirement.description,
            "Scholarship requirement"
        );

        const identifier = document.createElement("span");
        identifier.className = "requirement-id";

        identifier.textContent = [
            requirement.requirement_id,
            requirement.explanation
        ].filter(Boolean).join(" — ");

        information.append(description, identifier);
        item.appendChild(information);

        appendStatus(
            item,
            requirement.status || "UNKNOWN"
        );

        requirementsList.appendChild(item);
    });
}

// ----------------------------------------
// Field applicability
//
// API response:
// {
//     field: "STEM",
//     status: "PASSED",
//     applicable_fields: ["STEM", "Agriculture"]
// }
// ----------------------------------------

function renderFieldEvaluation(field) {
    fieldEvaluation.replaceChildren();

    if (!field || typeof field !== "object") {
        fieldEvaluation.textContent =
            "No field applicability information was returned.";

        return;
    }

    appendDetail(
        fieldEvaluation,
        "Selected field",
        field.field
    );

    appendDetail(
        fieldEvaluation,
        "Field evaluation",
        readableStatus(field.status)
    );

    appendDetail(
        fieldEvaluation,
        "Recorded applicable fields",
        Array.isArray(field.applicable_fields)
            ? field.applicable_fields.join(", ")
            : "Not recorded"
    );
}

// ----------------------------------------
// Scholarship metadata
//
// Uses the exact fields returned by
// backend/app/scholarships/engine.py
// ----------------------------------------

function renderScholarshipDetails(scholarship) {
    scholarshipDetails.replaceChildren();

    const details = [
        [
            "Scholarship type",
            scholarship.scholarship_type
        ],
        [
            "Coverage",
            scholarship.coverage_description
        ],
        [
            "Opening date",
            scholarship.opening_date
        ],
        [
            "Closing date",
            scholarship.closing_date
        ],
        [
            "Recorded status",
            scholarship.scholarship_status
        ],
        [
            "Last verified",
            scholarship.last_verified_date
        ]
    ];

    details.forEach(([label, value]) => {
        appendDetail(
            scholarshipDetails,
            label,
            value
        );
    });
}

// ----------------------------------------
// Application status
//
// IMPORTANT:
// The API uses scholarship_status,
// not status.
//
// Application status is independent
// of eligibility_status.
// ----------------------------------------

function renderApplicationStatus(scholarship) {
    const status = String(
        scholarship.scholarship_status || "Unknown"
    );

    if (status.toLowerCase() === "closed") {
        applicationStatus.textContent =
            "Application window: CLOSED. " +
            "This eligibility assessment does not mean " +
            "applications are currently being accepted.";

        return;
    }

    applicationStatus.textContent =
        "Recorded application status: " +
        status +
        ". Verify the current application window " +
        "using the official scholarship notice.";
}

// ----------------------------------------
// Official scholarship source
//
// Only HTTP and HTTPS URLs are allowed.
// ----------------------------------------

function renderOfficialLink(url) {
    officialLink.classList.add("hidden");
    officialLink.removeAttribute("href");

    if (typeof url !== "string") {
        return;
    }

    try {
        const parsed = new URL(url);

        if (
            parsed.protocol !== "https:" &&
            parsed.protocol !== "http:"
        ) {
            return;
        }

        officialLink.href = parsed.href;
        officialLink.classList.remove("hidden");

    } catch {
        // Do not display invalid URLs.
    }
}

// ----------------------------------------
// Overall eligibility explanation
// ----------------------------------------

function explainOverallStatus(status) {
    if (status === "ELIGIBLE_TO_APPLY") {
        return (
            "Your supplied information appears to meet " +
            "the recorded eligibility requirements. " +
            "This is not a scholarship award decision."
        );
    }

    if (status === "POTENTIALLY_ELIGIBLE") {
        return (
            "Some required information is missing. " +
            "Complete your profile to obtain a more " +
            "definite eligibility assessment."
        );
    }

    if (status === "REQUIREMENTS_NOT_MET") {
        return (
            "One or more recorded requirements are not met. " +
            "Review the individual evaluations below."
        );
    }

    return (
        "The eligibility assessment could not be determined " +
        "from the returned information."
    );
}

// ----------------------------------------
// Render complete scholarship result
//
// Actual API response is a flat object:
//
// scholarship_id
// scholarship_name
// provider_name
// scholarship_type
// coverage_description
// application_url
// opening_date
// closing_date
// scholarship_status
// last_verified_date
// eligibility_status
// requirements
// field_evaluation
// disclaimer
// ----------------------------------------

function renderScholarshipResult(data) {
    if (
        !data ||
        typeof data !== "object" ||
        data.eligibility_status === "NOT_FOUND" ||
        data.status === "NOT_FOUND"
    ) {
        throw new Error(
            "The selected scholarship was not found " +
            "in the WiseLanka knowledge base."
        );
    }

    const scholarship = data;

    // Scholarship identity

    resultName.textContent = textOrFallback(
        scholarship.scholarship_name,
        "Scholarship eligibility assessment"
    );

    resultProvider.textContent = textOrFallback(
        scholarship.provider_name,
        "Scholarship provider not recorded"
    );

    // Overall eligibility status

    const overallStatus =
        data.eligibility_status || "UNKNOWN";

    eligibilityBadge.className =
        "status-badge " + statusClass(overallStatus);

    eligibilityBadge.textContent =
        readableStatus(overallStatus);

    eligibilityExplanation.textContent =
        explainOverallStatus(overallStatus);

    // Application availability

    renderApplicationStatus(scholarship);

    // Scholarship information

    renderScholarshipDetails(scholarship);

    // Field applicability

    renderFieldEvaluation(
        data.field_evaluation
    );

    // Requirement evaluations

    renderRequirements(
        data.requirements
    );

    // Disclaimer

    resultDisclaimer.textContent =
        data.disclaimer || DEFAULT_DISCLAIMER;

    // Official source

    renderOfficialLink(
        data.application_url
    );
}

// ----------------------------------------
// Submit scholarship eligibility request
// ----------------------------------------

async function checkScholarship(event) {
    event.preventDefault();

    const scholarshipId = valueOf("scholarshipId");

    if (!/^SCH[0-9]+$/.test(scholarshipId)) {
        errorResult.textContent =
            "Please select a valid scholarship.";

        showSection(errorResult);
        return;
    }

    const learnerProfile = createLearnerProfile();

    checkButton.disabled = true;
    checkButton.setAttribute("aria-busy", "true");

    showSection(loadingResult);

    try {
        const response = await fetch(
            `${SCHOLARSHIP_API}/scholarships/${scholarshipId}/eligibility`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    learner_profile: learnerProfile
                })
            }
        );

        if (!response.ok) {
            throw new Error(
                `Scholarship API returned HTTP ${response.status}.`
            );
        }

        const data = await response.json();

        renderScholarshipResult(data);

        showSection(scholarshipResults);

    } catch (error) {
        console.error(
            "Scholarship eligibility error:",
            error
        );

        errorResult.textContent =
            "Unable to complete the scholarship check. " +
            error.message +
            " Verify that the WiseLanka backend is running.";

        showSection(errorResult);

    } finally {
        checkButton.disabled = false;
        checkButton.removeAttribute("aria-busy");
    }
}

// ----------------------------------------
// Initialise scholarship form
// ----------------------------------------

scholarshipForm.addEventListener(
    "submit",
    checkScholarship
);
