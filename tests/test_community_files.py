from pathlib import Path


def test_contributing_guide_exists():
    path = Path("CONTRIBUTING.md")

    assert path.exists()
    text = path.read_text()
    assert "Local Setup" in text
    assert "Required Checks" in text
    assert "Secrets" in text


def test_support_doc_exists():
    path = Path("SUPPORT.md")

    assert path.exists()
    text = path.read_text()
    assert "Portfolio Project Status" in text
    assert "Before Opening An Issue" in text


def test_issue_forms_exist():
    bug = Path(".github/ISSUE_TEMPLATE/bug_report.yml")
    feature = Path(".github/ISSUE_TEMPLATE/feature_request.yml")
    config = Path(".github/ISSUE_TEMPLATE/config.yml")

    assert bug.exists()
    assert feature.exists()
    assert config.exists()

    bug_text = bug.read_text()
    feature_text = feature.read_text()
    config_text = config.read_text()

    assert "name: Bug Report" in bug_text
    assert "name: Feature Request" in feature_text
    assert "blank_issues_enabled: false" in config_text


def test_pull_request_template_exists():
    path = Path(".github/pull_request_template.md")

    assert path.exists()
    text = path.read_text()
    assert "AI And Safety Review" in text
    assert "python -m pytest" in text


def test_readme_links_contributing_and_support():
    text = Path("README.md").read_text()

    assert "CONTRIBUTING.md" in text
    assert "SUPPORT.md" in text
