
"use strict";

const API_URL = window.WiseAPI.endpoint('personalised-recommendations');

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
    "Art", "Buddhism", "Hinduism", "Islam", "Christianity", "Catholicism",
    "English Literature", "Music", "Dancing", "Drama", "Agriculture",
    "Design and Technology", "Health and Physical Education", "Other subject"
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

let olSubjectCount = 2;
let qualificationCount = 0;
let qualificationOptions = [];

function addOlSubject(defaultSubject = "") {
    const number = ++olSubjectCount;
    const row = createElement("div", "subject-row");
    row.dataset.olRow = number;
    const label = createElement("label", "", `O/L Subject ${number}`);
    label.htmlFor = `olSubject${number}`;
    const subject = createElement("select");
    subject.id = `olSubject${number}`;
    const used = new Set(Array.from(additionalOlSubjects.querySelectorAll("select.subject-select")).map(s => s.value));
    const selected = defaultSubject || OL_OPTIONAL_SUBJECTS.find(s => !used.has(s) && s !== "Other subject");
    subject.className = "subject-select";
    OL_OPTIONAL_SUBJECTS.forEach(name => subject.appendChild(createOption(name, name === selected)));
    const customLabel = createElement("label", "hidden", `Name of O/L subject ${number}`);
    customLabel.htmlFor = `olCustom${number}`;
    const custom = createElement("input", "hidden");
    custom.id = `olCustom${number}`;
    custom.maxLength = 100;
    subject.addEventListener("change", () => {
        const other = subject.value === "Other subject";
        custom.classList.toggle("hidden", !other);
        customLabel.classList.toggle("hidden", !other);
    });
    const grade = createElement("select");
    grade.id = `olGrade${number}`;
    grade.setAttribute("aria-label", `O/L subject ${number} grade`);
    const placeholder = createOption("", true);
    placeholder.textContent = "Select grade";
    placeholder.disabled = true;
    grade.appendChild(placeholder);
    GRADES.forEach(value => grade.appendChild(createOption(value)));
    const unreported = createOption("NOT_REPORTED");
    unreported.textContent = "Not reported";
    grade.appendChild(unreported);
    row.append(label, subject, grade, customLabel, custom);
    if (number > 6) {
        const remove = createElement("button", "secondary-button", `Remove subject ${number}`);
        remove.type = "button";
        remove.addEventListener("click", () => removeProfileRow(row, "addOlSubject"));
        row.appendChild(remove);
    }
    additionalOlSubjects.appendChild(row);
}

function createOlSubjects() {
    OL_DEFAULT_SUBJECTS.forEach(addOlSubject);
}

function updateEducationLevel() {
    alSubjects.classList.toggle("hidden", educationLevel.value !== "A_LEVEL");
    olSubjects.classList.toggle("hidden", educationLevel.value !== "O_LEVEL");
    document.getElementById("completeResultsLabel").classList.toggle("hidden", educationLevel.value === "NONE");
    document.getElementById("educationComplete").checked = false;
}

function removeProfileRow(row, addButtonId) {
    const neighbour = row.nextElementSibling || row.previousElementSibling;
    const target = neighbour?.querySelector("select, input, button") || document.getElementById(addButtonId);
    row.remove();
    target.focus();
}

function populateQualificationSelect(select) {
    const selected = select.value;
    select.replaceChildren();
    const placeholder = createOption("");
    placeholder.textContent = "Enter another award or choose a recorded qualification";
    select.appendChild(placeholder);
    qualificationOptions.forEach(qualification => {
        const option = createOption(qualification.qualification_id);
        option.textContent = qualification.qualification_name;
        select.appendChild(option);
    });
    select.value = qualificationOptions.some(q => q.qualification_id === selected) ? selected : "";
}

function addQualification() {
    const number = ++qualificationCount;
    const row = createElement("div", "qualification-row");
    const fields = {};
    const select = createElement("select");
    select.setAttribute("aria-label", `Recorded qualification ${number}`);
    populateQualificationSelect(select);
    row.appendChild(select);
    [["title", "Award title"], ["framework", "Framework (optional)"], ["level", "Level (optional)"]].forEach(([key, text]) => {
        const label = createElement("label", "", `${text} — qualification ${number}`);
        const input = createElement("input");
        input.id = `qualification-${number}-${key}`;
        input.maxLength = key === "title" ? 160 : key === "framework" ? 80 : 40;
        input.dataset.qualificationField = key;
        label.htmlFor = input.id;
        fields[key] = input;
        row.append(label, input);
    });
    select.addEventListener("change", () => {
        const choice = qualificationOptions.find(q => q.qualification_id === select.value);
        fields.title.value = choice?.qualification_name || "";
        fields.framework.value = choice?.framework_name || "";
        fields.level.value = choice?.framework_level || "";
    });
    // Editing a catalogue value turns it into a custom self-report.
    Object.values(fields).forEach(input => input.addEventListener("input", () => { select.value = ""; }));
    const remove = createElement("button", "secondary-button", `Remove qualification ${number}`);
    remove.type = "button";
    remove.addEventListener("click", () => removeProfileRow(row, "addQualification"));
    row.appendChild(remove);
    document.getElementById("qualificationRows").appendChild(row);
    fields.title.focus();
}

async function loadProfileOptions() {
    const status = document.getElementById("profileOptionsStatus");
    const retry = document.getElementById("retryProfileOptions");
    retry.classList.add("hidden");
    try {
        const response = await window.WiseAPI.fetch(API_URL.replace("personalised-recommendations", "profile-options"));
        if (!response.ok) throw new Error("Choices unavailable");
        const data = await response.json();
        if (!Array.isArray(data.skills) || !Array.isArray(data.qualifications)) throw new Error("Invalid choices");
        qualificationOptions = data.qualifications;
        document.querySelectorAll(".qualification-row select").forEach(populateQualificationSelect);
        const choices = document.getElementById("skillChoices");
        const previousReports = new Map(Array.from(choices.querySelectorAll("[data-skill-id]")).map(input => [input.dataset.skillId, input.value]));
        choices.replaceChildren();
        data.skills.forEach(skill => {
            const label = createElement("label", "", skill.skill_name);
            const select = createElement("select");
            select.id = `skill-${skill.skill_id}`;
            select.dataset.skillId = skill.skill_id;
            label.htmlFor = select.id;
            [["", "Not reported"], ["REPORTED", "I report this skill"], ["DEVELOPMENT_OPPORTUNITY", "I want to develop this skill"]].forEach(([value, text]) => {
                const option = createOption(value);
                option.textContent = text;
                select.appendChild(option);
            });
            select.value = previousReports.get(skill.skill_id) || "";
            choices.append(label, select);
        });
        status.textContent = "Choices loaded from the current knowledge base. You may leave all skills unreported.";
        document.dispatchEvent(new Event("wiselanka:profile-options"));
    } catch {
        status.textContent = "Skill and recorded qualification choices could not be loaded. You can still enter examination results or an award manually; retry to report skills.";
        retry.classList.remove("hidden");
    }
}

function readSubjectResults(subjectIds, gradeIds, missingGrades = []) {
    const results = {};
    const usedSubjects = new Set();

    subjectIds.forEach((subjectId, index) => {
        let subject = document.getElementById(subjectId).value;
        if (subject === "Other subject") {
            subject = document.getElementById(subjectId.replace("olSubject", "olCustom")).value.trim();
            if (!subject) throw new Error("Enter a name for each other O/L subject.");
        }
        const grade = document.getElementById(gradeIds[index]).value;

        if (!grade) {
            missingGrades.push(subject);
        }

        if (usedSubjects.has(subject.trim().toLowerCase())) {
            throw new Error(
                `You selected "${subject}" more than once. ` +
                "Please select different subjects."
            );
        }

        usedSubjects.add(subject.trim().toLowerCase());

        if (grade && grade !== "NOT_REPORTED") {
            if (!GRADES.includes(grade)) throw new Error(`Invalid grade for ${subject}.`);
            results[subject] = grade;
        }
    });

    return results;
}

function collectEducation() {
    const missingGrades = [];
    if (educationLevel.value === "NONE") return {};

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

    const rowNumbers = Array.from(additionalOlSubjects.querySelectorAll("[data-ol-row]")).map(row => row.dataset.olRow);
    const optionalResults = readSubjectResults(
        rowNumbers.map(n => `olSubject${n}`), rowNumbers.map(n => `olGrade${n}`), missingGrades
    );
    if (Object.keys(optionalResults).some(name => ["mathematics", "english"].includes(name.toLowerCase()))) {
        throw new Error("Mathematics or English was selected more than once.");
    }

    if (missingGrades.length > 0) {
        throw new Error(
            "Please select grades for: " +
            missingGrades.join(", ") + "."
        );
    }

    const results = { ...optionalResults };
    if (mathematicsGrade !== "NOT_REPORTED") results.Mathematics = mathematicsGrade;
    if (englishGrade !== "NOT_REPORTED") results.English = englishGrade;
    return { O_LEVEL: results };
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

    const education = collectEducation();
    const qualifications = Array.from(document.querySelectorAll(".qualification-row")).map(row => {
        const award = { qualification_id: row.querySelector("select").value };
        row.querySelectorAll("[data-qualification-field]").forEach(input => { award[input.dataset.qualificationField] = input.value.trim(); });
        if (!award.title) throw new Error("Enter a title for each existing qualification or remove the empty row.");
        return award;
    });
    if (!Object.values(education).some(results => Object.keys(results).length) && !qualifications.length) {
        throw new Error("Provide examination results or add an existing qualification.");
    }
    if (document.getElementById("educationComplete").checked &&
        Object.keys(education).length &&
        (educationLevel.value === "O_LEVEL" ? olSubjects : alSubjects).querySelector('select option[value="NOT_REPORTED"]:checked')) {
        throw new Error("Some results are marked not reported. Uncheck the complete-results confirmation or enter those results.");
    }
    return {
        learner_profile: {
            education,
            learner_category: document.getElementById("learnerCategory").value,
            existing_qualifications: qualifications,
            self_reported_skills: Array.from(document.querySelectorAll("[data-skill-id]")).filter(input => input.value).map(input => ({skill_id: input.dataset.skillId, status: input.value})),
            education_complete: educationLevel.value === "NONE" ? {} : {[educationLevel.value]: document.getElementById("educationComplete").checked},
            interests,
            career_goal_id: document.getElementById("careerGoal").value,
            career_intention: document.getElementById("careerIntention").value.trim(),
            preferences
        }
    };
}

function showStatus(message, isError = false) {
    statusMessage.textContent = message;
    statusMessage.classList.toggle("error", isError);
    statusMessage.classList.remove("hidden");
    if (isError) statusMessage.focus();
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

function appendOfficialLink(card, programme, linkText = "View programme information ↗") {
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
        linkText
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
        if (pathway.source_url) appendOfficialLink(item, {application_url: pathway.source_url}, "Progression source ↗");
        if (pathway.supporting_source_url) appendOfficialLink(item, {application_url: pathway.supporting_source_url}, "Admission process source ↗");
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

function appendAcademicInsights(card, insight) {
    if (!insight) return;
    appendDetail(card, `Academic requirements: ${formatStatus(insight.status)}`, insight.next_step);
    (insight.groups || []).forEach(group => {
        const section = createElement("section", "recommendation-detail academic-gap-group");
        section.appendChild(createElement("strong", "", `${formatStatus(group.status)} — ${group.operator === "OR" ? "one accepted option required" : "all requirements in this group required"}`));
        const list = createElement("ul");
        (group.requirements || []).forEach(requirement => {
            const item = createElement("li", "", `${formatStatus(requirement.status)}: ${requirement.description || "Recorded requirement"}. ${requirement.explanation}`);
            if (requirement.source_url) appendOfficialLink(item, {application_url: requirement.source_url}, `Requirement source${requirement.source_organisation ? " — " + requirement.source_organisation : ""}${requirement.source_accessed ? " (accessed " + requirement.source_accessed + ")" : ""} ↗`);
            list.appendChild(item);
        });
        section.appendChild(list);
        card.appendChild(section);
    });
}

function appendRelevance(card, relevance) {
    if (!relevance) return;
    appendDetail(card, `Relevance method: ${relevance.method}`, relevance.explanation);
    if (relevance.preference_summary) appendDetail(card, "Your stated preference used", relevance.preference_summary);
    if (typeof relevance.score === "number") appendDetail(card, "Content similarity (not a probability)", relevance.score.toFixed(3));
    if (relevance.catalogue_fact) appendDetail(card, "Catalogue facts used for relevance", relevance.catalogue_fact);
}

function renderLearnerInsights(data) {
    const panel = document.getElementById("learnerInsights");
    panel.replaceChildren();
    if (data.ranking) appendDetail(panel, "Recommendation ranking", `${data.ranking.method} — ${data.ranking.status}${data.ranking.fallback_reason ? ": " + data.ranking.fallback_reason : ""}. Academic assessment is independent. Unknown eligibility requires provider review; unmet requirements are development routes, not eligible admissions.`);
    if (Array.isArray(data.existing_qualifications) && data.existing_qualifications.length) {
        appendDetail(panel, "Your reported qualifications", data.existing_qualifications.map(q => [q.title, q.framework, q.level].filter(Boolean).join(" · ")).join("; "));
        appendDetail(panel, "Qualification assessment limits", data.qualification_note);
    }
    (data.held_qualification_progression || []).forEach(progression => {
        appendDetail(panel, "Progression from your reported qualification", progression.qualification_name);
        appendAcademicProgression(panel, {progression});
    });
    const skills = data.learner_skill_insights;
    if (skills) {
        panel.appendChild(createElement("h3", "", "Your skills and development interests"));
        appendDetail(panel, "Self-report comparison", skills.explanation);
        appendDetail(panel, "Knowledge-base evidence limit", skills.evidence_note);
        const labels = {REPORTED: "Reported by you; competence not verified", DEVELOPMENT_OPPORTUNITY: "Development opportunity selected by you", UNREPORTED: "Not reported; not assessed"};
        const list = createElement("ul", "learner-skill-list");
        (skills.career_requirements || []).forEach(skill => {
            list.appendChild(createElement("li", "", `${skill.skill_name}: ${labels[skill.report_status]}. Recorded career level: ${skill.expected_level || "not recorded"}. ${skill.explanation}`));
        });
        panel.appendChild(list);
        const outside = (skills.reported_skills || []).filter(report => !(skills.career_requirements || []).some(skill => skill.skill_id === report.skill_id));
        if (outside.length) appendDetail(panel, "Other self-reports (career relevance not assessed)", outside.map(skill => `${skill.skill_name}: ${labels[skill.report_status]}`).join("; "));
    }
    if (!data.recommendations.length && Array.isArray(data.academic_insights)) {
        data.academic_insights.forEach(insight => {
            const card = createElement("article", "recommendation-card");
            card.appendChild(createElement("h3", "", insight.programme_name));
            appendRelevance(card, insight.relevance);
            appendAcademicInsights(card, insight);
            panel.appendChild(card);
        });
    }
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
    const category = programme.relevance && programme.academic_gap_insights
        ? ({MET: "ELIGIBLE", NOT_ASSESSED: "NOT_ASSESSED", NOT_MET: "NOT_MET"}[programme.academic_gap_insights.status] || "NOT_ASSESSED")
        : programme.academic_gap_insights?.status === "NOT_ASSESSED" ? "NOT_ASSESSED" : programme.category || "NOT_ASSESSED";

    metadata.appendChild(
        createElement(
            "span",
            `result-tag ${category.toLowerCase().replaceAll("_", "-")}`,
            `Academic eligibility: ${formatStatus(category)}`
        )
    );

    if (category !== "NOT_ASSESSED" && typeof programme.academic_match_score === "number") {
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

    appendRelevance(card, programme.relevance);
    appendDetail(card, "Programme context", programme.programme_notes);
    appendAcademicProgression(card, programme);
    if (programme.academic_gap_insights) appendAcademicInsights(card, programme.academic_gap_insights);
    else appendEvidence(card, programme);
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
    renderLearnerInsights(data);

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
    document.getElementById("learnerInsights").replaceChildren();
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
    document.querySelector('.results-panel').setAttribute('aria-busy', 'true');
    showStatus("Evaluating your learner profile...");

    try {
        const response = await window.WiseAPI.fetch(API_URL, {
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
                : Array.isArray(data.detail)
                    ? data.detail.map(error => `${(error.loc || []).slice(1).join(" / ")}: ${error.msg}`).join("; ")
                    : "The API could not process this profile.";

            throw new Error(detail);
        }

        renderRecommendations(data);
        const resultHeading = document.getElementById('resultsHeading');
        resultHeading.setAttribute('tabindex', '-1');
        resultHeading.focus();
    } catch (error) {
        const message = error instanceof TypeError
            ? "Could not connect to the WiseLanka API. " +
              "Make sure the backend is running on port 8000."
            : error.message;

        showStatus(message, true);
    } finally {
        submitButton.disabled = false;
        document.querySelector('.results-panel').setAttribute('aria-busy', 'false');
    }
}

["olMathematics", "olEnglish", "alGrade1", "alGrade2", "alGrade3"].forEach(id => {
    const option = createOption("NOT_REPORTED");
    option.textContent = "Not reported";
    document.getElementById(id).appendChild(option);
});
document.querySelectorAll(".al-subject").forEach(select => {
    ["Business Studies", "Accounting", "Economics", "Engineering Technology", "Science for Technology"].forEach(subject => {
        select.appendChild(createOption(subject));
    });
});
createOlSubjects();
// Landing cards set context only; grades and qualification evidence remain user supplied.
const landingParameters = new URLSearchParams(window.location.search);
const landingJourneys = {
    ordinary: {education: "O_LEVEL", category: "AL_LEARNER"},
    advanced: {education: "A_LEVEL", category: "AL_LEARNER"},
    vocational: {education: "NONE", category: "VOCATIONAL_LEARNER"},
    diploma: {education: "NONE", category: "EARLY_CAREER"}
};
const landingJourney = landingJourneys[landingParameters.get("journey")];
if (landingJourney) {
    educationLevel.value = landingJourney.education;
    document.getElementById("learnerCategory").value = landingJourney.category;
}
const requestedLanguage = landingParameters.get("lang");
if (["en", "si", "ta"].includes(requestedLanguage)) {
    document.getElementById("interfaceLanguage").value = requestedLanguage;
    window.WiseI18n.setLanguage(requestedLanguage);
}
updateEducationLevel();
document.getElementById("addOlSubject").addEventListener("click", () => {
    addOlSubject();
    document.getElementById(`olSubject${olSubjectCount}`).focus();
});
document.getElementById("addQualification").addEventListener("click", addQualification);
document.getElementById("retryProfileOptions").addEventListener("click", loadProfileOptions);
loadProfileOptions();

educationLevel.addEventListener(
    "change",
    updateEducationLevel
);

form.addEventListener(
    "submit",
    submitLearnerProfile
);
