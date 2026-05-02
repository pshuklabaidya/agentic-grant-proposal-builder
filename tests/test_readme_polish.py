from pathlib import Path


def test_readme_has_ci_badge_and_project_snapshot():
    text = Path("README.md").read_text()

    assert "actions/workflows/ci.yml/badge.svg" in text
    assert "## Project Snapshot" in text
    assert "Agentic RAG application" in text


def test_readme_has_quick_navigation_links():
    text = Path("README.md").read_text()

    assert "## Quick Navigation" in text
    assert "[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)" in text
    assert "[docs/DEMO_WALKTHROUGH.md](docs/DEMO_WALKTHROUGH.md)" in text
    assert "[docs/DOCS_INDEX.md](docs/DOCS_INDEX.md)" in text


def test_readme_has_fast_local_validation():
    text = Path("README.md").read_text()

    assert "## Fast Local Validation" in text
    assert "make check" in text
    assert "python scripts/check_version.py" in text
    assert "python scripts/repo_health.py" in text
