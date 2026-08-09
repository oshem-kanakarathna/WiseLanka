from backend.app.data_loader import load_csv


def get_programme(programme_id):
    programmes = load_csv("reference/programmes.csv")

    for programme in programmes:
        if programme["programme_id"] == programme_id:
            return programme

    return None


def build_explanation(result):
    programme = get_programme(result["programme_id"])

    if programme is None:
        return {
            "title": "Programme not found",
            "eligible": False,
            "summary": "The selected programme could not be found.",
            "passed": [],
            "failed": [],
        }

    passed_messages = []
    failed_messages = []

    for group in result["groups"]:

        if group["passed"]:
            if group["operator"] == "OR":
                successful = [
                    requirement["message"]
                    for requirement in group["requirements"]
                    if requirement["passed"]
                ]

                if successful:
                    passed_messages.append(successful[0])

            else:
                passed_messages.extend(
                    requirement["message"]
                    for requirement in group["requirements"]
                    if requirement["passed"]
                )

        else:
            if group["operator"] == "OR":
                failed_messages.append(
                    "At least one accepted subject must meet "
                    "the required minimum grade."
                )
            else:
                failed_messages.extend(
                    requirement["message"]
                    for requirement in group["requirements"]
                    if not requirement["passed"]
                )

    if result["eligible"]:
        summary = (
            "You currently satisfy the recorded entry requirements "
            "for this programme."
        )
    else:
        summary = (
            "You do not currently satisfy all recorded entry "
            "requirements for this programme."
        )

    return {
        "programme_id": result["programme_id"],
        "programme_name": programme["programme_name"],
        "eligible": result["eligible"],
        "summary": summary,
        "passed": passed_messages,
        "failed": failed_messages,
        "source_url": programme["application_url"],
    }