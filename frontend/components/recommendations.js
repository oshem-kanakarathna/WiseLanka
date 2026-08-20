const API_URL =
    "http://127.0.0.1:8000/recommendations";


const recommendButton =
    document.getElementById(
        "recommendButton"
    );


const emptyResult =
    document.getElementById(
        "emptyResult"
    );


const recommendationResults =
    document.getElementById(
        "recommendationResults"
    );


const recommendationList =
    document.getElementById(
        "recommendationList"
    );


const resultCount =
    document.getElementById(
        "resultCount"
    );


// ====================================
// Education Level Selection
// ====================================

let selectedEducationLevel =
    "A_LEVEL";


const alLevelButton =
    document.getElementById(
        "alLevelButton"
    );


const olLevelButton =
    document.getElementById(
        "olLevelButton"
    );


const alResultsForm =
    document.getElementById(
        "alResultsForm"
    );


const olResultsForm =
    document.getElementById(
        "olResultsForm"
    );


const inputDescription =
    document.getElementById(
        "inputDescription"
    );


// ------------------------------------
// Change active education level
// ------------------------------------

function setEducationLevel(
    level
) {

    selectedEducationLevel =
        level;


    const isAL =
        level === "A_LEVEL";


    if (
        alLevelButton
    ) {

        alLevelButton.classList.toggle(
            "active",
            isAL
        );


        alLevelButton.setAttribute(
            "aria-pressed",
            String(isAL)
        );
    }


    if (
        olLevelButton
    ) {

        olLevelButton.classList.toggle(
            "active",
            !isAL
        );


        olLevelButton.setAttribute(
            "aria-pressed",
            String(!isAL)
        );
    }


    if (
        alResultsForm
    ) {

        alResultsForm.classList.toggle(
            "hidden",
            !isAL
        );
    }


    if (
        olResultsForm
    ) {

        olResultsForm.classList.toggle(
            "hidden",
            isAL
        );
    }


    if (
        inputDescription
    ) {

        if (isAL) {

            inputDescription.textContent =
                (
                    "Add three GCE A/L "
                    + "subjects and grades."
                );

        } else {

            inputDescription.textContent =
                (
                    "Add six GCE O/L "
                    + "subjects and grades."
                );
        }
    }


    // Clear old results when the user
    // changes education level.

    recommendationList.innerHTML =
        "";


    recommendationResults
        .classList.add(
            "hidden"
        );


    emptyResult
        .classList.remove(
            "hidden"
        );
}


// ------------------------------------
// Education-level switch events
// ------------------------------------

if (
    alLevelButton
) {

    alLevelButton.addEventListener(
        "click",
        () => {

            setEducationLevel(
                "A_LEVEL"
            );
        }
    );
}


if (
    olLevelButton
) {

    olLevelButton.addEventListener(
        "click",
        () => {

            setEducationLevel(
                "O_LEVEL"
            );
        }
    );
}


// ====================================
// Collect Student Results
// ====================================

function collectStudentResults() {

    // --------------------------------
    // A/L results
    // --------------------------------

    if (
        selectedEducationLevel
        === "A_LEVEL"
    ) {

        const alResults = {};


        for (
            let index = 1;
            index <= 3;
            index++
        ) {

            const subjectElement =
                document.getElementById(
                    `subject${index}`
                );


            const gradeElement =
                document.getElementById(
                    `grade${index}`
                );


            if (
                !subjectElement
                || !gradeElement
            ) {
                continue;
            }


            const subject =
                subjectElement.value;


            const grade =
                gradeElement.value;


            if (
                subject
                && grade
            ) {

                alResults[
                    subject
                ] = grade;
            }
        }


        return {
            "A_LEVEL":
                alResults,
        };
    }


    // --------------------------------
    // O/L results
    // --------------------------------

    const olResults = {};


    const mathematics =
        document.getElementById(
            "olMathematics"
        );


    const english =
        document.getElementById(
            "olEnglish"
        );


    if (
        mathematics
    ) {

        olResults[
            "Mathematics"
        ] = mathematics.value;
    }


    if (
        english
    ) {

        olResults[
            "English"
        ] = english.value;
    }


    for (
        let index = 3;
        index <= 6;
        index++
    ) {

        const subjectElement =
            document.getElementById(
                `olSubject${index}`
            );


        const gradeElement =
            document.getElementById(
                `olGrade${index}`
            );


        if (
            !subjectElement
            || !gradeElement
        ) {
            continue;
        }


        const subject =
            subjectElement.value;


        const grade =
            gradeElement.value;


        if (
            subject
            && grade
        ) {

            olResults[
                subject
            ] = grade;
        }
    }


    return {
        "O_LEVEL":
            olResults,
    };
}


// ====================================
// Validate Student Results
// ====================================

function validateStudentResults(
    studentResults
) {

    if (
        !studentResults
        || typeof studentResults
            !== "object"
    ) {

        return {
            valid: false,
            message:
                "Please enter your academic results.",
        };
    }


    const levelResults =
        studentResults[
            selectedEducationLevel
        ];


    if (
        !levelResults
        || typeof levelResults
            !== "object"
    ) {

        return {
            valid: false,
            message:
                "Please enter your academic results.",
        };
    }


    const subjects =
        Object.keys(
            levelResults
        );


    // --------------------------------
    // A/L validation
    // --------------------------------

    if (
        selectedEducationLevel
        === "A_LEVEL"
    ) {

        if (
            subjects.length !== 3
        ) {

            return {
                valid: false,
                message:
                    (
                        "Please select three "
                        + "different A/L subjects."
                    ),
            };
        }


        return {
            valid: true,
            message: "",
        };
    }


    // --------------------------------
    // O/L validation
    // --------------------------------

    if (
        subjects.length !== 6
    ) {

        return {
            valid: false,
            message:
                (
                    "Please select six "
                    + "different O/L subjects."
                ),
        };
    }


    if (
        !Object.prototype
            .hasOwnProperty.call(
                levelResults,
                "Mathematics"
            )
    ) {

        return {
            valid: false,
            message:
                (
                    "Mathematics is required "
                    + "for the O/L profile."
                ),
        };
    }


    if (
        !Object.prototype
            .hasOwnProperty.call(
                levelResults,
                "English"
            )
    ) {

        return {
            valid: false,
            message:
                (
                    "English is required "
                    + "for the O/L profile."
                ),
        };
    }


    return {
        valid: true,
        message: "",
    };
}


// ------------------------------------
// Recommendation category helpers
// ------------------------------------

function getCategoryLabel(
    category
) {

    if (
        category
        === "ELIGIBLE"
    ) {
        return "Eligible";
    }


    if (
        category
        === "NEARLY_ELIGIBLE"
    ) {
        return "Nearly Eligible";
    }


    return "Not Eligible";
}


function getCategoryClass(
    category
) {

    if (
        category
        === "ELIGIBLE"
    ) {
        return "status-success";
    }


    if (
        category
        === "NEARLY_ELIGIBLE"
    ) {
        return "status-warning";
    }


    return "status-fail";
}


// ------------------------------------
// Requirement explanation section
// ------------------------------------

function createRequirementList(
    title,
    messages,
    className
) {

    if (
        !Array.isArray(
            messages
        )
        || messages.length === 0
    ) {
        return null;
    }


    const section =
        document.createElement(
            "div"
        );


    section.className =
        "requirement-section";


    const heading =
        document.createElement(
            "h5"
        );


    heading.textContent =
        title;


    section.appendChild(
        heading
    );


    const list =
        document.createElement(
            "ul"
        );


    list.className =
        className;


    for (
        const message
        of messages
    ) {

        const item =
            document.createElement(
                "li"
            );


        item.textContent =
            message;


        list.appendChild(
            item
        );
    }


    section.appendChild(
        list
    );


    return section;
}


// ====================================
// Career Pathway Intelligence
// ====================================


// ------------------------------------
// Career relevance helpers
// ------------------------------------

function getCareerRelevanceClass(
    relevanceLevel
) {

    const normalized =
        (
            relevanceLevel
            || "Unknown"
        )
        .trim()
        .toLowerCase();


    if (
        normalized === "high"
    ) {
        return "career-relevance-high";
    }


    if (
        normalized === "medium"
    ) {
        return "career-relevance-medium";
    }


    if (
        normalized === "low"
    ) {
        return "career-relevance-low";
    }


    return "career-relevance-unknown";
}


// ------------------------------------
// Create career indicator
// ------------------------------------

function createCareerIndicator(
    label,
    value
) {

    const indicator =
        document.createElement(
            "span"
        );


    indicator.className =
        "career-indicator";


    const indicatorLabel =
        document.createElement(
            "span"
        );


    indicatorLabel.className =
        "career-indicator-label";


    indicatorLabel.textContent =
        `${label}: `;


    const indicatorValue =
        document.createElement(
            "strong"
        );


    indicatorValue.textContent =
        value || "Unknown";


    indicator.appendChild(
        indicatorLabel
    );


    indicator.appendChild(
        indicatorValue
    );


    return indicator;
}


// ------------------------------------
// Career pathway section
// ------------------------------------

function createCareerPathways(
    careers
) {

    if (
        !Array.isArray(
            careers
        )
        || careers.length === 0
    ) {
        return null;
    }


    const section =
        document.createElement(
            "section"
        );


    section.className =
        "career-section";


    const sectionHeader =
        document.createElement(
            "div"
        );


    sectionHeader.className =
        "career-section-heading";


    const headingContent =
        document.createElement(
            "div"
        );


    const heading =
        document.createElement(
            "h5"
        );


    heading.textContent =
        "Career Pathways";


    const subtitle =
        document.createElement(
            "p"
        );


    subtitle.textContent =
        (
            "Potential careers connected "
            + "to this programme."
        );


    headingContent.appendChild(
        heading
    );


    headingContent.appendChild(
        subtitle
    );


    sectionHeader.appendChild(
        headingContent
    );


    const careerCount =
        document.createElement(
            "span"
        );


    careerCount.className =
        "career-count";


    careerCount.textContent =
        (
            careers.length === 1
                ? "1 career"
                : `${careers.length} careers`
        );


    sectionHeader.appendChild(
        careerCount
    );


    section.appendChild(
        sectionHeader
    );


    const careerList =
        document.createElement(
            "div"
        );


    careerList.className =
        "career-list";


    for (
        const career
        of careers
    ) {

        const careerCard =
            document.createElement(
                "article"
            );


        careerCard.className =
            "career-item";


        const careerTop =
            document.createElement(
                "div"
            );


        careerTop.className =
            "career-item-top";


        const careerName =
            document.createElement(
                "strong"
            );


        careerName.className =
            "career-name";


        careerName.textContent =
            (
                career.career_name
                || "Career pathway"
            );


        const relevanceLevel =
            (
                career.relevance_level
                || "Unknown"
            );


        const relevance =
            document.createElement(
                "span"
            );


        relevance.className =
            (
                "career-relevance "
                + getCareerRelevanceClass(
                    relevanceLevel
                )
            );


        relevance.textContent =
            `${relevanceLevel} relevance`;


        careerTop.appendChild(
            careerName
        );


        careerTop.appendChild(
            relevance
        );


        careerCard.appendChild(
            careerTop
        );


        if (
            career.description
        ) {

            const description =
                document.createElement(
                    "p"
                );


            description.className =
                "career-description";


            description.textContent =
                career.description;


            careerCard.appendChild(
                description
            );
        }


        const indicators =
            document.createElement(
                "div"
            );


        indicators.className =
            "career-indicators";


        indicators.appendChild(
            createCareerIndicator(
                "Sri Lanka demand",
                career.sri_lanka_demand
            )
        );


        indicators.appendChild(
            createCareerIndicator(
                "International",
                career
                    .international_potential
            )
        );


        indicators.appendChild(
            createCareerIndicator(
                "Remote potential",
                career
                    .remote_work_potential
            )
        );


        careerCard.appendChild(
            indicators
        );


        if (
            career.relationship_notes
        ) {

            const relationshipNote =
                document.createElement(
                    "p"
                );


            relationshipNote.className =
                "career-relationship-note";


            relationshipNote.textContent =
                career.relationship_notes;


            careerCard.appendChild(
                relationshipNote
            );
        }


        careerList.appendChild(
            careerCard
        );
    }


    section.appendChild(
        careerList
    );


    return section;
}


// ====================================
// Qualification Progression Intelligence
// ====================================


// ------------------------------------
// Progression type helper
// ------------------------------------

function getProgressionTypeClass(
    progressionType
) {

    const normalized =
        (
            progressionType
            || ""
        )
        .trim()
        .toLowerCase();


    if (
        normalized.includes(
            "conditional"
        )
    ) {
        return "progression-type-conditional";
    }


    return "progression-type-direct";
}


// ------------------------------------
// Create one destination programme
// ------------------------------------

function createProgressionProgramme(
    programme
) {

    const wrapper =
        document.createElement(
            "div"
        );


    wrapper.className =
        "progression-programme";


    const provider =
        document.createElement(
            "p"
        );


    provider.className =
        "progression-provider";


    provider.textContent =
        (
            "Delivered by "
            + (
                programme.provider_name
                || "provider not recorded"
            )
        );


    wrapper.appendChild(
        provider
    );


    if (
        programme.awarding_body_name
    ) {

        const awardingBody =
            document.createElement(
                "p"
            );


        awardingBody.className =
            "progression-awarding-body";


        awardingBody.textContent =
            (
                "Awarded by "
                + programme
                    .awarding_body_name
            );


        wrapper.appendChild(
            awardingBody
        );
    }


    const metadata =
        document.createElement(
            "div"
        );


    metadata.className =
        "progression-programme-meta";


    if (
        programme.duration_months
    ) {

        const duration =
            document.createElement(
                "span"
            );


        duration.textContent =
            (
                `${programme.duration_months}`
                + " months"
            );


        metadata.appendChild(
            duration
        );
    }


    if (
        programme.study_mode
    ) {

        const studyMode =
            document.createElement(
                "span"
            );


        studyMode.textContent =
            programme.study_mode;


        metadata.appendChild(
            studyMode
        );
    }


    if (
        programme.delivery_mode
    ) {

        const deliveryMode =
            document.createElement(
                "span"
            );


        deliveryMode.textContent =
            programme.delivery_mode;


        metadata.appendChild(
            deliveryMode
        );
    }


    if (
        metadata.children.length > 0
    ) {

        wrapper.appendChild(
            metadata
        );
    }


    if (
        programme.application_url
    ) {

        const applicationLink =
            document.createElement(
                "a"
            );


        applicationLink.className =
            "progression-link";


        applicationLink.href =
            programme.application_url;


        applicationLink.target =
            "_blank";


        applicationLink.rel =
            "noopener noreferrer";


        applicationLink.textContent =
            "View programme details →";


        wrapper.appendChild(
            applicationLink
        );
    }


    return wrapper;
}


// ------------------------------------
// Create one progression pathway
// ------------------------------------

function createProgressionPathway(
    pathway
) {

    const item =
        document.createElement(
            "article"
        );


    item.className =
        "progression-item";


    const top =
        document.createElement(
            "div"
        );


    top.className =
        "progression-item-top";


    const titleArea =
        document.createElement(
            "div"
        );


    titleArea.className =
        "progression-title-area";


    const pathwayIcon =
        document.createElement(
            "div"
        );


    pathwayIcon.className =
        "progression-icon";


    pathwayIcon.textContent =
        "→";


    const nameArea =
        document.createElement(
            "div"
        );


    const name =
        document.createElement(
            "strong"
        );


    name.className =
        "progression-name";


    name.textContent =
        (
            pathway.qualification_name
            || pathway
                .to_qualification_id
            || "Progression pathway"
        );


    nameArea.appendChild(
        name
    );


    if (
        pathway.to_qualification_id
    ) {

        const qualificationId =
            document.createElement(
                "span"
            );


        qualificationId.className =
            "progression-qualification-id";


        qualificationId.textContent =
            pathway.to_qualification_id;


        nameArea.appendChild(
            qualificationId
        );
    }


    titleArea.appendChild(
        pathwayIcon
    );


    titleArea.appendChild(
        nameArea
    );


    const type =
        document.createElement(
            "span"
        );


    type.className =
        (
            "progression-type "
            + getProgressionTypeClass(
                pathway.progression_type
            )
        );


    type.textContent =
        (
            pathway.progression_type
            || "Academic Progression"
        );


    top.appendChild(
        titleArea
    );


    top.appendChild(
        type
    );


    item.appendChild(
        top
    );


    if (
        pathway.conditions
    ) {

        const conditions =
            document.createElement(
                "div"
            );


        const isConditional =
            (
                pathway.progression_type
                && pathway
                    .progression_type
                    .toLowerCase()
                    .includes(
                        "conditional"
                    )
            );


        conditions.className =
            (
                isConditional
                    ? (
                        "progression-condition "
                        + "progression-condition-warning"
                    )
                    : "progression-condition"
            );


        const conditionLabel =
            document.createElement(
                "strong"
            );


        conditionLabel.textContent =
            (
                isConditional
                    ? "Additional condition: "
                    : "Progression requirement: "
            );


        conditions.appendChild(
            conditionLabel
        );


        conditions.appendChild(
            document.createTextNode(
                pathway.conditions
            )
        );


        item.appendChild(
            conditions
        );
    }


    if (
        Array.isArray(
            pathway.programmes
        )
    ) {

        for (
            const programme
            of pathway.programmes
        ) {

            const programmeBlock =
                createProgressionProgramme(
                    programme
                );


            item.appendChild(
                programmeBlock
            );
        }
    }


    return item;
}


// ------------------------------------
// Full progression section
// ------------------------------------

function createProgressionSection(
    progression
) {

    if (
        !progression
        || !Array.isArray(
            progression.pathways
        )
        || progression.pathways.length === 0
    ) {
        return null;
    }


    const section =
        document.createElement(
            "section"
        );


    section.className =
        "progression-section";


    const header =
        document.createElement(
            "div"
        );


    header.className =
        "progression-section-heading";


    const headingContent =
        document.createElement(
            "div"
        );


    const heading =
        document.createElement(
            "h5"
        );


    heading.textContent =
        "Where This Pathway Can Lead";


    const subtitle =
        document.createElement(
            "p"
        );


    subtitle.textContent =
        (
            "Verified academic progression "
            + "options available after "
            + "successfully completing "
            + "this qualification."
        );


    headingContent.appendChild(
        heading
    );


    headingContent.appendChild(
        subtitle
    );


    header.appendChild(
        headingContent
    );


    const count =
        document.createElement(
            "span"
        );


    count.className =
        "progression-count";


    count.textContent =
        (
            progression.pathways.length
            === 1
                ? "1 pathway"
                : (
                    `${progression.pathways.length}`
                    + " pathways"
                )
        );


    header.appendChild(
        count
    );


    section.appendChild(
        header
    );


    const source =
        document.createElement(
            "div"
        );


    source.className =
        "progression-source";


    const sourceLabel =
        document.createElement(
            "span"
        );


    sourceLabel.textContent =
        "From";


    const sourceName =
        document.createElement(
            "strong"
        );


    sourceName.textContent =
        (
            progression.qualification_name
            || progression.qualification_id
            || "Current qualification"
        );


    source.appendChild(
        sourceLabel
    );


    source.appendChild(
        sourceName
    );


    section.appendChild(
        source
    );


    const list =
        document.createElement(
            "div"
        );


    list.className =
        "progression-list";


    for (
        const pathway
        of progression.pathways
    ) {

        list.appendChild(
            createProgressionPathway(
                pathway
            )
        );
    }


    section.appendChild(
        list
    );


    const disclaimer =
        document.createElement(
            "p"
        );


    disclaimer.className =
        "progression-disclaimer";


    disclaimer.textContent =
        (
            "Progression information is "
            + "guidance based on recorded "
            + "academic pathways. Final "
            + "admission remains subject "
            + "to the institution's current "
            + "requirements."
        );


    section.appendChild(
        disclaimer
    );


    return section;
}


// ====================================
// Recommendation Card
// ====================================

function createRecommendationCard(
    recommendation,
    position
) {

    const card =
        document.createElement(
            "article"
        );


    card.className =
        "recommendation-card";


    const topRow =
        document.createElement(
            "div"
        );


    topRow.className =
        "recommendation-top";


    const rank =
        document.createElement(
            "div"
        );


    rank.className =
        "rank-number";


    rank.textContent =
        `#${position}`;


    const status =
        document.createElement(
            "span"
        );


    status.className =
        (
            "status-badge "
            + getCategoryClass(
                recommendation.category
            )
        );


    status.textContent =
        getCategoryLabel(
            recommendation.category
        );


    topRow.appendChild(
        rank
    );


    topRow.appendChild(
        status
    );


    card.appendChild(
        topRow
    );


    const title =
        document.createElement(
            "h4"
        );


    title.textContent =
        (
            recommendation.programme_name
            || recommendation.programme_id
        );


    card.appendChild(
        title
    );


    const meta =
        document.createElement(
            "div"
        );


    meta.className =
        "recommendation-meta";


    const programmeId =
        document.createElement(
            "span"
        );


    programmeId.textContent =
        (
            recommendation
                .qualification_id
                ? (
                    recommendation.programme_id
                    + " · "
                    + recommendation
                        .qualification_id
                )
                : recommendation
                    .programme_id
        );


    const score =
        document.createElement(
            "strong"
        );


    const matchScore =
        Number(
            recommendation.match_score
            || 0
        );


    score.textContent =
        `${matchScore}% match`;


    meta.appendChild(
        programmeId
    );


    meta.appendChild(
        score
    );


    card.appendChild(
        meta
    );


    const progressTrack =
        document.createElement(
            "div"
        );


    progressTrack.className =
        "progress-track";


    const progressBar =
        document.createElement(
            "div"
        );


    progressBar.className =
        "progress-bar";


    progressBar.style.width =
        (
            `${Math.min(
                Math.max(
                    matchScore,
                    0
                ),
                100
            )}%`
        );


    progressTrack.appendChild(
        progressBar
    );


    card.appendChild(
        progressTrack
    );


    const passedSection =
        createRequirementList(
            "Requirements currently satisfied",
            recommendation
                .passed_requirements,
            "passed-list"
        );


    if (
        passedSection
    ) {

        card.appendChild(
            passedSection
        );
    }


    const failedSection =
        createRequirementList(
            recommendation.category
                === "NEARLY_ELIGIBLE"
                ? "What is still needed"
                : "Requirements not satisfied",
            recommendation
                .failed_requirements,
            "failed-list"
        );


    if (
        failedSection
    ) {

        card.appendChild(
            failedSection
        );
    }


    // --------------------------------
    // Academic progression
    // --------------------------------

    const progressionSection =
        createProgressionSection(
            recommendation.progression
        );


    if (
        progressionSection
    ) {

        card.appendChild(
            progressionSection
        );
    }


    // --------------------------------
    // Career pathways
    // --------------------------------

    const careerSection =
        createCareerPathways(
            recommendation
                .career_pathways
        );


    if (
        careerSection
    ) {

        card.appendChild(
            careerSection
        );
    }


    return card;
}


// ------------------------------------
// Display Recommendations
// ------------------------------------

function displayRecommendations(
    data
) {

    recommendationList.innerHTML =
        "";


    const recommendations =
        (
            data.recommendations
            || []
        );


    resultCount.textContent =
        (
            recommendations.length === 1
                ? "1 programme"
                : `${recommendations.length} programmes`
        );


    if (
        recommendations.length === 0
    ) {

        recommendationResults
            .classList.add(
                "hidden"
            );


        emptyResult
            .classList.remove(
                "hidden"
            );


        return;
    }


    recommendations.forEach(
        (
            recommendation,
            index
        ) => {

            const card =
                createRecommendationCard(
                    recommendation,
                    index + 1
                );


            recommendationList
                .appendChild(
                    card
                );
        }
    );


    emptyResult
        .classList.add(
            "hidden"
        );


    recommendationResults
        .classList.remove(
            "hidden"
        );
}


// ------------------------------------
// Fetch Recommendations from API
// ------------------------------------

async function fetchRecommendations() {

    const studentResults =
        collectStudentResults();


    const validation =
        validateStudentResults(
            studentResults
        );


    if (
        !validation.valid
    ) {

        alert(
            validation.message
        );

        return;
    }


    const payload = {
        student_results:
            studentResults,
    };


    recommendButton.disabled =
        true;


    recommendButton.textContent =
        "Finding pathways...";


    try {

        const response =
            await fetch(
                API_URL,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json",
                    },

                    body:
                        JSON.stringify(
                            payload
                        ),
                }
            );


        if (
            !response.ok
        ) {

            throw new Error(
                (
                    "WiseLanka API returned "
                    + response.status
                )
            );
        }


        const data =
            await response.json();


        displayRecommendations(
            data
        );

    } catch (
        error
    ) {

        console.error(
            error
        );


        alert(
            (
                "Could not connect to the "
                + "WiseLanka backend.\n\n"
                + "Make sure the FastAPI "
                + "server is running on "
                + "port 8000."
            )
        );

    } finally {

        recommendButton.disabled =
            false;


        recommendButton.textContent =
            "Find My Pathways";
    }
}


// ------------------------------------
// Main action button
// ------------------------------------

recommendButton.addEventListener(
    "click",
    fetchRecommendations
);


// ------------------------------------
// Initialize interface
// ------------------------------------

setEducationLevel(
    "A_LEVEL"
);