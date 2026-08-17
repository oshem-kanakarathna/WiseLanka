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


function collectStudentResults() {

    const studentResults = {};

    for (
        let index = 1;
        index <= 3;
        index++
    ) {

        const subject =
            document.getElementById(
                `subject${index}`
            ).value;


        const grade =
            document.getElementById(
                `grade${index}`
            ).value;


        studentResults[
            subject
        ] = grade;
    }

    return studentResults;
}


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
        recommendation.programme_name;


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


    score.textContent =
        (
            `${recommendation.match_score}% match`
        );


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
                    recommendation.match_score,
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


    if (passedSection) {

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


    if (failedSection) {

        card.appendChild(
            failedSection
        );
    }


    return card;
}


function displayRecommendations(
    data
) {

    recommendationList.innerHTML =
        "";


    const recommendations =
        data.recommendations || [];


    resultCount.textContent =
        (
            `${recommendations.length} programmes`
        );


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


async function fetchRecommendations() {

    const studentResults =
        collectStudentResults();


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


        if (!response.ok) {

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

    } catch (error) {

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


recommendButton.addEventListener(
    "click",
    fetchRecommendations
);