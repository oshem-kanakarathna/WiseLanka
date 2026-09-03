const API_URL =
    "http://127.0.0.1:8000/recommendations";

const ALTERNATIVE_PATHWAYS_API_URL =
    "http://127.0.0.1:8000/alternative-pathways";

const SKILLS_API_URL =
    "http://127.0.0.1:8000/skills/alignment";

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
// Alternative Pathway DOM Elements
// ====================================

const targetProgramme =
    document.getElementById(
        "targetProgramme"
    );


const targetProgrammeSection =
    document.querySelector(
        ".target-programme-section"
    );


const alternativePathwayResults =
    document.getElementById(
        "alternativePathwayResults"
    );


const alternativePathwayStatus =
    document.getElementById(
        "alternativePathwayStatus"
    );


const alternativePathwayList =
    document.getElementById(
        "alternativePathwayList"
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


// ====================================
// Alternative Pathway Reset
// ====================================

function hideAlternativePathways() {

    if (
        alternativePathwayList
    ) {

        alternativePathwayList.innerHTML =
            "";
    }


    if (
        alternativePathwayStatus
    ) {

        alternativePathwayStatus.textContent =
            "";
    }


    if (
        alternativePathwayResults
    ) {

        alternativePathwayResults
            .classList.add(
                "hidden"
            );
    }
}


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
        targetProgrammeSection
    ) {

        targetProgrammeSection
            .classList.toggle(
                "hidden",
                isAL
            );
    }


    if (
        isAL
        && targetProgramme
    ) {

        targetProgramme.value =
            "";
    }


    if (
        inputDescription
    ) {

        if (
            isAL
        ) {

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


    hideAlternativePathways();
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


// ====================================
// Recommendation Category Helpers
// ====================================

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


// ====================================
// Requirement Explanation
// ====================================

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

// ====================================
// Skills Intelligence
// ====================================

async function fetchSkillAlignment(
    programmeId,
    careerId
) {

    const response =
        await fetch(
            (
                SKILLS_API_URL
                + "/"
                + encodeURIComponent(
                    programmeId
                )
                + "/"
                + encodeURIComponent(
                    careerId
                )
            )
        );


    if (
        !response.ok
    ) {

        throw new Error(
            (
                "Skills API returned "
                + response.status
            )
        );
    }


    return await response.json();
}


// ====================================
// Create Skill Alignment Result
// ====================================

function createSkillAlignmentContent(
    alignment
) {

    const wrapper =
        document.createElement(
            "div"
        );


    wrapper.className =
        "skill-alignment-content";


    if (
        !alignment
        || alignment.status
            !== "AVAILABLE"
    ) {

        const unavailable =
            document.createElement(
                "p"
            );


        unavailable.className =
            "skill-alignment-unavailable";


        unavailable.textContent =
            (
                "Skill alignment data is "
                + "not currently available "
                + "for this programme and "
                + "career combination."
            );


        wrapper.appendChild(
            unavailable
        );


        return wrapper;
    }


    // --------------------------------
    // Alignment heading
    // --------------------------------

    const header =
        document.createElement(
            "div"
        );


    header.className =
        "skill-alignment-header";


    const headerText =
        document.createElement(
            "div"
        );


    const title =
        document.createElement(
            "strong"
        );


    title.className =
        "skill-alignment-title";


    title.textContent =
        "Programme–Career Skill Alignment";


    const subtitle =
        document.createElement(
            "p"
        );


    subtitle.textContent =
        (
            "How strongly the recorded "
            + "programme skills overlap "
            + "with this career model."
        );


    headerText.appendChild(
        title
    );


    headerText.appendChild(
        subtitle
    );


    const percentage =
        document.createElement(
            "span"
        );


    percentage.className =
        "skill-alignment-percentage";


    percentage.textContent =
        (
            alignment
                .alignment_percentage
            + "%"
        );


    header.appendChild(
        headerText
    );


    header.appendChild(
        percentage
    );


    wrapper.appendChild(
        header
    );


    // --------------------------------
    // Alignment progress bar
    // --------------------------------

    const progressTrack =
        document.createElement(
            "div"
        );


    progressTrack.className =
        "skill-alignment-track";


    const progressBar =
        document.createElement(
            "div"
        );


    progressBar.className =
        "skill-alignment-bar";


    const alignmentPercentage =
        Number(
            alignment
                .alignment_percentage
            || 0
        );


    progressBar.style.width =
        (
            Math.min(
                Math.max(
                    alignmentPercentage,
                    0
                ),
                100
            )
            + "%"
        );


    progressTrack.appendChild(
        progressBar
    );


    wrapper.appendChild(
        progressTrack
    );


    // --------------------------------
    // Alignment summary
    // --------------------------------

    const summary =
        document.createElement(
            "p"
        );


    summary.className =
        "skill-alignment-summary";


    summary.textContent =
        (
            alignment.shared_skill_count
            + " of "
            + alignment.career_skill_count
            + " career skills recorded "
            + "in WiseLanka are represented "
            + "by this programme."
        );


    wrapper.appendChild(
        summary
    );


    // --------------------------------
    // Shared skills
    // --------------------------------

    const sharedSkills =
        alignment.shared_skills
        || [];


    if (
        sharedSkills.length > 0
    ) {

        const sharedSection =
            document.createElement(
                "div"
            );


        sharedSection.className =
            "skill-alignment-group";


        const sharedTitle =
            document.createElement(
                "strong"
            );


        sharedTitle.className =
            "skill-alignment-group-title";


        sharedTitle.textContent =
            "Represented by programme";


        sharedSection.appendChild(
            sharedTitle
        );


        const sharedList =
            document.createElement(
                "ul"
            );


        sharedList.className =
            (
                "skill-alignment-list "
                + "skill-alignment-shared"
            );


        sharedSkills.forEach(
            skill => {

                const item =
                    document.createElement(
                        "li"
                    );


                const icon =
                    document.createElement(
                        "span"
                    );


                icon.className =
                    "skill-alignment-icon";


                icon.textContent =
                    "✓";


                const skillName =
                    document.createElement(
                        "span"
                    );


                skillName.textContent =
                    (
                        skill.skill_name
                        || skill.skill_id
                        || "Recorded skill"
                    );


                item.appendChild(
                    icon
                );


                item.appendChild(
                    skillName
                );


                sharedList.appendChild(
                    item
                );
            }
        );


        sharedSection.appendChild(
            sharedList
        );


        wrapper.appendChild(
            sharedSection
        );
    }


    // --------------------------------
    // Additional career skills
    // --------------------------------

    const additionalSkills =
        (
            alignment
                .additional_career_skills
            || []
        );


    if (
        additionalSkills.length > 0
    ) {

        const additionalSection =
            document.createElement(
                "div"
            );


        additionalSection.className =
            "skill-alignment-group";


        const additionalTitle =
            document.createElement(
                "strong"
            );


        additionalTitle.className =
            "skill-alignment-group-title";


        additionalTitle.textContent =
            "Additional career skills";


        additionalSection.appendChild(
            additionalTitle
        );


        const additionalDescription =
            document.createElement(
                "p"
            );


        additionalDescription.className =
            "skill-alignment-group-description";


        additionalDescription.textContent =
            (
                "These career skills are not "
                + "represented in the recorded "
                + "programme skills."
            );


        additionalSection.appendChild(
            additionalDescription
        );


        const additionalList =
            document.createElement(
                "ul"
            );


        additionalList.className =
            (
                "skill-alignment-list "
                + "skill-alignment-additional"
            );


        additionalSkills.forEach(
            skill => {

                const item =
                    document.createElement(
                        "li"
                    );


                const icon =
                    document.createElement(
                        "span"
                    );


                icon.className =
                    "skill-alignment-icon";


                icon.textContent =
                    "○";


                const skillName =
                    document.createElement(
                        "span"
                    );


                skillName.textContent =
                    (
                        skill.skill_name
                        || skill.skill_id
                        || "Recorded skill"
                    );


                item.appendChild(
                    icon
                );


                item.appendChild(
                    skillName
                );


                additionalList.appendChild(
                    item
                );
            }
        );


        additionalSection.appendChild(
            additionalList
        );


        wrapper.appendChild(
            additionalSection
        );
    }


    // --------------------------------
    // Explanation
    // --------------------------------

    if (
        alignment.explanation
    ) {

        const explanation =
            document.createElement(
                "p"
            );


        explanation.className =
            "skill-alignment-explanation";


        explanation.textContent =
            alignment.explanation;


        wrapper.appendChild(
            explanation
        );
    }


    return wrapper;
}


// ====================================
// Career Pathway Intelligence
// ====================================

function createCareerPathways(
    careers,
    programmeId
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


        // --------------------------------
        // Career heading
        // --------------------------------

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


        // --------------------------------
        // Career description
        // --------------------------------

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


        // --------------------------------
        // Career indicators
        // --------------------------------

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


        // --------------------------------
        // Relationship explanation
        // --------------------------------

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


        // --------------------------------
        // Skill Alignment UI
        // --------------------------------

        const skillAlignmentButton =
            document.createElement(
                "button"
            );


        skillAlignmentButton.type =
            "button";


        skillAlignmentButton.className =
            "skill-alignment-button";


        skillAlignmentButton.textContent =
            "View Skill Alignment";


        const skillAlignmentContainer =
            document.createElement(
                "div"
            );


        skillAlignmentContainer.className =
            "skill-alignment-container";


        skillAlignmentContainer.style.display =
            "none";


        skillAlignmentButton.addEventListener(
            "click",
            async () => {

                // ------------------------
                // Hide existing alignment
                // ------------------------

                if (
                    skillAlignmentContainer
                        .style.display
                    !== "none"
                ) {

                    skillAlignmentContainer
                        .style.display =
                        "none";


                    skillAlignmentButton
                        .textContent =
                        "View Skill Alignment";


                    return;
                }


                // ------------------------
                // Validate identifiers
                // ------------------------

                if (
                    !programmeId
                    || !career.career_id
                ) {

                    skillAlignmentContainer
                        .innerHTML =
                        "";


                    const message =
                        document.createElement(
                            "p"
                        );


                    message.textContent =
                        (
                            "Skill alignment cannot "
                            + "be calculated because "
                            + "the programme or career "
                            + "identifier is missing."
                        );


                    skillAlignmentContainer
                        .appendChild(
                            message
                        );


                    skillAlignmentContainer
                        .style.display =
                        "block";


                    return;
                }


                // ------------------------
                // Loading state
                // ------------------------

                skillAlignmentButton.disabled =
                    true;


                skillAlignmentButton.textContent =
                    "Loading alignment...";


                skillAlignmentContainer.innerHTML =
                    "";


                try {

                    const alignment =
                        await fetchSkillAlignment(
                            programmeId,
                            career.career_id
                        );


                    const content =
                        createSkillAlignmentContent(
                            alignment
                        );


                    skillAlignmentContainer
                        .appendChild(
                            content
                        );


                    skillAlignmentContainer
                        .style.display =
                        "block";


                    skillAlignmentButton
                        .textContent =
                        "Hide Skill Alignment";

                } catch (
                    error
                ) {

                    console.error(
                        (
                            "Skill alignment "
                            + "request failed:"
                        ),
                        error
                    );


                    const errorMessage =
                        document.createElement(
                            "p"
                        );


                    errorMessage.className =
                        "skill-alignment-error";


                    errorMessage.textContent =
                        (
                            "Could not load skill "
                            + "alignment right now."
                        );


                    skillAlignmentContainer
                        .appendChild(
                            errorMessage
                        );


                    skillAlignmentContainer
                        .style.display =
                        "block";


                    skillAlignmentButton
                        .textContent =
                        "Try Skill Alignment Again";

                } finally {

                    skillAlignmentButton.disabled =
                        false;
                }
            }
        );


        careerCard.appendChild(
            skillAlignmentButton
        );


        careerCard.appendChild(
            skillAlignmentContainer
        );


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
            || pathway.to_qualification_id
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
            recommendation.qualification_id
                ? (
                    recommendation.programme_id
                    + " · "
                    + recommendation.qualification_id
                )
                : recommendation.programme_id
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


    const careerSection =
    createCareerPathways(
        recommendation
            .career_pathways,
        recommendation
            .programme_id
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


// ====================================
// Display Recommendations
// ====================================

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


// ====================================
// Alternative Pathway UI
// ====================================

function createRouteNode(
    label,
    value,
    className
) {

    const node =
        document.createElement(
            "div"
        );


    node.className =
        (
            "route-node "
            + className
        );


    const nodeLabel =
        document.createElement(
            "span"
        );


    nodeLabel.className =
        "route-node-label";


    nodeLabel.textContent =
        label;


    const nodeValue =
        document.createElement(
            "strong"
        );


    nodeValue.textContent =
        value || "Not specified";


    node.appendChild(
        nodeLabel
    );


    node.appendChild(
        nodeValue
    );


    return node;
}


function createRouteConnector(
    progressionType
) {

    const connector =
        document.createElement(
            "div"
        );


    connector.className =
        "route-connector";


    const line =
        document.createElement(
            "div"
        );


    line.className =
        "route-connector-line";


    connector.appendChild(
        line
    );


    if (
        progressionType
    ) {

        const label =
            document.createElement(
                "span"
            );


        label.className =
            "route-progression-label";


        label.textContent =
            progressionType;


        connector.appendChild(
            label
        );
    }


    const arrow =
        document.createElement(
            "span"
        );


    arrow.className =
        "route-connector-arrow";


    arrow.textContent =
        "↓";


    connector.appendChild(
        arrow
    );


    return connector;
}


function createAlternativePathwayCard(
    pathway
) {

    const availableNow =
        (
            pathway.pathway_status
            === "AVAILABLE_NOW"
        );


    const statusClass =
        availableNow
            ? "available-now"
            : "requirements-not-met";


    const card =
        document.createElement(
            "article"
        );


    card.className =
        (
            "alternative-route-card "
            + statusClass
        );


    // --------------------------------
    // Header
    // --------------------------------

    const header =
        document.createElement(
            "div"
        );


    header.className =
        "alternative-route-header";


    const headerText =
        document.createElement(
            "div"
        );


    const kicker =
        document.createElement(
            "span"
        );


    kicker.className =
        "alternative-route-kicker";


    kicker.textContent =
        availableNow
            ? "Alternative route"
            : "Possible future route";


    const title =
        document.createElement(
            "h4"
        );


    title.textContent =
        (
            pathway
                .alternative_programme_name
            || "Alternative programme"
        );


    headerText.appendChild(
        kicker
    );


    headerText.appendChild(
        title
    );


    const badge =
        document.createElement(
            "span"
        );


    badge.className =
        (
            "alternative-route-badge "
            + statusClass
        );


    badge.textContent =
        availableNow
            ? "Available now"
            : "Requirements not met";


    header.appendChild(
        headerText
    );


    header.appendChild(
        badge
    );


    card.appendChild(
        header
    );


    // --------------------------------
    // Visual route
    // --------------------------------

    const flow =
        document.createElement(
            "div"
        );


    flow.className =
        "alternative-route-flow";


    flow.appendChild(
        createRouteNode(
            "Starting point",
            "Your current results",
            "route-node-current"
        )
    );


    flow.appendChild(
        createRouteConnector(
            ""
        )
    );


    flow.appendChild(
        createRouteNode(
            "Bridge programme",
            pathway
                .alternative_programme_name,
            "route-node-bridge"
        )
    );


    flow.appendChild(
        createRouteConnector(
            pathway.progression_type
        )
    );


    flow.appendChild(
        createRouteNode(
            "Target programme",
            pathway.target_programme_name,
            "route-node-target"
        )
    );


    card.appendChild(
        flow
    );


    // --------------------------------
    // Pathway status explanation
    // --------------------------------

    const message =
        document.createElement(
            "div"
        );


    message.className =
        (
            "alternative-route-message "
            + (
                availableNow
                    ? "success"
                    : "warning"
            )
        );


    const messageStrong =
        document.createElement(
            "strong"
        );


    messageStrong.textContent =
        availableNow
            ? "✓ Pathway available: "
            : "Pathway requirements: ";


    message.appendChild(
        messageStrong
    );


    message.appendChild(
        document.createTextNode(
            pathway
                .pathway_status_message
            || ""
        )
    );


    card.appendChild(
        message
    );


    // --------------------------------
    // Current eligibility
    // --------------------------------

    const eligibility =
        pathway.current_eligibility
        || {};


    const failedRequirements =
        eligibility.failed_requirements
        || [];


    if (
        !availableNow
        && failedRequirements.length > 0
    ) {

        const missingSection =
            document.createElement(
                "div"
            );


        missingSection.className =
            "alternative-missing-section";


        const missingTitle =
            document.createElement(
                "h5"
            );


        missingTitle.textContent =
            (
                "Entry requirements "
                + "still to complete"
            );


        const list =
            document.createElement(
                "ul"
            );


        failedRequirements.forEach(
            requirement => {

                const item =
                    document.createElement(
                        "li"
                    );


                item.textContent =
                    requirement;


                list.appendChild(
                    item
                );
            }
        );


        missingSection.appendChild(
            missingTitle
        );


        missingSection.appendChild(
            list
        );


        card.appendChild(
            missingSection
        );
    }


    // --------------------------------
    // Progression conditions
    // --------------------------------

    if (
        pathway.progression_conditions
    ) {

        const condition =
            document.createElement(
                "div"
            );


        condition.className =
            "alternative-missing-section";


        const conditionTitle =
            document.createElement(
                "h5"
            );


        conditionTitle.textContent =
            "Progression condition";


        const conditionText =
            document.createElement(
                "p"
            );


        conditionText.textContent =
            pathway.progression_conditions;


        condition.appendChild(
            conditionTitle
        );


        condition.appendChild(
            conditionText
        );


        card.appendChild(
            condition
        );
    }


    // --------------------------------
    // Progression notes
    // --------------------------------

    if (
        pathway.progression_notes
    ) {

        const note =
            document.createElement(
                "div"
            );


        note.className =
            "alternative-route-message";


        const noteStrong =
            document.createElement(
                "strong"
            );


        noteStrong.textContent =
            "Progression note: ";


        note.appendChild(
            noteStrong
        );


        note.appendChild(
            document.createTextNode(
                pathway.progression_notes
            )
        );


        card.appendChild(
            note
        );
    }


    // --------------------------------
    // Metadata
    // --------------------------------

    const details =
        document.createElement(
            "div"
        );


    details.className =
        "alternative-route-details";


    const detailValues = [
        [
            "Programme",
            pathway
                .alternative_programme_id
        ],
        [
            "Qualification",
            pathway
                .alternative_qualification_id
        ],
        [
            "Progression",
            pathway.progression_id
        ]
    ];


    detailValues.forEach(
        ([label, value]) => {

            if (
                !value
            ) {
                return;
            }


            const detail =
                document.createElement(
                    "span"
                );


            detail.className =
                "alternative-route-detail";


            const strong =
                document.createElement(
                    "strong"
                );


            strong.textContent =
                label + ": ";


            detail.appendChild(
                strong
            );


            detail.appendChild(
                document.createTextNode(
                    value
                )
            );


            details.appendChild(
                detail
            );
        }
    );


    if (
        details.children.length > 0
    ) {

        card.appendChild(
            details
        );
    }


    // --------------------------------
    // Official programme link
    // --------------------------------

    if (
        pathway.application_url
    ) {

        const link =
            document.createElement(
                "a"
            );


        link.className =
            "alternative-route-link";


        link.href =
            pathway.application_url;


        link.target =
            "_blank";


        link.rel =
            "noopener noreferrer";


        link.textContent =
            (
                "View official "
                + "programme page →"
            );


        card.appendChild(
            link
        );
    }


    // --------------------------------
    // Evidence disclaimer
    // --------------------------------

    const disclaimer =
        document.createElement(
            "p"
        );


    disclaimer.className =
        "alternative-route-disclaimer";


    disclaimer.textContent =
        (
            "This route is shown from "
            + "progression relationships "
            + "recorded in the WiseLanka "
            + "knowledge base. Final "
            + "admission and progression "
            + "remain subject to the "
            + "institution's current "
            + "requirements."
        );


    card.appendChild(
        disclaimer
    );


    return card;
}


function displayAlternativePathways(
    data
) {

    if (
        !alternativePathwayList
        || !alternativePathwayResults
    ) {
        return;
    }


    alternativePathwayList.innerHTML =
        "";


    const pathways =
        (
            data.alternative_pathways
            || []
        );


    if (
        pathways.length === 0
    ) {

        hideAlternativePathways();

        return;
    }


    if (
        alternativePathwayStatus
    ) {

        alternativePathwayStatus
            .textContent =
            (
                data
                    .eligible_alternative_count
                    > 0
                    ? (
                        data
                            .eligible_alternative_count
                        + " available now"
                    )
                    : "Future route"
            );
    }


    pathways.forEach(
        pathway => {

            const card =
                createAlternativePathwayCard(
                    pathway
                );


            alternativePathwayList
                .appendChild(
                    card
                );
        }
    );


    alternativePathwayResults
        .classList.remove(
            "hidden"
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


// ====================================
// Fetch Alternative Pathways
// ====================================

async function fetchAlternativePathways(
    targetProgrammeId,
    studentResults
) {

    const response =
        await fetch(
            (
                ALTERNATIVE_PATHWAYS_API_URL
                + "/"
                + encodeURIComponent(
                    targetProgrammeId
                )
            ),
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json",
                },

                body:
                    JSON.stringify(
                        {
                            student_results:
                                studentResults,
                        }
                    ),
            }
        );


    if (
        !response.ok
    ) {

        throw new Error(
            (
                "Alternative pathway API returned "
                + response.status
            )
        );
    }


    return await response.json();
}


// ====================================
// Fetch Recommendations
// ====================================

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


    const selectedTargetProgramme =
        targetProgramme
            ? targetProgramme.value
            : "";


    recommendButton.disabled =
        true;


    recommendButton.textContent =
        "Finding pathways...";


    hideAlternativePathways();


    try {

        // --------------------------------
        // Normal recommendations
        // --------------------------------

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


        // --------------------------------
        // Optional alternative route
        // --------------------------------

        if (
            selectedEducationLevel
                === "O_LEVEL"
            && selectedTargetProgramme
        ) {

            try {

                const alternativeData =
                    await fetchAlternativePathways(
                        selectedTargetProgramme,
                        studentResults
                    );


                displayAlternativePathways(
                    alternativeData
                );

            } catch (
                alternativeError
            ) {

                console.error(
                    (
                        "Alternative pathway "
                        + "request failed:"
                    ),
                    alternativeError
                );


                // The normal recommendations
                // remain available even when
                // the optional route request
                // fails.
                hideAlternativePathways();
            }
        }

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


// ====================================
// Main Action Button
// ====================================

recommendButton.addEventListener(
    "click",
    fetchRecommendations
);


// ====================================
// Initialize Interface
// ====================================

setEducationLevel(
    "A_LEVEL"
);