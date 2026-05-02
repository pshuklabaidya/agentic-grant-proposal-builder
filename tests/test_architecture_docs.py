from pathlib import Path


def test_architecture_doc_exists():
    path = Path("docs/ARCHITECTURE.md")

    assert path.exists()
    text = path.read_text()
    assert "System Overview" in text
    assert "Agent Workflow" in text
    assert "OpenAI Runtime Path" in text
    assert "Deterministic Fallback Path" in text


def test_architecture_doc_contains_mermaid_diagrams():
    text = Path("docs/ARCHITECTURE.md").read_text()

    assert text.count("```mermaid") >= 3
    assert "flowchart TD" in text
    assert "flowchart LR" in text


def test_readme_links_architecture_doc():
    text = Path("README.md").read_text()

    assert "docs/ARCHITECTURE.md" in text
