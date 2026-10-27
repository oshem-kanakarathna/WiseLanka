
"use strict";

const API_URL = "http://127.0.0.1:8000/personalised-recommendations";

const form = document.getElementById("learnerProfileForm");
const educationLevel = document.getElementById("educationLevel");
const alSubjects = document.getElementById("alSubjects");
const olSubjects = document.getElementById("olSubjects");
const additionalOlSubjects = document.getElementById("additionalOlSubjects");
const submitButton = document.getElementById("submitProfile");
const statusMessage = document.getElementById("statusMessage");
const resultsSummary = document.getElementById("resultsSummary");
const recommendationList = document.getElementById("recommendationList");

const OL_OPTIONAL_SUBJECTS = [
    "Science",
    "ICT",
    "Sinhala",
    "Tamil",
    "History",
    "Geography",
    "Commerce",
    "Art"
];

const OL_DEFAULT_SUBJECTS = [
    "Science",
    "ICT",
    "Sinhala",
    "History"
];


const GRADES = ["A", "B", "C", "S", "F"];

function createElement(tag, className = "", text = null) {
    const element = document.createElement(tag);

    if (className) {
        element.className = className;
    }

    if (text !== null && text !== undefined) {
        element.textContent = String(text);
    }

    return element;
}

function createOption(value, selected = false) {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value;
    option.selected = selected;
    return option;
}

function createOlSubjects() {
    additionalOlSubjects.replaceChildren();

    OL_DEFAULT_SUBJECTS.forEach((defaultSubject, index) => {
        const number = index + 3;

        const row = createElement("div", "subject-row");

        const label = createElement(
            "label",
            "",
            `O/L Subject ${number}`
        );

        label.htmlFor = `olSubject${number}`;

        const subjectSelect = createElement("select");
        subjectSelect.id = `olSubject${number}`;

        OL_OPTIONAL_SUBJECTS.forEach(subject => {
            subjectSelect.appendChild(
                createOption(subject, subject === defaultSubject)
            );
        });

        const gradeSelect = createElement("select");
        gradeSelect.id = `olGrade${number}`;
        gradeSelect.setAttribute(
            "aria-label",
            `O/L subject ${number} grade`
        );

        // Start with no grade selected.
        const placeholder = createOption("", true);
        placeholder.textContent = "Select grade";
        placeholder.disabled = true;
        gradeSelect.appendChild(placeholder);

        GRADES.forEach(grade => {
            gradeSelect.appendChild(
                createOption(grade)
            );
        });

        row.append(label, subjectSelect, gradeSelect);
        additionalOlSubjects.appendChild(row);
    });
}

function updateEducationLevel() {
    const isAL = educationLevel.value === "A_LEVEL";

    alSubjects.classList.toggle("hidden", !isAL);
    olSubjects.classList.toggle("hidden", isAL);
}

function readSubjectResults(subjectIds, gradeIds, missingGrades = []) {
    const results = {};
    const usedSubjects = new Set();

    subjectIds.forEach((subjectId, index) => {
        const subject = document.getElementById(subjectId).value;
        const grade = document.getElementById(gradeIds[index]).value;

        if (!grade) {
            missingGrades.push(subject);
        }

        if (usedSubjects.has(subject)) {
            throw new Error(
                `You selected "${subject}" more than once. ` +
                "Please select different subjects."
            );
        }

        usedSubjects.add(subject);

        if (grade) {
            results[subject] = grade;
        }
    });

    return results;
}

function collectEducation() {
    const missingGrades = [];

    if (educationLevel.value === "A_LEVEL") {
        const alResults = readSubjectResults(
            ["alSubject1", "alSubject2", "alSubject3"],
            ["alGrade1", "alGrade2", "alGrade3"],
            missingGrades
        );

        if (missingGrades.length > 0) {
            throw new Error(
                "Please select grades for: " +
                missingGrades.join(", ") + "."
            );
        }

        return {
            A_LEVEL: alResults
        };
    }

    const mathematicsGrade =
        document.getElementById("olMathematics").value;

    const englishGrade =
        document.getElementById("olEnglish").value;

    if (!mathematicsGrade) {
        missingGrades.push("Mathematics");
    }

    if (!englishGrade) {
        missingGrades.push("English");
    }

    const optionalResults = readSubjectResults(
        ["olSubject3", "olSubject4", "olSubject5", "olSubject6"],
        ["olGrade3", "olGrade4", "olGrade5", "olGrade6"],
        missingGrades
    );

    if (missingGrades.length > 0) {
        throw new Error(
            "Please select grades for: " +
            missingGrades.join(", ") + "."
        );
    }

    return {
        O_LEVEL: {
            Mathematics: mathematicsGrade,
            English: englishGrade,
            ...optionalResults
        }
    };
}

function collectProfile() {
    const interests = Array.from(
        document.querySelectorAll(
            'input[name="interests"]:checked'
        )
    ).map(input => input.value);

    const preferences = {};

    const studyMode = document.getElementById("studyMode").value;
    const district = document.getElementById("district").value;

    if (studyMode) {
        preferences.study_mode = studyMode;
    }

    if (district) {
        preferences.district = district;
    }

    return {
        learner_profile: {
            education: collectEducation(),
            interests,
            career_goal_id: document.getElementById("careerGoal").value,
            preferences
        }
    };
}

function showStatus(message, isError = false) {
    statusMessage.textContent = message;
    statusMessage.classList.toggle("error", isError);
    statusMessage.classList.remove("hidden");
}

function hideStatus() {
    statusMessage.classList.add("hidden");
}

function formatStatus(status) {
    return String(status || "NOT_ASSESSED")
        .replaceAll("_", " ")
        .toLowerCase()
        .replace(/\b\w/g, character => character.toUpperCase());
}

function appendDetail(card, heading, description) {
    if (!description) {
        return;
    }

    const section = createElement(
        "div",
        "recommendation-detail"
    );

    section.appendChild(
        createElement("strong", "", heading)
    );

    section.appendChild(
        createElement("p", "", description)
    );

    card.appendChild(section);
}

function appendEvidence(card, programme) {
    const passed = Array.isArray(programme.passed_requirements)
        ? programme.passed_requirements
        : [];

    const failed = Array.isArray(programme.failed_requirements)
        ? programme.failed_requirements
        : [];

    if (passed.length > 0) {
        appendDetail(
            card,
            "Requirements satisfied",
            passed.join("; ")
        );
    }

    if (failed.length > 0) {
        appendDetail(
            card,
            "Requirements needing attention",
            failed.join("; ")
        );
    }
}

function getCareerAssessment(programme) {
    const assessment = programme.career_goal_assessment || {};

    if (assessment.status === "NOT_PROVIDED") {
        return {
            label: "Career goal not selected",
            detail:
                "You have not selected a career goal. " +
                "Choose a career to explore recorded " +
                "programme-to-career relationships."
        };
    }

    if (assessment.status !== "ASSESSED") {
        return {
            label: "Career alignment not assessed",
            detail:
                assessment.explanation ||
                "The knowledge base does not contain enough " +
                "evidence to assess this career relationship."
        };
    }

    const score = programme.personal_suitability_score;

    return {
        label: typeof score === "number"
            ? `Recorded career alignment: ${score}/100`
            : "Career relationship assessed",
        detail:
            assessment.explanation ||
            "This assessment uses recorded programme-to-career " +
            "relationships. It does not predict employment."
    };
}

function describeInterestAssessment(assessment) {
    if (!assessment || typeof assessment !== "object") {
        return "Interest assessment is not available.";
    }

    const matched = Array.isArray(assessment.matched_interests)
        ? assessment.matched_interests
        : [];

    const summary = matched.length > 0
        ? `Matched interests: ${matched.join(", ")}.`
        : "No direct descriptive interest match was found.";

    return [
        summary,
        assessment.explanation || ""
    ].filter(Boolean).join(" ");
}

function describePreferences(assessment) {
    if (!assessment || typeof assessment !== "object") {
        return "No preference assessment is available.";
    }

    const comparisons = Array.isArray(assessment.comparisons)
        ? assessment.comparisons
        : [];

    if (comparisons.length === 0) {
        return "No study preferences were provided for comparison.";
    }

    const descriptions = comparisons.map(comparison => {
        const label = comparison.field === "study_mode"
            ? "Study mode"
            : comparison.field === "district"
                ? "District"
                : formatStatus(comparison.field);

        const preferred = comparison.preferred || "Not specified";
        const actual = comparison.actual || "Not recorded";

        if (comparison.status === "MATCH") {
            return `${label}: matches your preference (${preferred}).`;
        }

        if (comparison.status === "NO_MATCH") {
            return (
                `${label}: you prefer ${preferred}, ` +
                `but the programme lists ${actual}.`
            );
        }

        return (
            `${label}: you prefer ${preferred}, ` +
            "but the programme information is insufficient " +
            "to confirm a match."
        );
    });

    return descriptions.join(" ");
}

function appendOfficialLink(card, programme) {
    const url = programme.application_url;

    if (typeof url !== "string" || !url.trim()) {
        return;
    }

    let parsedUrl;

    try {
        parsedUrl = new URL(url);
    } catch {
        return;
    }

    if (!["https:", "http:"].includes(parsedUrl.protocol)) {
        return;
    }

    const section = createElement(
        "div",
        "recommendation-detail"
    );

    const link = createElement(
        "a",
        "",
        "View programme information ↗"
    );

    link.href = parsedUrl.href;
    link.target = "_blank";
    link.rel = "noopener noreferrer";

    section.appendChild(link);
    card.appendChild(section);
}

function appendAcademicProgression(card, programme) {
    const pathways = programme.progression?.pathways;
    if (!Array.isArray(pathways) || !pathways.length) return;

    const section = createElement("section", "recommendation-detail academic-progression");
    section.appendChild(createElement("strong", "", "Possible Academic Progression"));

    pathways.forEach(pathway => {
        const item = createElement("div", "progression-item");
        item.appendChild(createElement("h4", "", pathway.qualification_name || "Further qualification"));

        const providers = [...new Set(
            (pathway.programmes || []).map(p => p.provider_name).filter(Boolean)
        )];

        if (providers.length) {
            item.appendChild(createElement("p", "", "Provider: " + providers.join(", ")));
        }
        if (pathway.conditions) {
            item.appendChild(createElement("p", "", "Conditions: " + pathway.conditions));
        }

        item.appendChild(createElement("p", "progression-status",
            pathway.guaranteed === true ? "Recorded as guaranteed progression" : "Progression not guaranteed"
        ));
        section.appendChild(item);
    });

    card.appendChild(section);
}

function createRecommendationCard(programme) {
    const card = createElement(
        "article",
        "recommendation-card"
    );

    card.appendChild(
        createElement(
            "h3",
            "",
            programme.programme_name ||
            programme.programme_id ||
            "Unnamed programme"
        )
    );

    const programmeInfo = [
        programme.field_of_study,
        programme.programme_type,
        programme.campus
    ].filter(Boolean);

    if (programmeInfo.length > 0) {
        card.appendChild(
            createElement(
                "p",
                "",
                programmeInfo.join(" · ")
            )
        );
    }

    const metadata = createElement(
        "div",
        "recommendation-meta"
    );

    // The backend uses "category" for academic eligibility.
    const category = programme.category || "NOT_ASSESSED";

    metadata.appendChild(
        createElement(
            "span",
            `result-tag ${category.toLowerCase().replaceAll("_", "-")}`,
            `Academic eligibility: ${formatStatus(category)}`
        )
    );

    if (typeof programme.academic_match_score === "number") {
        metadata.appendChild(
            createElement(
                "span",
                "result-tag",
                `Academic requirement match: ` +
                `${programme.academic_match_score}/100`
            )
        );
    }

    const career = getCareerAssessment(programme);

    metadata.appendChild(
        createElement(
            "span",
            "result-tag",
            career.label
        )
    );

    card.appendChild(metadata);

    appendDetail(
        card,
        "Career alignment",
        career.detail
    );

    appendDetail(
        card,
        "Your interests",
        describeInterestAssessment(programme.interest_assessment)
    );

    appendDetail(
        card,
        "Study preferences",
        describePreferences(programme.preference_assessment)
    );

    appendAcademicProgression(card, programme);
    appendEvidence(card, programme);
    appendOfficialLink(card, programme);

    return card;
}

function renderRecommendations(data) {
    recommendationList.replaceChildren();
    resultsSummary.replaceChildren();

    if (!data || !Array.isArray(data.recommendations)) {
        throw new Error(
            "Invalid API response: expected a recommendations array."
        );
    }

    const programmes = data.recommendations;

    if (programmes.length === 0) {
        resultsSummary.classList.add("hidden");

        showStatus(
            "No programmes were returned for this profile. " +
            "The current knowledge base covers a limited " +
            "selection of Sri Lankan education pathways."
        );

        return;
    }

    resultsSummary.appendChild(
        createElement(
            "p",
            "",
            `${programmes.length} programme(s) evaluated ` +
            "against your learner profile."
        )
    );

    resultsSummary.classList.remove("hidden");

    programmes.forEach(programme => {
        recommendationList.appendChild(
            createRecommendationCard(programme)
        );
    });

    hideStatus();
}

async function submitLearnerProfile(event) {
    event.preventDefault();

    recommendationList.replaceChildren();
    resultsSummary.replaceChildren();
    resultsSummary.classList.add("hidden");

    let payload;

    try {
        payload = collectProfile();

    } catch (error) {
        showStatus(error.message, true);
        return;
    }

    submitButton.disabled = true;
    showStatus("Evaluating your learner profile...");

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (!response.ok) {
            const detail = typeof data.detail === "string"
                ? data.detail
                : "The API could not process this profile.";

            throw new Error(detail);
        }

        renderRecommendations(data);
    } catch (error) {
        const message = error instanceof TypeError
            ? "Could not connect to the WiseLanka API. " +
              "Make sure the backend is running on port 8000."
            : error.message;

        showStatus(message, true);
    } finally {
        submitButton.disabled = false;
    }
}

createOlSubjects();
updateEducationLevel();

educationLevel.addEventListener(
    "change",
    updateEducationLevel
);

form.addEventListener(
    "submit",
    submitLearnerProfile
);
