from pathlib import Path

from scripts import publication_readiness


def test_publication_readiness_doc_exists():
    path = Path("docs/PUBLICATION_READINESS.md")

    assert path.exists()
    text = path.read_text()
    assert "Streamlit Deployment Values" in text
    assert "Suggested GitHub Topics" in text
    assert "OPENAI_API_KEY" in text


def test_publication_readiness_script_exists():
    path = Path("scripts/publication_readiness.py")

    assert path.exists()
    text = path.read_text()
    assert "EXPECTED_TOPICS" in text
    assert "STREAMLIT_APP_PATH" in text
    assert "publication_readiness.md" in text


def test_publication_deployment_values():
    values = publication_readiness.deployment_values()

    assert values["Branch"] == "main"
    assert values["Main file path"] == "src/agentic_grant_proposal_builder/app.py"


def test_publication_suggested_topic_command():
    command = publication_readiness.suggested_topic_command()

    assert "gh repo edit" in command
    assert "agentic-rag" in command
    assert "openai-agents" in command
    assert "portfolio-project" in command


def test_readme_and_docs_index_link_publication_readiness():
    readme = Path("README.md").read_text()
    docs_index = Path("docs/DOCS_INDEX.md").read_text()

    assert "docs/PUBLICATION_READINESS.md" in readme
    assert "PUBLICATION_READINESS.md" in docs_index
