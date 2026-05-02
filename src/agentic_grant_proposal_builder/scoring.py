from __future__ import annotations

from agentic_grant_proposal_builder.models import FitScore, OrganizationProfile
from agentic_grant_proposal_builder.retrieval import RetrievedChunk


def clamp_score(value: int) -> int:
    return max(0, min(100, value))


def keyword_score(text: str, keywords: list[str]) -> int:
    lower_text = text.lower()
    hits = sum(1 for keyword in keywords if keyword.lower() in lower_text)
    return clamp_score(35 + hits * 13)


def score_funder_fit(profile: OrganizationProfile, evidence: list[RetrievedChunk]) -> FitScore:
    evidence_text = " ".join(chunk.text for chunk in evidence)
    profile_text = " ".join(
        [
            profile.mission,
            profile.target_population,
            profile.geography,
            profile.current_programs,
            profile.requested_amount,
            profile.project_duration,
        ]
    )

    mission_fit = keyword_score(evidence_text, profile.mission.split()[:10])
    eligibility_fit = keyword_score(
        evidence_text,
        ["eligible", "eligibility", "nonprofit", "applicant", "community"],
    )
    evidence_fit = keyword_score(
        evidence_text + profile_text,
        ["outcomes", "data", "evidence", "evaluation"],
    )
    budget_fit = keyword_score(
        evidence_text + profile_text,
        ["budget", "allowable", "cost", "request"],
    )
    implementation_fit = keyword_score(
        evidence_text + profile_text,
        ["timeline", "capacity", "staff", "implementation"],
    )

    overall = round(
        (mission_fit + eligibility_fit + evidence_fit + budget_fit + implementation_fit) / 5
    )

    return FitScore(
        mission_fit=mission_fit,
        eligibility_fit=eligibility_fit,
        evidence_fit=evidence_fit,
        budget_fit=budget_fit,
        implementation_fit=implementation_fit,
        overall=overall,
        rationale=(
            "The score reflects textual overlap between funder guidance, applicant profile, "
            "eligibility language, budget terms, implementation terms, and evaluation expectations."
        ),
    )
