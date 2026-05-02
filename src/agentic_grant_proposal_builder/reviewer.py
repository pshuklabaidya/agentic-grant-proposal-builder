from __future__ import annotations

import re

from agentic_grant_proposal_builder.models import FitScore, OrganizationProfile, ProposalArtifact
from agentic_grant_proposal_builder.retrieval import RetrievedChunk
from agentic_grant_proposal_builder.workflow import (
    AgentStep,
    BudgetLineItem,
    BudgetPlan,
    ComplianceCheck,
    FunderRequirement,
    ProposalPackage,
    QualityCheck,
    QualityReport,
    ReviewerFinding,
)


def parse_amount(value: str) -> float:
    matches = re.findall(r"[0-9]+(?:,[0-9]{3})*(?:\.[0-9]+)?", value)
    if not matches:
        return 0.0
    return float(matches[0].replace(",", ""))


def build_workflow_trace(
    profile: OrganizationProfile,
    fit_score: FitScore,
    evidence: list[RetrievedChunk],
    used_openai_agents: bool = False,
) -> list[AgentStep]:
    runtime = "OpenAI Agents SDK" if used_openai_agents else "deterministic fallback"

    return [
        AgentStep(
            agent_name="Intake Agent",
            responsibility="Normalize applicant profile and project constraints.",
            output_summary=(
                f"{profile.organization_name} requests {profile.requested_amount} for a "
                f"{profile.project_duration} project serving {profile.target_population}."
            ),
            confidence="high",
        ),
        AgentStep(
            agent_name="Retrieval Agent",
            responsibility="Find funder-relevant evidence from uploaded guidance.",
            output_summary=f"Retrieved {len(evidence)} evidence chunks for alignment review.",
            confidence="high" if evidence else "low",
        ),
        AgentStep(
            agent_name="Fit Agent",
            responsibility="Score funder alignment.",
            output_summary=f"Computed overall fit score of {fit_score.overall}/100.",
        ),
        AgentStep(
            agent_name="Funder Requirements Extractor Agent",
            responsibility="Extract eligibility, rubric, budget, and evidence requirements.",
            output_summary=f"Generated requirements artifact using {runtime}.",
        ),
        AgentStep(
            agent_name="Grant Proposal Writer Agent",
            responsibility="Draft proposal sections.",
            output_summary=f"Generated proposal artifact using {runtime}.",
        ),
        AgentStep(
            agent_name="Grant Reviewer Agent",
            responsibility="Flag weaknesses and risks.",
            output_summary=f"Generated reviewer findings using {runtime}.",
        ),
        AgentStep(
            agent_name="Budget Narrative Agent",
            responsibility="Create budget line items and narrative.",
            output_summary=f"Generated budget plan using {runtime}.",
        ),
        AgentStep(
            agent_name="Proposal Quality Gate Agent",
            responsibility="Evaluate readiness and unresolved risks.",
            output_summary=f"Generated quality gate report using {runtime}.",
        ),
    ]


def build_funder_requirements(evidence: list[RetrievedChunk]) -> list[FunderRequirement]:
    evidence_text = " ".join(chunk.text.lower() for chunk in evidence)
    source = evidence[0].source if evidence else "retrieved guidance"

    candidates = [
        (
            "Eligibility",
            "Confirm applicant eligibility, nonprofit status, geography, and population fit.",
            "high",
            ["eligible", "eligibility", "applicant", "nonprofit"],
        ),
        (
            "Required Section",
            "Include need statement, project design, outcomes, budget narrative, evaluation plan, and sustainability.",
            "high",
            ["need statement", "project design", "outcomes", "budget", "evaluation", "sustainability"],
        ),
        (
            "Budget",
            "Align line items with allowable costs and implementation needs.",
            "high",
            ["budget", "allowable", "cost"],
        ),
        (
            "Evaluation",
            "Define measurable outputs, outcomes, reporting cadence, and data sources.",
            "medium",
            ["evaluation", "outcomes", "measure", "reporting"],
        ),
        (
            "Sustainability",
            "Explain continuation beyond the grant period.",
            "medium",
            ["sustainability", "partnership", "future funding"],
        ),
    ]

    requirements: list[FunderRequirement] = []

    for requirement_type, requirement, priority, keywords in candidates:
        matched = [keyword for keyword in keywords if keyword in evidence_text]
        if matched:
            requirements.append(
                FunderRequirement(
                    requirement_type=requirement_type,
                    requirement=requirement,
                    priority=priority,
                    evidence=", ".join(matched),
                    source=source,
                )
            )

    if not requirements:
        requirements.append(
            FunderRequirement(
                requirement_type="Evidence",
                requirement="Upload complete funder guidance before final review.",
                priority="high",
                evidence="No matching funder requirement keywords were retrieved.",
                source=source,
            )
        )

    return requirements


def build_reviewer_findings(
    proposal: ProposalArtifact,
    fit_score: FitScore,
    evidence: list[RetrievedChunk],
    funder_requirements: list[FunderRequirement] | None = None,
) -> list[ReviewerFinding]:
    findings: list[ReviewerFinding] = []

    if fit_score.overall < 70:
        findings.append(
            ReviewerFinding(
                category="Funder Fit",
                severity="high",
                finding=f"Overall fit score is {fit_score.overall}/100.",
                recommended_fix="Tighten alignment with funder priorities and eligibility language.",
            )
        )

    if not evidence:
        findings.append(
            ReviewerFinding(
                category="Evidence",
                severity="high",
                finding="No source evidence was retrieved.",
                recommended_fix="Upload the full RFP, NOFO, FAQ, rubric, or grant guidelines.",
            )
        )

    if funder_requirements:
        high_priority = [
            item.requirement for item in funder_requirements if item.priority.lower() == "high"
        ]
        if high_priority:
            findings.append(
                ReviewerFinding(
                    category="High-Priority Requirements",
                    severity="medium",
                    finding="High-priority requirements require explicit proposal coverage.",
                    recommended_fix="Map proposal language to each high-priority requirement.",
                )
            )

    if len(proposal.need_statement.split()) < 80:
        findings.append(
            ReviewerFinding(
                category="Need Statement",
                severity="medium",
                finding="Need statement likely needs more support.",
                recommended_fix="Add current local data, service gaps, and target-population evidence.",
            )
        )

    if len(proposal.outcomes.split()) < 50:
        findings.append(
            ReviewerFinding(
                category="Outcomes",
                severity="medium",
                finding="Outcomes section needs more measurable specificity.",
                recommended_fix="Add baselines, numeric targets, data sources, and reporting cadence.",
            )
        )

    for risk in proposal.reviewer_risks:
        findings.append(
            ReviewerFinding(
                category="Proposal Risk",
                severity="medium",
                finding=risk,
                recommended_fix="Resolve before submission and verify against funder instructions.",
            )
        )

    return findings


def build_compliance_checks(evidence: list[RetrievedChunk]) -> list[ComplianceCheck]:
    evidence_text = " ".join(chunk.text.lower() for chunk in evidence)

    checks = [
        ("Applicant eligibility reviewed", ["eligible", "eligibility", "applicant", "nonprofit"]),
        ("Budget allowability reviewed", ["budget", "allowable", "cost"]),
        ("Evaluation expectations reviewed", ["evaluation", "outcomes", "measure"]),
        ("Implementation expectations reviewed", ["timeline", "implementation", "staff"]),
        ("Sustainability expectations reviewed", ["sustainability", "partnership", "future funding"]),
    ]

    output: list[ComplianceCheck] = []

    for requirement, keywords in checks:
        matched = [keyword for keyword in keywords if keyword in evidence_text]
        output.append(
            ComplianceCheck(
                requirement=requirement,
                status="found" if matched else "needs review",
                evidence=", ".join(matched) if matched else "No matching guidance terms retrieved.",
            )
        )

    return output


def build_budget_plan(profile: OrganizationProfile) -> BudgetPlan:
    total = parse_amount(profile.requested_amount)
    if total <= 0:
        total = 250000.0

    allocations = [
        ("Personnel", 0.45, "Program staff and direct service delivery."),
        ("Program Delivery", 0.20, "Curriculum, workshops, and implementation costs."),
        ("Participant Support", 0.12, "Transportation, supplies, and access-related needs."),
        ("Technology And Data", 0.08, "Data tracking, reporting tools, and software."),
        ("Evaluation", 0.07, "Outcome measurement, reporting, and data review."),
        ("Indirect Costs", 0.08, "Administrative support and compliance infrastructure."),
    ]

    line_items = [
        BudgetLineItem(
            category=category,
            amount=round(total * share, 2),
            justification=justification,
        )
        for category, share, justification in allocations
    ]

    return BudgetPlan(
        total_request=total,
        line_items=line_items,
        narrative=(
            "The draft budget prioritizes personnel and direct program delivery while reserving "
            "funds for participant support, data systems, evaluation, and administrative capacity."
        ),
    )


def build_quality_report(
    proposal: ProposalArtifact,
    fit_score: FitScore,
    evidence: list[RetrievedChunk],
    funder_requirements: list[FunderRequirement],
    reviewer_findings: list[ReviewerFinding],
    budget_plan: BudgetPlan,
) -> QualityReport:
    checks: list[QualityCheck] = []

    checks.append(
        QualityCheck(
            check_name="Evidence Retrieval",
            status="pass" if evidence else "needs_work",
            severity="low" if evidence else "high",
            finding=f"{len(evidence)} evidence chunks retrieved.",
            recommended_fix="Upload complete guidance if evidence is missing.",
        )
    )

    checks.append(
        QualityCheck(
            check_name="Requirements Coverage",
            status="pass" if funder_requirements else "needs_work",
            severity="low" if funder_requirements else "high",
            finding=f"{len(funder_requirements)} funder requirements extracted.",
            recommended_fix="Map proposal text to high-priority requirements.",
        )
    )

    budget_total = round(sum(item.amount for item in budget_plan.line_items), 2)
    expected_total = round(budget_plan.total_request, 2)
    budget_ok = budget_total == expected_total

    checks.append(
        QualityCheck(
            check_name="Budget Math",
            status="pass" if budget_ok else "needs_work",
            severity="low" if budget_ok else "high",
            finding=(
                "Budget line items sum to the total request."
                if budget_ok
                else f"Budget totals ${budget_total:,.2f}, expected ${expected_total:,.2f}."
            ),
            recommended_fix="Verify all line items against funder allowability rules.",
        )
    )

    checks.append(
        QualityCheck(
            check_name="Funder Fit",
            status="pass" if fit_score.overall >= 75 else "needs_work",
            severity="low" if fit_score.overall >= 75 else "medium",
            finding=f"Overall fit score is {fit_score.overall}/100.",
            recommended_fix="Strengthen low alignment areas before final review.",
        )
    )

    unresolved = [
        finding for finding in reviewer_findings if finding.severity.lower() in {"high", "medium"}
    ]

    checks.append(
        QualityCheck(
            check_name="Reviewer Risk",
            status="pass" if not unresolved else "needs_work",
            severity="low" if not unresolved else "medium",
            finding=f"{len(unresolved)} medium-or-high reviewer findings remain.",
            recommended_fix="Resolve reviewer findings before submission.",
        )
    )

    penalty = sum(12 for check in checks if check.status == "needs_work")
    readiness_score = max(0, min(100, 100 - penalty))

    if readiness_score >= 85:
        overall_status = "ready_for_human_review"
        recommendation = "Proceed to human review and funder-instruction verification."
    elif readiness_score >= 65:
        overall_status = "revise_before_submission"
        recommendation = "Revise flagged sections before final review."
    else:
        overall_status = "not_ready"
        recommendation = "Do not submit until evidence, fit, budget, and reviewer risks are addressed."

    return QualityReport(
        overall_status=overall_status,
        readiness_score=readiness_score,
        checks=checks,
        final_recommendation=recommendation,
    )


def build_proposal_package(
    profile: OrganizationProfile,
    proposal: ProposalArtifact,
    fit_score: FitScore,
    evidence: list[RetrievedChunk],
    funder_requirements: list[FunderRequirement] | None = None,
    reviewer_findings: list[ReviewerFinding] | None = None,
    budget_plan: BudgetPlan | None = None,
    quality_report: QualityReport | None = None,
    used_openai_agents: bool = False,
) -> ProposalPackage:
    requirements = funder_requirements or build_funder_requirements(evidence)
    findings = reviewer_findings or build_reviewer_findings(
        proposal,
        fit_score,
        evidence,
        requirements,
    )
    budget = budget_plan or build_budget_plan(profile)
    quality = quality_report or build_quality_report(
        proposal,
        fit_score,
        evidence,
        requirements,
        findings,
        budget,
    )

    return ProposalPackage(
        workflow_trace=build_workflow_trace(profile, fit_score, evidence, used_openai_agents),
        funder_requirements=requirements,
        reviewer_findings=findings,
        compliance_checks=build_compliance_checks(evidence),
        budget_plan=budget,
        quality_report=quality,
    )
