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


// ------------------------------------
// Collect student results
// ------------------------------------

function collectStudentResults() {

    const studentResults = {};

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

            studentResults[
                subject
            ] = grade;
        }
    }

    return studentResults;
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
        !messages
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


// ------------------------------------
// Create programme recommendation card
// ------------------------------------

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
        recommendation.programme_id;


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
// Display recommendations
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


    emptyResult.classList.add(
        "hidden"
    );


    recommendationResults
        .classList.remove(
            "hidden"
        );
}


// ------------------------------------
// Fetch recommendations from API
// ------------------------------------

async function fetchRecommendations() {

    const studentResults =
        collectStudentResults();


    if (
        Object.keys(
            studentResults
        ).length === 0
    ) {

        alert(
            "Please enter your A/L results."
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
// Event listener
// ------------------------------------

recommendButton.addEventListener(
    "click",
    fetchRecommendations
);