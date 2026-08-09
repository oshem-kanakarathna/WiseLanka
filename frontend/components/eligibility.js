const API_URL =
    "http://127.0.0.1:8000/eligibility";


const checkButton =
    document.getElementById(
        "checkButton"
    );


const resultCard =
    document.getElementById(
        "resultCard"
    );


const emptyResult =
    document.getElementById(
        "emptyResult"
    );


const statusBadge =
    document.getElementById(
        "statusBadge"
    );


const resultProgramme =
    document.getElementById(
        "resultProgramme"
    );


const resultSummary =
    document.getElementById(
        "resultSummary"
    );


const passedList =
    document.getElementById(
        "passedList"
    );


const failedList =
    document.getElementById(
        "failedList"
    );


const failedSection =
    document.getElementById(
        "failedSection"
    );


const sourceLink =
    document.getElementById(
        "sourceLink"
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


function clearResultLists() {

    passedList.innerHTML = "";

    failedList.innerHTML = "";
}


function addListItem(
    list,
    message
) {

    const item =
        document.createElement("li");

    item.textContent =
        message;

    list.appendChild(item);
}


function displayResult(data) {

    clearResultLists();


    resultProgramme.textContent =
        data.programme_name;


    resultSummary.textContent =
        data.summary;


    data.passed.forEach(
        message => {

            addListItem(
                passedList,
                message
            );
        }
    );


    data.failed.forEach(
        message => {

            addListItem(
                failedList,
                message
            );
        }
    );


    if (
        data.failed.length === 0
    ) {

        failedSection.classList.add(
            "hidden"
        );

    } else {

        failedSection.classList.remove(
            "hidden"
        );
    }


    if (data.eligible) {

        statusBadge.textContent =
            "✓ Eligible";

        statusBadge.className =
            (
                "status-badge "
                + "status-success"
            );

    } else {

        statusBadge.textContent =
            "Not Eligible";

        statusBadge.className =
            (
                "status-badge "
                + "status-fail"
            );
    }


    sourceLink.href =
        data.source_url;


    emptyResult.classList.add(
        "hidden"
    );


    resultCard.classList.remove(
        "hidden"
    );
}


async function checkEligibility() {

    const programmeId =
        document.getElementById(
            "programme"
        ).value;


    const studentResults =
        collectStudentResults();


    const payload = {

        programme_id:
            programmeId,

        student_results:
            studentResults,
    };


    checkButton.disabled = true;

    checkButton.textContent =
        "Checking eligibility...";


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


        displayResult(data);

    } catch (error) {

        console.error(error);


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

        checkButton.disabled =
            false;

        checkButton.textContent =
            "Check My Eligibility";
    }
}


checkButton.addEventListener(
    "click",
    checkEligibility
);