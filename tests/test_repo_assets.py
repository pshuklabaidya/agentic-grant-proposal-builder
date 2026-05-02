from pathlib import Path


def test_ci_workflow_exists():
    path = Path(".github/workflows/ci.yml")

    assert path.exists()
    text = path.read_text()
    assert "python -m pytest" in text
    assert "python -m ruff check ." in text
    assert "python -m agentic_grant_proposal_builder.evaluation" in text


def test_makefile_exists_with_core_commands():
    path = Path("Makefile")

    assert path.exists()
    text = path.read_text()
    assert "check:" in text
    assert "run:" in text
    assert "eval:" in text


def test_deployment_guide_exists():
    path = Path("DEPLOYMENT.md")

    assert path.exists()
    text = path.read_text()
    assert "Streamlit Community Cloud" in text
    assert "OPENAI_API_KEY" in text


def test_portfolio_review_brief_exists():
    path = Path("docs/PORTFOLIO_REVIEW.md")

    assert path.exists()
    text = path.read_text()
    assert "Agentic Grant Proposal Builder" in text
    assert "Evaluation Story" in text
