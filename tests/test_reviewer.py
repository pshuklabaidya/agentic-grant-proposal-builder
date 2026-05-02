from agentic_grant_proposal_builder.models import OrganizationProfile
from agentic_grant_proposal_builder.reviewer import build_budget_plan, parse_amount


def test_parse_amount_handles_commas_and_currency():
    assert parse_amount("$250,000") == 250000.0


def test_budget_plan_allocates_full_request():
    profile = OrganizationProfile(requested_amount="$100,000")
    plan = build_budget_plan(profile)

    assert plan.total_request == 100000.0
    assert round(sum(item.amount for item in plan.line_items), 2) == 100000.0
