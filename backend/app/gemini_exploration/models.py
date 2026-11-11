"""Small request and response contracts for bounded pathway exploration."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from backend.app.personalisation.models import LearnerProfile


ExplorationDomain = Literal[
    "Information Technology",
    "Business and Management",
    "Engineering",
    "Vocational progression",
    "Foundation pathways",
]


class ExplorationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    learner_profile: LearnerProfile
    exploration_domain: ExplorationDomain
    compare_programme_ids: list[str] = Field(default_factory=list, max_length=3)

    @model_validator(mode="before")
    @classmethod
    def infer_omitted_o_level_category(cls, value):
        # Preserve older callers while avoiding the misleading AL_LEARNER
        # default for an O/L-only profile. Explicit categories are retained.
        if not isinstance(value, dict):
            return value
        profile = value.get("learner_profile")
        if not isinstance(profile, dict) or "learner_category" in profile:
            return value
        education = profile.get("education")
        if (
            isinstance(education, dict)
            and isinstance(education.get("O_LEVEL"), dict)
            and education["O_LEVEL"]
            and not education.get("A_LEVEL")
        ):
            copied = dict(value)
            copied_profile = dict(profile)
            copied_profile["learner_category"] = "O_LEVEL_LEARNER"
            copied["learner_profile"] = copied_profile
            return copied
        return value

    @field_validator("compare_programme_ids")
    @classmethod
    def unique_programme_ids(cls, values):
        if len(values) != len(set(values)):
            raise ValueError("Programme IDs must be unique.")
        return values

    @model_validator(mode="after")
    def bound_profile_payload(self):
        interests = self.learner_profile.interests
        if len(interests) > 20 or any(len(item) > 160 for item in interests):
            raise ValueError("Exploration profiles support at most 20 interests of 160 characters each.")
        total_subjects = sum(
            len(value) if isinstance(value, dict) else 1
            for value in self.learner_profile.education.values()
        )
        if total_subjects > 24:
            raise ValueError("Exploration profile contains too many examination subjects.")
        if (
            self.learner_profile.learner_category == "O_LEVEL_LEARNER"
            and not self.learner_profile.education.get("O_LEVEL")
        ):
            raise ValueError("O_LEVEL_LEARNER requires O_LEVEL examination evidence.")
        return self


class GeminiPathwaySelection(BaseModel):
    model_config = ConfigDict(extra="forbid")

    programme_id: str = Field(min_length=1, max_length=40)
    progression_ids: list[str] = Field(default_factory=list, max_length=3)
    reason_code: Literal[
        "INTEREST_AREA_MATCH",
        "DOCUMENTED_PROGRESSION",
        "COMPARISON_OPTION",
    ]


class GeminiExplorationOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pathways: list[GeminiPathwaySelection] = Field(min_length=1, max_length=4)
    unverified_ideas: list[str] = Field(default_factory=list, max_length=2)

    @field_validator("unverified_ideas")
    @classmethod
    def bound_unverified_ideas(cls, values):
        cleaned = []
        for value in values:
            value = value.strip()
            if not value or len(value) > 160:
                raise ValueError("Unverified ideas must contain 1–160 characters.")
            if "http://" in value.casefold() or "https://" in value.casefold():
                raise ValueError("Gemini cannot supply resource URLs.")
            cleaned.append(value)
        return cleaned
