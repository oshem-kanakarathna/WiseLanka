"""Learner-facing explanations from the canonical evidence-aware assessment."""
from backend.app.data_loader import load_csv
from backend.app.eligibility.engine import _combine_gap_states


def get_programme(programme_id):
    return next((row for row in load_csv("reference/programmes.csv")
                 if row["programme_id"] == programme_id), None)


def build_explanation(result, academic_insights=None):
    programme = get_programme(result["programme_id"])
    if academic_insights is None:
        # Compatibility for callers that only supplied technical results.
        states = ["MET" if group["passed"] else "NOT_MET" for group in result.get("groups", [])]
        status = _combine_gap_states(states, "AND")
    else:
        status = academic_insights["status"]
    passed, failed, unknown, sources = [], [], [], []
    if academic_insights:
        for group in academic_insights["groups"]:
            for item in group["requirements"]:
                if item["source_url"]:
                    sources.append({key: item[key] for key in (
                        "source_id", "source_url", "source_organisation", "source_accessed"
                    )})
                if item["status"] == "MET":
                    passed.append(item["explanation"])
                elif group["status"] != "MET":
                    (failed if item["status"] == "NOT_MET" else unknown).append(item["explanation"])
    else:
        for group in result.get("groups", []):
            for item in group["requirements"]:
                if item["passed"]:
                    passed.append(item["message"])
                elif not group["passed"]:
                    failed.append(item["message"])
    return {
        "programme_id": result["programme_id"],
        "programme_name": programme["programme_name"] if programme else "Unknown programme",
        "eligible": result["eligible"],
        "assessment_status": status,
        "summary": {
            "MET": "The recorded requirements are met. Admission and selection are not guaranteed.",
            "NOT_MET": "At least one recorded requirement is not met. Review the groups and official sources.",
            "NOT_ASSESSED": "Eligibility is not assessed: input or rule evidence is incomplete, or provider review is required. This is not a rejection.",
        }[status],
        "passed": passed, "failed": failed, "not_assessed": unknown,
        "source_url": programme.get("application_url", "") if programme else "",
        "requirement_sources": list({item["source_id"]: item for item in sources}.values()),
        "academic_gap_insights": academic_insights,
    }
