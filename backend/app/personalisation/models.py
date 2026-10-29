"""Profile contract; no identity, persistence or competence assessment."""

from typing import Any, Literal, Union

from pydantic import BaseModel, Field, field_validator, model_validator

from backend.app.data_loader import load_csv


class ExistingQualification(BaseModel):
    title: str = Field(min_length=1, max_length=160)
    qualification_id: str = Field(default="", max_length=40)
    framework: str = Field(default="", max_length=80)
    level: str = Field(default="", max_length=40)

    @field_validator("title", "qualification_id", "framework", "level")
    @classmethod
    def clean_text(cls, value):
        value = value.strip()
        return value

    @model_validator(mode="after")
    def nonblank_title(self):
        if not self.title:
            raise ValueError("A qualification title is required.")
        if self.qualification_id:
            record = next((row for row in load_csv("reference/qualifications.csv")
                           if row["qualification_id"] == self.qualification_id
                           and row.get("active_status") == "Active"), None)
            if record is None:
                raise ValueError("Unknown or inactive catalogue qualification ID; use an empty ID for a custom award.")
            for field, column in (("title", "qualification_name"),
                                  ("framework", "framework_name"),
                                  ("level", "framework_level")):
                expected = record[column].strip()
                supplied = getattr(self, field)
                if supplied and supplied.casefold() != expected.casefold():
                    raise ValueError(f"Qualification {field} does not match its catalogue ID; use an empty ID for a custom award.")
                # Fill omitted metadata and return consistent canonical strings.
                setattr(self, field, expected)
        return self


class ReportedSkill(BaseModel):
    skill_id: str = Field(min_length=1, max_length=40)
    status: Literal["REPORTED", "DEVELOPMENT_OPPORTUNITY"]


class LearnerProfile(BaseModel):
    education: dict[str, Union[str, dict[str, str]]]
    interests: list[str] = Field(default_factory=list)
    career_goal_id: str = ""
    preferences: dict[str, Any] = Field(default_factory=dict)
    learner_category: Literal["AL_LEARNER", "VOCATIONAL_LEARNER", "EARLY_CAREER"] = "AL_LEARNER"
    existing_qualifications: list[ExistingQualification] = Field(default_factory=list, max_length=30)
    self_reported_skills: list[ReportedSkill] = Field(default_factory=list, max_length=100)
    # Omitted flags preserve the interpretation of existing submitted results.
    education_complete: dict[Literal["O_LEVEL", "A_LEVEL"], bool] = Field(default_factory=dict)

    @field_validator("education")
    @classmethod
    def validate_results(cls, education):
        nested = any(isinstance(value, dict) for value in education.values())
        if nested and any(not isinstance(value, dict) for value in education.values()):
            raise ValueError("Do not mix flat and level-aware examination results.")
        sections = education.items() if nested else [("A_LEVEL", education)]
        cleaned = {}
        for level, results in sections:
            if level not in {"O_LEVEL", "A_LEVEL"}:
                raise ValueError("Examination level must be O_LEVEL or A_LEVEL; use existing_qualifications for other awards.")
            output = {}
            seen = set()
            for subject, grade in results.items():
                name = subject.strip()
                if not name or name.casefold() in seen:
                    raise ValueError("Examination subjects must be nonblank and unique within each level.")
                seen.add(name.casefold())
                grade = grade.strip().upper()
                if grade not in {"A", "B", "C", "S", "F"}:
                    raise ValueError(f"Invalid examination grade for {name}; use A, B, C, S or F.")
                output[name] = grade
            cleaned[level] = output
        return cleaned if nested else cleaned["A_LEVEL"]

    @model_validator(mode="after")
    def validate_profile(self):
        if not any(self.education.values()) and not self.existing_qualifications:
            raise ValueError("Provide examination results or an existing qualification.")
        ids = [item.skill_id for item in self.self_reported_skills]
        if len(ids) != len(set(ids)):
            raise ValueError("Each skill may be reported only once.")
        return self
