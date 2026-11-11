"""Opt-in, separate endpoint for grounded Gemini pathway exploration."""

from fastapi import APIRouter, HTTPException

from backend.app.data_loader import KnowledgeDataError
from backend.app.eligibility.engine import assess_academic_gaps
from backend.app.gemini_exploration.models import ExplorationRequest
from backend.app.gemini_exploration.models import GeminiPathwaySelection
from backend.app.gemini_exploration.shortlisting import build_candidate_shortlist
from backend.app.gemini_exploration.service import (
    GeminiUnavailable,
    InvalidModelOutput,
    enabled,
    generate_selection,
    verified_catalogue,
)


router = APIRouter(tags=["optional Gemini exploration"])
STATUS_ORDER = {"MET": 0, "NOT_ASSESSED": 1, "NOT_MET": 2}
POSITION_ORDER = {"IMMEDIATE_OPTION": 0, "FUTURE_PROGRESSION": 1, "EXPLORATORY": 2}


@router.post("/gemini/pathway-exploration")
def explore_pathways(request: ExplorationRequest):
    if not enabled():
        raise HTTPException(status_code=503, detail="Gemini pathway exploration is disabled.")

    try:
        programmes, progression = verified_catalogue()
        if request.compare_programme_ids:
            unknown = set(request.compare_programme_ids) - {p["programme_id"] for p in programmes}
            if unknown:
                raise HTTPException(status_code=422, detail="Unknown or unsupported programme ID.")
            programmes = [p for p in programmes if p["programme_id"] in request.compare_programme_ids]
            qualification_ids = {p["qualification_id"] for p in programmes}
            progression = [
                edge for edge in progression
                if edge["to_qualification_id"] in qualification_ids
            ]

        profile = request.learner_profile.model_dump()
        shortlist = build_candidate_shortlist(
            profile,
            request.exploration_domain,
            programmes,
            progression,
            # Send the complete public domain/comparison pool. A profile-
            # dependent top-N cut could expose learner stage or qualifications
            # through the selected IDs. Local ordering still applies after
            # Gemini returns its bounded comparison.
            limit=len(programmes),
            apply_domain=not bool(request.compare_programme_ids),
        )
        programmes = shortlist["programmes"]
        progression = shortlist["progression"]
        local_progression = shortlist["local_progression"]
        if not programmes:
            raise GeminiUnavailable("No verified catalogue candidates match this exploration.")

        fallback = False
        try:
            # Stable catalogue ordering prevents local grades/interests from
            # being encoded into prompt ordering. Candidate records remain
            # public catalogue facts only.
            provider_programmes = sorted(programmes, key=lambda item: item["programme_id"])
            provider_progression = sorted(progression, key=lambda item: item["progression_id"])
            selection, programmes, progression = generate_selection(
                request.exploration_domain,
                request.compare_programme_ids,
                provider_programmes,
                provider_progression,
            )
            selected = [
                {"selection": item, "source": "GEMINI", "rank": index}
                for index, item in enumerate(selection.pathways, 1)
            ]
            unverified_ideas = [
                {"idea": idea, "status": "UNVERIFIED",
                 "notice": "This topic is outside the verified catalogue. No eligibility or progression claim is made."}
                for idea in selection.unverified_ideas
            ]
        except GeminiUnavailable:
            # Provider/configuration failures do not erase the local result.
            # This bounded fallback uses only the deterministic shortlist.
            fallback = True
            selected = [
                {"selection": GeminiPathwaySelection(
                    programme_id=programme["programme_id"], progression_ids=[],
                    reason_code="COMPARISON_OPTION",
                ), "source": "LOCAL_FALLBACK", "rank": None}
                for programme in shortlist["programmes"][:4]
            ]
            unverified_ideas = []

        selected_ids = {item["selection"].programme_id for item in selected}
        # Preserve the strongest local MET immediate option even if the model
        # omits it. Keep the public response capped at four pathways.
        for programme_id in shortlist["required_ids"]:
            if programme_id not in selected_ids:
                selected.append({
                    "selection": GeminiPathwaySelection(
                        programme_id=programme_id, progression_ids=[],
                        reason_code="COMPARISON_OPTION",
                    ),
                    "source": "LOCAL_SHORTLIST",
                    "rank": None,
                })
        if len(selected) > 4:
            required = [item for item in selected if item["source"] == "LOCAL_SHORTLIST"]
            model_candidates = [item for item in selected if item["source"] != "LOCAL_SHORTLIST"]
            selected = required[:4] + model_candidates[:max(0, 4 - len(required))]

        programme_by_id = {p["programme_id"]: p for p in programmes}
        edges_by_id = {p["progression_id"]: p for p in progression}
        pathways = []
        for selected_item in selected:
            selected_path = selected_item["selection"]
            programme = programme_by_id[selected_path.programme_id]
            assessment = assess_academic_gaps(
                programme["programme_id"],
                profile["education"],
                profile["education_complete"],
                profile["existing_qualifications"],
            )
            chosen_edges = [edges_by_id[edge_id] for edge_id in selected_path.progression_ids]
            # Attach evidence for routes from learner-held awards only after
            # local selection; those profile-linked edges never leave the API.
            chosen_edges.extend(
                edge for edge in local_progression
                if edge["to_qualification_id"] == programme["qualification_id"]
                and edge["from_qualification_id"] in {
                    item.get("qualification_id")
                    for item in profile.get("existing_qualifications", [])
                    if item.get("qualification_id")
                }
                and edge["progression_id"] not in {item["progression_id"] for item in chosen_edges}
            )
            future_edges = [
                edge for edge in local_progression
                if edge["from_qualification_id"] == programme["qualification_id"]
            ]
            pathway_position = shortlist["metadata"][programme["programme_id"]]["pathway_position"]
            full_evidence = programme["entry_requirement_status"] == "VERIFIED"
            pathway_status = "VERIFIED" if full_evidence else "PARTIALLY_VERIFIED"
            explanation = (
                (
                    "WiseLanka retained this as a local pathway option. "
                    if selected_item["source"] != "GEMINI"
                    else f"Gemini selected this shortlisted catalogue item for exploration of {request.exploration_domain}. "
                )
                + f"Its programme record is supported by {programme['programme_source']['organisation']}. "
                + (
                    "The listed entry requirements have official source records."
                    if full_evidence
                    else "Entry requirements are incomplete in the catalogue; requirements remain NOT_ASSESSED."
                )
                + (
                    " This is a future progression option; its recorded conditions must be completed and confirmed with the provider."
                    if pathway_position == "FUTURE_PROGRESSION" else ""
                )
            )
            pathways.append({
                "programme_id": programme["programme_id"],
                "programme_name": programme["programme_name"],
                "domain": programme["domain"],
                "field_of_study": programme["field_of_study"],
                "qualification_id": programme["qualification_id"],
                "qualification_name": programme["qualification_name"],
                "qualification_source": programme["qualification_source"],
                "pathway_evidence_status": pathway_status,
                "entry_requirement_status": programme["entry_requirement_status"],
                "academic_assessment": assessment,
                "entry_requirements": programme["entry_requirements"],
                "progression": chosen_edges,
                "future_progression_options": future_edges,
                "programme_source": programme["programme_source"],
                "reason_code": selected_path.reason_code if selected_item["source"] == "GEMINI" else None,
                "selection_source": selected_item["source"],
                "pathway_position": pathway_position,
                "model_selection_rank": selected_item["rank"],
                "local_assessment_status": shortlist["metadata"][programme["programme_id"]]["local_assessment_status"],
                "explanation": explanation,
            })

        # Keep immediate routes and local eligibility status authoritative;
        # relevance and stage context also order options within these groups.
        pathways.sort(key=lambda p: (
            POSITION_ORDER.get(p["pathway_position"], 2),
            STATUS_ORDER.get(p["academic_assessment"]["status"], 1),
            -shortlist["metadata"][p["programme_id"]]["shortlist_score"],
            p["model_selection_rank"] or 99,
            p["programme_id"],
        ))
        return {
            "mode": "LOCAL_SHORTLIST_FALLBACK" if fallback else "GEMINI_ASSISTED_PATHWAY_EXPLORATION",
            "pathways": pathways,
            "unverified_ideas": unverified_ideas,
            "notice": (
                (
                    "Gemini is unavailable; these options were produced by WiseLanka's local shortlist. "
                    if fallback else "Exploration only. Gemini compared candidates selected locally. "
                )
                + "Academic status was assessed locally from WiseLanka rules. Gemini did not receive the learner's grades, "
                "reported qualification profile, learner category, free-text profile content, identifiers or questionnaire responses. "
                "VERIFIED describes catalogue evidence only; it is not admission, equivalence, selection or award confirmation."
            ),
        }
    except HTTPException:
        raise
    except KnowledgeDataError as error:
        raise HTTPException(status_code=503, detail="Verified pathway knowledge is unavailable.") from error
    except FileNotFoundError as error:
        raise HTTPException(status_code=503, detail="Verified pathway knowledge is unavailable.") from error
    except GeminiUnavailable as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    except InvalidModelOutput as error:
        raise HTTPException(status_code=502, detail="Gemini returned unsupported pathway references.") from error
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
