from pathlib import Path


def test_changelog_exists_and_has_baseline_version():
    path = Path("CHANGELOG.md")

    assert path.exists()
    text = path.read_text()
    assert "# Changelog" in text
    assert "## [Unreleased]" in text
    assert "## [0.1.0] - 2026-05-02" in text
    assert "Semantic Versioning" in text


def test_release_checklist_exists():
    path = Path("docs/RELEASE_CHECKLIST.md")

    assert path.exists()
    text = path.read_text()
    assert "Release Checklist" in text
    assert "make check" in text
    assert "Streamlit Deployment Review" in text
    assert "Final Safety Review" in text


def test_docs_index_links_changelog_and_release_checklist():
    text = Path("docs/DOCS_INDEX.md").read_text()

    assert "../CHANGELOG.md" in text
    assert "RELEASE_CHECKLIST.md" in text


def test_readme_links_changelog_and_release_checklist():
    text = Path("README.md").read_text()

    assert "CHANGELOG.md" in text
    assert "docs/RELEASE_CHECKLIST.md" in text
