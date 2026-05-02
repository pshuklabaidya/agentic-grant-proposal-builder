from __future__ import annotations

from pydantic import BaseModel, Field


class GrantDocument(BaseModel):
    name: str
    text: str
    source_type: str = "uploaded"


class OrganizationProfile(BaseModel):
    organization_name: str = "Example Community Impact Organization"
    mission: str = "Expand equitable access to education, workforce readiness, and community support."
    target_population: str = "Low-income students, adult learners, and underserved families."
    geography: str = "Regional service area"
    current_programs: str = "Tutoring, career coaching, digital literacy, and case management."
    requested_amount: str = "$250,000"
    project_duration: str = "12 months"


class ProposalArtifact(BaseModel):
    title: str
    executive_summary: str
    need_statement: str
    project_design: str
    outcomes: str
    budget_narrative: str
    evaluation_plan: str
    sustainability: str
    funder_alignment: str
    reviewer_risks: list[str] = Field(default_factory=list)
    evidence_used: list[str] = Field(default_factory=list)


class FitScore(BaseModel):
    mission_fit: int
    eligibility_fit: int
    evidence_fit: int
    budget_fit: int
    implementation_fit: int
    overall: int
    rationale: str
