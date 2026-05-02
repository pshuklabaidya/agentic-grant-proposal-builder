from agentic_grant_proposal_builder.models import GrantDocument, OrganizationProfile
from agentic_grant_proposal_builder.pipeline import build_proposal


def test_pipeline_builds_proposal_without_openai_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    profile = OrganizationProfile()
    docs = [
        GrantDocument(
            name="guidance.txt",
            text=(
                "Eligible nonprofit applicants may request budget support for education, "
                "workforce readiness, evaluation, outcomes, allowable costs, and implementation."
            ),
        )
    ]

    proposal, fit_score, evidence, package = build_proposal(profile, docs)

    assert proposal.title
    assert fit_score.overall >= 0
    assert evidence
    assert package.workflow_trace
    assert package.funder_requirements
    assert package.quality_report is not None
