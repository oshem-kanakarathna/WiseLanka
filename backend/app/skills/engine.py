from backend.app.data_loader import load_csv


def assess_learner_skills(career_id, reported_skills):
    """Compare explicit self-reports with curated career skills, not competence."""
    lookup = _skill_lookup()
    reports = {item["skill_id"]: item["status"] for item in reported_skills}
    unknown = set(reports) - set(lookup)
    if unknown:
        raise ValueError("Unknown or inactive self-reported skill ID: " + ", ".join(sorted(unknown)))
    career = _find_by_id(_load_careers(), "career_id", career_id)
    requirements = get_career_skills(career_id) if career and career.get("active_status") == "Active" else []
    items = []
    for skill in requirements:
        report = reports.get(skill["skill_id"], "UNREPORTED")
        items.append({
            **skill, "report_status": report,
            "status": "SELF_REPORTED" if report == "REPORTED" else "DEVELOPMENT_OPPORTUNITY" if report == "DEVELOPMENT_OPPORTUNITY" else "NOT_ASSESSED",
            "explanation": {
                "REPORTED": "You report this skill. This does not verify competence or the expected career proficiency level.",
                "DEVELOPMENT_OPPORTUNITY": "You identified this skill as a development opportunity; this is not an objective assessment.",
                "UNREPORTED": "You have not reported this skill. No conclusion about your competence can be drawn.",
            }[report],
        })
    return {
        "career_id": career_id, "status": "SELF_REPORT_COMPARISON" if requirements else "NOT_ASSESSED",
        "career_requirements": items,
        "reported_skills": [{**lookup[item["skill_id"]], "report_status": item["status"]} for item in reported_skills],
        "explanation": "Comparison uses curated career-skill relationships and your optional self-reports. No skill test or objective competence assessment was performed. Career proficiency is not verified."
        if requirements else "Select a supported career with recorded skill requirements. Missing career evidence is not a negative assessment; your self-reports are retained below.",
        "evidence_note": "Career-skill mappings currently contain descriptive notes, not per-relationship source citations. This limits their evidential strength.",
    }


# ====================================
# Load Skills Knowledge
# ====================================

def _load_skills():
    return load_csv(
        "reference/skills.csv"
    )


def _load_programme_skills():
    return load_csv(
        "relationships/programme_skills.csv"
    )


def _load_career_skills():
    return load_csv(
        "relationships/career_skills.csv"
    )


def _load_programmes():
    return load_csv(
        "reference/programmes.csv"
    )


def _load_careers():
    return load_csv(
        "reference/careers.csv"
    )


# ====================================
# Lookup Helpers
# ====================================

def _find_by_id(
    records,
    field_name,
    record_id,
):
    for record in records:

        if (
            record.get(field_name)
            == record_id
        ):
            return record

    return None


def _skill_lookup():
    skills = _load_skills()

    return {
        skill["skill_id"]: skill
        for skill in skills
        if (
            skill.get(
                "active_status"
            )
            == "Active"
        )
    }


# ====================================
# Programme Skills
# ====================================

def get_programme_skills(
    programme_id,
):
    skill_lookup = _skill_lookup()

    relationships = (
        _load_programme_skills()
    )

    programme_skills = []

    for relationship in relationships:

        if (
            relationship.get(
                "programme_id"
            )
            != programme_id
        ):
            continue

        skill_id = relationship.get(
            "skill_id"
        )

        skill = skill_lookup.get(
            skill_id
        )

        if not skill:
            continue

        programme_skills.append(
            {
                "skill_id":
                    skill_id,

                "skill_name":
                    skill.get(
                        "skill_name"
                    ),

                "skill_category":
                    skill.get(
                        "skill_category"
                    ),

                "skill_level":
                    relationship.get(
                        "skill_level"
                    ),

                "relationship_type":
                    relationship.get(
                        "relationship_type"
                    ),

                "notes":
                    relationship.get(
                        "notes"
                    ),
            }
        )

    return programme_skills


# ====================================
# Career Skills
# ====================================

def get_career_skills(
    career_id,
):
    skill_lookup = _skill_lookup()

    relationships = (
        _load_career_skills()
    )

    career_skills = []

    for relationship in relationships:

        if (
            relationship.get(
                "career_id"
            )
            != career_id
        ):
            continue

        skill_id = relationship.get(
            "skill_id"
        )

        skill = skill_lookup.get(
            skill_id
        )

        if not skill:
            continue

        career_skills.append(
            {
                "skill_id":
                    skill_id,

                "skill_name":
                    skill.get(
                        "skill_name"
                    ),

                "skill_category":
                    skill.get(
                        "skill_category"
                    ),

                "importance_level":
                    relationship.get(
                        "importance_level"
                    ),

                "expected_level":
                    relationship.get(
                        "expected_level"
                    ),

                "notes":
                    relationship.get(
                        "notes"
                    ),
            }
        )

    return career_skills


# ====================================
# Programme-Career Skill Alignment
# ====================================

def get_skill_alignment(
    programme_id,
    career_id,
):
    programmes = _load_programmes()
    careers = _load_careers()

    programme = _find_by_id(
        programmes,
        "programme_id",
        programme_id,
    )

    career = _find_by_id(
        careers,
        "career_id",
        career_id,
    )


    # --------------------------------
    # Unknown programme or career
    # --------------------------------

    if (
        not programme
        or not career
    ):
        return {
            "programme_id":
                programme_id,

            "career_id":
                career_id,

            "status":
                "NOT_FOUND",

            "alignment_percentage":
                None,

            "shared_skills":
                [],

            "additional_career_skills":
                [],

            "explanation":
                (
                    "The requested programme "
                    "or career could not be "
                    "found in the WiseLanka "
                    "knowledge base."
                ),
        }


    programme_skills = (
        get_programme_skills(
            programme_id
        )
    )

    career_skills = (
        get_career_skills(
            career_id
        )
    )


    # --------------------------------
    # Insufficient programme evidence
    # --------------------------------

    if (
        len(programme_skills)
        == 0
    ):
        return {
            "programme_id":
                programme_id,

            "programme_name":
                programme.get(
                    "programme_name"
                ),

            "career_id":
                career_id,

            "career_name":
                career.get(
                    "career_name"
                ),

            "status":
                "INSUFFICIENT_DATA",

            "programme_skill_count":
                0,

            "career_skill_count":
                len(
                    career_skills
                ),

            "shared_skill_count":
                0,

            "additional_skill_count":
                0,

            "alignment_percentage":
                None,

            "programme_skills":
                [],

            "career_skills":
                career_skills,

            "shared_skills":
                [],

            "additional_career_skills":
                [],

            "explanation":
                (
                    "WiseLanka does not "
                    "currently have sufficient "
                    "recorded programme-skill "
                    "evidence to calculate "
                    "this alignment. A missing "
                    "alignment score does not "
                    "mean that the programme "
                    "does not develop skills "
                    "relevant to this career."
                ),
        }


    # --------------------------------
    # Insufficient career evidence
    # --------------------------------

    if (
        len(career_skills)
        == 0
    ):
        return {
            "programme_id":
                programme_id,

            "programme_name":
                programme.get(
                    "programme_name"
                ),

            "career_id":
                career_id,

            "career_name":
                career.get(
                    "career_name"
                ),

            "status":
                "INSUFFICIENT_DATA",

            "programme_skill_count":
                len(
                    programme_skills
                ),

            "career_skill_count":
                0,

            "shared_skill_count":
                0,

            "additional_skill_count":
                0,

            "alignment_percentage":
                None,

            "programme_skills":
                programme_skills,

            "career_skills":
                [],

            "shared_skills":
                [],

            "additional_career_skills":
                [],

            "explanation":
                (
                    "WiseLanka does not "
                    "currently have sufficient "
                    "recorded career-skill "
                    "evidence to calculate "
                    "this alignment."
                ),
        }


    # --------------------------------
    # Compare skill identifiers
    # --------------------------------

    programme_skill_ids = {
        skill["skill_id"]
        for skill
        in programme_skills
    }

    shared_skills = []

    additional_career_skills = []

    for skill in career_skills:

        if (
            skill["skill_id"]
            in programme_skill_ids
        ):
            shared_skills.append(
                skill
            )

        else:
            additional_career_skills.append(
                skill
            )


    # --------------------------------
    # Calculate transparent alignment
    # --------------------------------

    career_skill_count = len(
        career_skills
    )

    alignment_percentage = round(
        (
            len(
                shared_skills
            )
            / career_skill_count
        )
        * 100,
        1,
    )


    # --------------------------------
    # Final alignment response
    # --------------------------------

    return {
        "programme_id":
            programme_id,

        "programme_name":
            programme.get(
                "programme_name"
            ),

        "career_id":
            career_id,

        "career_name":
            career.get(
                "career_name"
            ),

        "status":
            "AVAILABLE",

        "programme_skill_count":
            len(
                programme_skills
            ),

        "career_skill_count":
            career_skill_count,

        "shared_skill_count":
            len(
                shared_skills
            ),

        "additional_skill_count":
            len(
                additional_career_skills
            ),

        "alignment_percentage":
            alignment_percentage,

        "programme_skills":
            programme_skills,

        "career_skills":
            career_skills,

        "shared_skills":
            shared_skills,

        "additional_career_skills":
            additional_career_skills,

        "explanation":
            (
                "The alignment percentage "
                "compares career skills "
                "recorded in the WiseLanka "
                "knowledge base with skills "
                "represented by the selected "
                "programme. Additional career "
                "skills are not claims about "
                "the learner's personal skill "
                "level."
            ),
    }
