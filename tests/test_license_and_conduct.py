from pathlib import Path


def test_license_exists_and_is_mit():
    path = Path("LICENSE")

    assert path.exists()
    text = path.read_text()
    assert "MIT License" in text
    assert "Prashant Shuklabaidya" in text
    assert "Permission is hereby granted" in text


def test_code_of_conduct_exists():
    path = Path("CODE_OF_CONDUCT.md")

    assert path.exists()
    text = path.read_text()
    assert "Code Of Conduct" in text
    assert "Expected Behavior" in text
    assert "Unacceptable Behavior" in text
    assert "AI-Specific Expectations" in text


def test_docs_index_links_license_and_conduct():
    text = Path("docs/DOCS_INDEX.md").read_text()

    assert "../LICENSE" in text
    assert "../CODE_OF_CONDUCT.md" in text


def test_readme_links_license_and_conduct():
    text = Path("README.md").read_text()

    assert "LICENSE" in text
    assert "CODE_OF_CONDUCT.md" in text
