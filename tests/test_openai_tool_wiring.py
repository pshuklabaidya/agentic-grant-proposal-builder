from pathlib import Path


def test_openai_workflow_defines_function_tools():
    source = Path("src/agentic_grant_proposal_builder/openai_workflow.py").read_text()

    assert "@function_tool" in source
    assert "get_applicant_profile" in source
    assert "get_retrieved_evidence" in source
    assert "get_fit_score" in source
    assert "calculate_budget_plan" in source
    assert "list_evidence_sources" in source


def test_openai_workflow_wires_tools_to_agents():
    source = Path("src/agentic_grant_proposal_builder/openai_workflow.py").read_text()

    assert "Funder Requirements Extractor Agent" in source
    assert "Grant Proposal Writer Agent" in source
    assert "Grant Reviewer Agent" in source
    assert "Budget Narrative Agent" in source
    assert "Proposal Quality Gate Agent" in source
