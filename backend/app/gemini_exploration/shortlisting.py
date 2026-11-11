"""Local learner-aware shortlist for optional Gemini pathway exploration.

All examination/qualification assessment and interest matching happens locally.
Only the resulting public catalogue candidates are sent to Gemini; learner text,
grades, category, qualifications and assessment states are never included.
"""

import re
import unicodedata

from backend.app.data_loader import load_csv
from backend.app.eligibility.engine import assess_academic_gaps


_STOP_WORDS = {
    "a", "an", "and", "for", "i", "in", "into", "my", "of", "or",
    "the", "to", "with", "want", "interested", "interest", "career",
}
_STATUS_WEIGHT = {"MET": 18, "NOT_ASSESSED": 5, "NOT_MET": 0}
_ROLE_WEIGHT = {"IMMEDIATE_OPTION": 100, "FUTURE_PROGRESSION": 65, "EXPLORATORY": 25}


def _tokens(value):
    normalized = unicodedata.normalize("NFKC", str(value or "")).casefold()
    return {
        token for token in re.findall(r"[\w]+", normalized)
        if len(token) > 1 and token not in _STOP_WORDS
    }


def _target_domain(programme, domain, vocational_qualification_ids):
    if domain == "Vocational progression":
        return (
            "vocational" in programme.get("programme_type", "").casefold()
            or programme.get("qualification_id") in vocational_qualification_ids
        )
    if domain == "Foundation pathways":
        return "foundation" in programme.get("programme_type", "").casefold()
    return programme.get("domain") == domain


def build_candidate_shortlist(profile, domain, programmes, progression, limit=8, apply_domain=True):
    """Return public candidate records plus local route metadata.

    Academic status is used as a local ordering signal only. This function does
    not change requirement rules and does not emit a new eligibility decision.
    """
    programme_rows = {
        row["programme_id"]: row for row in load_csv("reference/programmes.csv")
    }
    requirements_by_programme = {}
    for row in load_csv("relationships/programme_entry_requirements.csv"):
        requirements_by_programme.setdefault(row["programme_id"], []).append(row)

    qualifications = load_csv("reference/qualifications.csv")
    vocational_qualification_ids = {
        row["qualification_id"]
        for row in qualifications
        if row.get("education_sector", "").strip().casefold() == "vocational education"
        or row.get("framework_name", "").strip().casefold() == "national vocational qualifications"
    }
    vocational_qualification_ids.update(
        edge["to_qualification_id"]
        for edge in progression
        if edge["from_qualification_id"] in vocational_qualification_ids
    )

    education = profile.get("education", {})
    supplied_levels = {
        level for level in ("O_LEVEL", "A_LEVEL")
        if isinstance(education.get(level), dict) and education[level]
    }
    category = profile.get("learner_category", "AL_LEARNER")
    existing_ids = {
        item.get("qualification_id")
        for item in profile.get("existing_qualifications", [])
        if item.get("qualification_id")
    }
    interests = _tokens(" ".join(profile.get("interests", [])))
    interests.update(_tokens(profile.get("career_intention", "")))

    eligible_domain = [
        p for p in programmes
        if not apply_domain or _target_domain(p, domain, vocational_qualification_ids)
    ]
    by_id = {p["programme_id"]: p for p in eligible_domain}
    if not by_id:
        return {"programmes": [], "progression": [], "required_ids": [], "metadata": {}}

    assessment_by_id = {
        pid: assess_academic_gaps(
            pid,
            education,
            profile.get("education_complete", {}),
            profile.get("existing_qualifications", []),
        )
        for pid in by_id
    }

    if category == "O_LEVEL_LEARNER" or ("O_LEVEL" in supplied_levels and "A_LEVEL" not in supplied_levels):
        source_levels = {"O_LEVEL"}
    elif category == "AL_LEARNER" or "A_LEVEL" in supplied_levels:
        source_levels = {"A_LEVEL"}
    else:
        source_levels = set()

    immediate_ids = set()
    held_route_ids = set()
    for pid in by_id:
        rows = requirements_by_programme.get(pid, [])
        if any(
            (r.get("education_level", "").strip().upper() in source_levels)
            for r in rows
        ):
            immediate_ids.add(pid)
        if any(
            r.get("requirement_type", "").strip().upper() == "QUALIFICATION_HELD"
            and r.get("qualification_id") in existing_ids
            for r in rows
        ):
            held_route_ids.add(pid)

    immediate_ids.update(held_route_ids)
    starting_qualification_ids = set(existing_ids)
    for pid in immediate_ids:
        starting_qualification_ids.add(by_id[pid]["qualification_id"])

    future_ids = {
        p["programme_id"]
        for p in eligible_domain
        if any(
            edge["to_qualification_id"] == p["qualification_id"]
            and edge["from_qualification_id"] in starting_qualification_ids
            for edge in progression
        )
    }
    metadata = {}
    ranked = []
    for programme in eligible_domain:
        pid = programme["programme_id"]
        rows = requirements_by_programme.get(pid, [])
        assessment = assessment_by_id[pid]
        if pid in immediate_ids:
            role = "IMMEDIATE_OPTION"
        elif pid in future_ids:
            role = "FUTURE_PROGRESSION"
        else:
            role = "EXPLORATORY"

        source_row = programme_rows.get(pid, {})
        candidate_text = " ".join((
            source_row.get("programme_name", ""),
            source_row.get("field_of_study", ""),
            source_row.get("programme_type", ""),
            source_row.get("notes", ""),
        ))
        overlap = len(interests & _tokens(candidate_text))
        score = _ROLE_WEIGHT[role] + _STATUS_WEIGHT[assessment["status"]] + min(overlap, 5) * 3
        # A MET immediate route is retained as a required local candidate.
        metadata[pid] = {
            "pathway_position": role,
            "local_assessment_status": assessment["status"],
            "interest_overlap_count": overlap,
            "shortlist_score": score,
            "source_levels": sorted({
                r.get("education_level", "").strip().upper()
                for r in rows if r.get("education_level", "").strip()
            }),
        }
        ranked.append((score, pid))

    ranked.sort(key=lambda item: (-item[0], item[1]))
    chosen_ids = [pid for _, pid in ranked[:limit]]
    # Do not let a candidate limit silently remove a locally MET immediate route.
    required_ids = [
        pid for _, pid in ranked
        if metadata[pid]["pathway_position"] == "IMMEDIATE_OPTION"
        and metadata[pid]["local_assessment_status"] == "MET"
    ][:4]
    for pid in required_ids:
        if pid not in chosen_ids:
            chosen_ids[-1:] = [pid]
    shortlisted = [by_id[pid] for pid in chosen_ids]
    selected_qualifications = {p["qualification_id"] for p in shortlisted}
    local_progression = [
        edge for edge in progression
        if edge["to_qualification_id"] in selected_qualifications
    ]
    # These are catalogue-wide public relationships. Include them independent
    # of the learner's holdings so the provider context does not reveal which
    # qualifications this particular profile reports.
    provider_progression = local_progression
    return {
        "programmes": shortlisted,
        "progression": provider_progression,
        "local_progression": local_progression,
        "required_ids": [pid for pid in required_ids if pid in chosen_ids],
        "metadata": {pid: metadata[pid] for pid in chosen_ids},
    }
