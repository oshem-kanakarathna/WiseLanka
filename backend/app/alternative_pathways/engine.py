from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Dict, List, Optional

from backend.app.eligibility.engine import (
    evaluate_programme,
)

from backend.app.progression.engine import (
    get_progression_pathways,
)


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[3]

PROGRAMMES_PATH = (
    PROJECT_ROOT
    / "data"
    / "reference"
    / "programmes.csv"
)

PROGRESSION_PATH = (
    PROJECT_ROOT
    / "data"
    / "relationships"
    / "qualification_progression.csv"
)


# ---------------------------------------------------------
# CSV helpers
# ---------------------------------------------------------

def load_csv(
    path: Path,
) -> List[Dict[str, str]]:
    """
    Load a CSV file as a list of dictionaries.
    """

    if not path.exists():
        return []

    with path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:

        reader = csv.DictReader(file)

        return [
            dict(row)
            for row in reader
        ]


def load_programmes() -> List[Dict[str, str]]:
    """
    Load active WiseLanka programme records.
    """

    programmes = load_csv(
        PROGRAMMES_PATH
    )

    return [
        programme
        for programme in programmes
        if (
            programme.get(
                "programme_status",
                ""
            ).strip().lower()
            == "active"
        )
    ]


def load_progression_relationships(
) -> List[Dict[str, str]]:
    """
    Load qualification-to-qualification
    progression relationships.
    """

    return load_csv(
        PROGRESSION_PATH
    )


# ---------------------------------------------------------
# Programme lookup helpers
# ---------------------------------------------------------

def get_programme(
    programme_id: str,
) -> Optional[Dict[str, str]]:
    """
    Return one active programme by ID.
    """

    for programme in load_programmes():

        if (
            programme.get(
                "programme_id"
            )
            == programme_id
        ):

            return programme

    return None


def get_programmes_for_qualification(
    qualification_id: str,
) -> List[Dict[str, str]]:
    """
    Return active programmes that lead to
    the supplied qualification.
    """

    return [
        programme
        for programme in load_programmes()
        if (
            programme.get(
                "qualification_id"
            )
            == qualification_id
        )
    ]


# ---------------------------------------------------------
# Incoming progression lookup
# ---------------------------------------------------------

def get_incoming_progression(
    target_qualification_id: str,
) -> List[Dict[str, str]]:
    """
    Find progression relationships whose
    destination is the target qualification.

    Example:

    QLF0004 -> QLF0006

    If QLF0006 is the target, this function
    returns the relationship from QLF0004.
    """

    relationships = (
        load_progression_relationships()
    )

    return [
        relationship
        for relationship in relationships
        if (
            relationship.get(
                "to_qualification_id"
            )
            == target_qualification_id
        )
    ]


# ---------------------------------------------------------
# Eligibility summary helper
# ---------------------------------------------------------

def build_eligibility_summary(
    technical_result: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Convert the eligibility engine's
    technical result into a compact summary.
    """

    passed_requirements: List[str] = []
    failed_requirements: List[str] = []

    for group in technical_result.get(
        "groups",
        [],
    ):

        for requirement in group.get(
            "requirements",
            [],
        ):

            message = requirement.get(
                "message",
                "",
            )

            if not message:
                continue

            if requirement.get(
                "passed",
                False,
            ):
                passed_requirements.append(
                    message
                )

            else:
                failed_requirements.append(
                    message
                )

    return {
        "eligible": technical_result.get(
            "eligible",
            False,
        ),

        "passed_requirements":
            passed_requirements,

        "failed_requirements":
            failed_requirements,
    }


# ---------------------------------------------------------
# Pathway status helper
# ---------------------------------------------------------

def build_pathway_status(
    eligibility: Dict[str, Any],
) -> Dict[str, str]:
    """
    Convert eligibility into a clear
    alternative-pathway status that can be
    consumed directly by the API/frontend.

    AVAILABLE_NOW:
        The learner currently satisfies the
        entry requirements of the alternative
        programme.

    REQUIREMENTS_NOT_MET:
        The pathway exists structurally, but
        the learner does not currently satisfy
        the entry requirements.
    """

    if eligibility.get(
        "eligible",
        False,
    ):

        return {
            "pathway_status":
                "AVAILABLE_NOW",

            "pathway_status_message":
                (
                    "You currently meet the "
                    "entry requirements for "
                    "this alternative pathway."
                ),
        }

    return {
        "pathway_status":
            "REQUIREMENTS_NOT_MET",

        "pathway_status_message":
            (
                "This pathway can lead towards "
                "the target programme, but you "
                "do not currently meet its "
                "entry requirements."
            ),
    }


# ---------------------------------------------------------
# Main alternative-pathway engine
# ---------------------------------------------------------

def find_alternative_pathways(
    target_programme_id: str,
    student_results: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Find realistic predecessor pathways that
    can lead towards a target programme.

    The process is:

    1. Find the target programme.
    2. Read its target qualification.
    3. Find progression relationships that
       lead INTO that qualification.
    4. Find programmes that award each
       predecessor qualification.
    5. Evaluate the learner against those
       predecessor programmes.
    6. Return current eligibility together
       with progression evidence and
       conditions.

    This function does not invent progression.
    Only relationships stored in WiseLanka's
    structured knowledge base are returned.
    """

    target_programme = get_programme(
        target_programme_id
    )

    if target_programme is None:

        return {
            "target_programme_id":
                target_programme_id,

            "target_programme_name":
                None,

            "target_qualification_id":
                None,

            "target_field_of_study":
                None,

            "count":
                0,

            "eligible_alternative_count":
                0,

            "alternative_pathways":
                [],

            "message":
                (
                    "Target programme was not "
                    "found in the active "
                    "WiseLanka programme data."
                ),
        }

    target_qualification_id = (
        target_programme.get(
            "qualification_id",
            ""
        )
    )

    incoming_relationships = (
        get_incoming_progression(
            target_qualification_id
        )
    )

    alternatives: List[
        Dict[str, Any]
    ] = []

    for relationship in (
        incoming_relationships
    ):

        source_qualification_id = (
            relationship.get(
                "from_qualification_id",
                "",
            )
        )

        predecessor_programmes = (
            get_programmes_for_qualification(
                source_qualification_id
            )
        )

        for alternative_programme in (
            predecessor_programmes
        ):

            alternative_programme_id = (
                alternative_programme.get(
                    "programme_id",
                    "",
                )
            )

            technical_result = (
                evaluate_programme(
                    alternative_programme_id,
                    student_results,
                )
            )

            eligibility = (
                build_eligibility_summary(
                    technical_result
                )
            )

            pathway_status = (
                build_pathway_status(
                    eligibility
                )
            )

            # Confirm the progression information
            # using the existing progression engine.
            progression_result = (
                get_progression_pathways(
                    source_qualification_id
                )
            )

            matched_progression = None

            for pathway in (
                progression_result.get(
                    "pathways",
                    [],
                )
            ):

                if (
                    pathway.get(
                        "to_qualification_id"
                    )
                    == target_qualification_id
                ):

                    matched_progression = (
                        pathway
                    )

                    break

            if matched_progression is None:
                continue

            alternatives.append(
                {
                    "alternative_programme_id":
                        alternative_programme_id,

                    "alternative_programme_name":
                        alternative_programme.get(
                            "programme_name"
                        ),

                    "alternative_programme_type":
                        alternative_programme.get(
                            "programme_type"
                        ),

                    "alternative_qualification_id":
                        source_qualification_id,

                    "current_eligibility":
                        eligibility,

                    "pathway_status":
                        pathway_status.get(
                            "pathway_status"
                        ),

                    "pathway_status_message":
                        pathway_status.get(
                            "pathway_status_message"
                        ),

                    "progression_id":
                        matched_progression.get(
                            "progression_id"
                        ),

                    "progression_type":
                        matched_progression.get(
                            "progression_type"
                        ),

                    "progression_conditions":
                        matched_progression.get(
                            "conditions"
                        ),

                    "guaranteed":
                        matched_progression.get(
                            "guaranteed",
                            False,
                        ),

                    "progression_notes":
                        matched_progression.get(
                            "notes"
                        ),

                    "target_qualification_id":
                        target_qualification_id,

                    "target_qualification_name":
                        matched_progression.get(
                            "qualification_name"
                        ),

                    "target_programme_id":
                        target_programme_id,

                    "target_programme_name":
                        target_programme.get(
                            "programme_name"
                        ),

                    "application_url":
                        alternative_programme.get(
                            "application_url"
                        ),
                }
            )

    # Alternatives currently available to the
    # learner are presented before pathways for
    # which requirements are not yet satisfied.
    alternatives.sort(
        key=lambda item: (
            item.get(
                "pathway_status"
            )
            != "AVAILABLE_NOW",

            item.get(
                "alternative_programme_name"
            )
            or "",
        )
    )

    eligible_count = sum(
        1
        for alternative in alternatives
        if (
            alternative.get(
                "pathway_status"
            )
            == "AVAILABLE_NOW"
        )
    )

    return {
        "target_programme_id":
            target_programme_id,

        "target_programme_name":
            target_programme.get(
                "programme_name"
            ),

        "target_qualification_id":
            target_qualification_id,

        "target_field_of_study":
            target_programme.get(
                "field_of_study"
            ),

        "count":
            len(alternatives),

        "eligible_alternative_count":
            eligible_count,

        "alternative_pathways":
            alternatives,
    }