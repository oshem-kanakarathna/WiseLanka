"""
WiseLanka Progression Intelligence Engine.

This module reads verified qualification-progression
relationships and converts them into structured pathway
information for the API and frontend.

The progression graph is qualification-based:

    source qualification
            ↓
    progression relationship
            ↓
    destination qualification
            ↓
    available programme(s)
"""

import csv
from pathlib import Path


# ========================================
# DATA PATHS
# ========================================


PROJECT_ROOT = Path(__file__).resolve().parents[3]

PROGRESSION_FILE = (
    PROJECT_ROOT
    / "data"
    / "relationships"
    / "qualification_progression.csv"
)

QUALIFICATIONS_FILE = (
    PROJECT_ROOT
    / "data"
    / "reference"
    / "qualifications.csv"
)

PROGRAMMES_FILE = (
    PROJECT_ROOT
    / "data"
    / "reference"
    / "programmes.csv"
)

INSTITUTIONS_FILE = (
    PROJECT_ROOT
    / "data"
    / "reference"
    / "institutions.csv"
)


# ========================================
# CSV LOADING
# ========================================


def load_csv(path):
    """
    Load a CSV file and return its rows
    as dictionaries.
    """

    with open(
        path,
        encoding="utf-8",
        newline="",
    ) as file:

        return list(
            csv.DictReader(file)
        )


def load_progression_relationships():
    """
    Load all qualification progression
    relationships.
    """

    return load_csv(
        PROGRESSION_FILE
    )


def load_qualifications():
    """
    Load qualification reference data.
    """

    return load_csv(
        QUALIFICATIONS_FILE
    )


def load_programmes():
    """
    Load programme reference data.
    """

    return load_csv(
        PROGRAMMES_FILE
    )


def load_institutions():
    """
    Load institution reference data.
    """

    return load_csv(
        INSTITUTIONS_FILE
    )


# ========================================
# LOOKUP HELPERS
# ========================================


def build_lookup(
    rows,
    key,
):
    """
    Convert a list of dictionaries into
    an ID-based lookup dictionary.
    """

    return {
        row[key]: row
        for row in rows
        if row.get(key)
    }


def parse_boolean(value):
    """
    Convert CSV boolean text into a Python
    boolean.
    """

    return (
        str(value)
        .strip()
        .lower()
        == "true"
    )


def get_programmes_for_qualification(
    qualification_id,
    programmes,
):
    """
    Return active programmes that deliver
    the specified qualification.
    """

    matches = []

    for programme in programmes:

        if (
            programme.get(
                "qualification_id"
            )
            != qualification_id
        ):
            continue

        if (
            programme.get(
                "programme_status",
                "",
            )
            .strip()
            .lower()
            != "active"
        ):
            continue

        matches.append(
            programme
        )

    return matches


# ========================================
# PROGRESSION ENGINE
# ========================================


def get_progression_pathways(
    qualification_id,
):
    """
    Return immediate academic progression
    pathways from a qualification.

    Example:

        QLF0004
            ↓
        QLF0005
        QLF0006
        QLF0007

    Each destination is enriched with
    qualification, programme, provider and
    awarding-body information.
    """

    relationships = (
        load_progression_relationships()
    )

    qualifications = (
        load_qualifications()
    )

    programmes = (
        load_programmes()
    )

    institutions = (
        load_institutions()
    )

    qualification_lookup = (
        build_lookup(
            qualifications,
            "qualification_id",
        )
    )

    institution_lookup = (
        build_lookup(
            institutions,
            "institution_id",
        )
    )

    source_qualification = (
        qualification_lookup.get(
            qualification_id
        )
    )

    if source_qualification is None:

        return {
            "qualification_id":
                qualification_id,

            "qualification_name":
                None,

            "count":
                0,

            "pathways":
                [],
        }

    pathways = []

    for relationship in relationships:

        if (
            relationship.get(
                "from_qualification_id"
            )
            != qualification_id
        ):
            continue

        destination_id = (
            relationship.get(
                "to_qualification_id"
            )
        )

        destination = (
            qualification_lookup.get(
                destination_id
            )
        )

        if destination is None:
            continue

        destination_programmes = (
            get_programmes_for_qualification(
                destination_id,
                programmes,
            )
        )

        programme_results = []

        for programme in (
            destination_programmes
        ):

            provider_id = (
                programme.get(
                    "provider_institution_id"
                )
            )

            awarding_body_id = (
                programme.get(
                    "awarding_body_id"
                )
            )

            provider = (
                institution_lookup.get(
                    provider_id,
                    {},
                )
            )

            awarding_body = (
                institution_lookup.get(
                    awarding_body_id,
                    {},
                )
            )

            programme_results.append(
                {
                    "programme_id":
                        programme.get(
                            "programme_id"
                        ),

                    "programme_name":
                        programme.get(
                            "programme_name"
                        ),

                    "programme_type":
                        programme.get(
                            "programme_type"
                        ),

                    "field_of_study":
                        programme.get(
                            "field_of_study"
                        ),

                    "duration_months":
                        programme.get(
                            "duration_months"
                        ),

                    "study_mode":
                        programme.get(
                            "study_mode"
                        ),

                    "delivery_mode":
                        programme.get(
                            "delivery_mode"
                        ),

                    "provider_institution_id":
                        provider_id,

                    "provider_name":
                        provider.get(
                            "institution_name"
                        ),

                    "awarding_body_id":
                        awarding_body_id,

                    "awarding_body_name":
                        awarding_body.get(
                            "institution_name"
                        ),

                    "application_url":
                        programme.get(
                            "application_url"
                        ),

                    "programme_status":
                        programme.get(
                            "programme_status"
                        ),
                }
            )

        pathway = {
            "progression_id":
                relationship.get(
                    "progression_id"
                ),

            "from_qualification_id":
                qualification_id,

            "to_qualification_id":
                destination_id,

            "qualification_name":
                destination.get(
                    "qualification_name"
                ),

            "qualification_type":
                destination.get(
                    "qualification_type"
                ),

            "progression_type":
                relationship.get(
                    "progression_type"
                ),

            "conditions":
                relationship.get(
                    "conditions"
                ),

            "guaranteed":
                parse_boolean(
                    relationship.get(
                        "guaranteed"
                    )
                ),

            "notes":
                relationship.get(
                    "notes"
                ),

            "programmes":
                programme_results,
        }

        pathways.append(
            pathway
        )

    return {
        "qualification_id":
            qualification_id,

        "qualification_name":
            source_qualification.get(
                "qualification_name"
            ),

        "count":
            len(pathways),

        "pathways":
            pathways,
    }