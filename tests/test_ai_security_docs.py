from pathlib import Path


def test_ai_usage_doc_exists():
    path = Path("docs/AI_USAGE_AND_LIMITATIONS.md")

    assert path.exists()
    text = path.read_text()
    assert "Deterministic Fallback Path" in text
    assert "OpenAI Agents Path" in text
    assert "Review Boundaries" in text


def test_security_policy_exists():
    path = Path("SECURITY.md")

    assert path.exists()
    text = path.read_text()
    assert ".env" in text
    assert ".streamlit/secrets.toml" in text
    assert "OpenAI API Key" in text


def test_human_review_checklist_exists():
    path = Path("docs/HUMAN_REVIEW_CHECKLIST.md")

    assert path.exists()
    text = path.read_text()
    assert "Before Submission" in text
    assert "Budget" in text
    assert "AI Output Review" in text


def test_docs_index_links_ai_security_docs():
    text = Path("docs/DOCS_INDEX.md").read_text()

    assert "AI_USAGE_AND_LIMITATIONS.md" in text
    assert "HUMAN_REVIEW_CHECKLIST.md" in text
    assert "../SECURITY.md" in text


def test_readme_links_ai_security_docs():
    text = Path("README.md").read_text()

    assert "docs/AI_USAGE_AND_LIMITATIONS.md" in text
    assert "docs/HUMAN_REVIEW_CHECKLIST.md" in text
    assert "SECURITY.md" in text
