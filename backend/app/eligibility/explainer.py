from backend.app.data_loader import load_csv


def get_programme(programme_id):
    """
    Retrieve one programme from the
    WiseLanka programme dataset.
    """

    programmes = load_csv(
        "reference/programmes.csv"
    )

    for programme in programmes:

        if (
            programme["programme_id"]
            == programme_id
        ):
            return programme

    return None


def build_explanation(result):
    """
    Convert technical eligibility results
    into learner-friendly information.
    """

    programme = get_programme(
        result["programme_id"]
    )

    if programme is None:

        return {
            "programme_id":
                result["programme_id"],

            "programme_name":
                "Unknown programme",

            "eligible":
                False,

            "summary":
                (
                    "The selected programme "
                    "could not be found."
                ),

            "passed":
                [],

            "failed":
                [],

            "source_url":
                "",
        }

    passed_messages = []
    failed_messages = []

    for group in result["groups"]:

        # --------------------------------
        # Passed group
        # --------------------------------

        if group["passed"]:

            if group["operator"] == "OR":

                successful_requirements = [
                    requirement["message"]
                    for requirement
                    in group["requirements"]
                    if requirement["passed"]
                ]

                if successful_requirements:

                    passed_messages.append(
                        successful_requirements[0]
                    )

            else:

                passed_messages.extend(
                    requirement["message"]
                    for requirement
                    in group["requirements"]
                    if requirement["passed"]
                )

        # --------------------------------
        # Failed group
        # --------------------------------

        else:

            if group["operator"] == "OR":

                failed_messages.append(
                    (
                        "At least one accepted "
                        "subject must meet the "
                        "required minimum grade."
                    )
                )

            else:

                failed_messages.extend(
                    requirement["message"]
                    for requirement
                    in group["requirements"]
                    if not requirement["passed"]
                )

    # ------------------------------------
    # Final summary
    # ------------------------------------

    if result["eligible"]:

        summary = (
            "You currently satisfy the "
            "recorded entry requirements "
            "for this programme."
        )

    else:

        summary = (
            "You do not currently satisfy "
            "all recorded entry requirements "
            "for this programme."
        )

    return {
        "programme_id":
            programme["programme_id"],

        "programme_name":
            programme["programme_name"],

        "eligible":
            result["eligible"],

        "summary":
            summary,

        "passed":
            passed_messages,

        "failed":
            failed_messages,

        "source_url":
            programme["application_url"],
    }