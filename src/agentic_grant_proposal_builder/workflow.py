from __future__ import annotations

from pydantic import BaseModel, Field


class AgentStep(BaseModel):
    agent_name: str
    responsibility: str
    output_summary: str
    confidence: str = "medium"


class ReviewerFinding(BaseModel):
    category: str
    severity: str
    finding: str
    recommended_fix: str


class ComplianceCheck(BaseModel):
    requirement: str
    status: str
    evidence: str


class FunderRequirement(BaseModel):
    requirement_type: str
    requirement: str
    priority: str = "medium"
    evidence: str
    source: str = "retrieved guidance"


class BudgetLineItem(BaseModel):
    category: str
    amount: float
    justification: str


class BudgetPlan(BaseModel):
    total_request: float
    line_items: list[BudgetLineItem] = Field(default_factory=list)
    narrative: str


class QualityCheck(BaseModel):
    check_name: str
    status: str
    severity: str
    finding: str
    recommended_fix: str


class QualityReport(BaseModel):
    overall_status: str
    readiness_score: int
    checks: list[QualityCheck] = Field(default_factory=list)
    final_recommendation: str


class ProposalPackage(BaseModel):
    workflow_trace: list[AgentStep]
    funder_requirements: list[FunderRequirement] = Field(default_factory=list)
    reviewer_findings: list[ReviewerFinding]
    compliance_checks: list[ComplianceCheck]
    budget_plan: BudgetPlan
    quality_report: QualityReport | None = None
