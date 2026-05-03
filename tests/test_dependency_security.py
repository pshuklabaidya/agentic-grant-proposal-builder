from pathlib import Path

from scripts import dependency_audit


def test_dependabot_config_exists():
    path = Path(".github/dependabot.yml")

    assert path.exists()
    text = path.read_text()
    assert 'package-ecosystem: "pip"' in text
    assert 'package-ecosystem: "github-actions"' in text


def test_dependency_audit_script_exists():
    path = Path("scripts/dependency_audit.py")

    assert path.exists()
    text = path.read_text()
    assert "run_pip_audit" in text
    assert "AGPB_STRICT_DEPENDENCY_AUDIT" in text


def test_dependency_audit_report_helpers_parse_empty_payload():
    rows = dependency_audit.vulnerability_rows({"dependencies": []})

    assert rows == []


def test_dependency_security_doc_exists():
    path = Path("docs/DEPENDENCY_SECURITY.md")

    assert path.exists()
    text = path.read_text()
    assert "Dependabot" in text
    assert "pip-audit" in text
    assert "Strict Mode" in text


def test_makefile_and_ci_include_dependency_audit():
    makefile = Path("Makefile").read_text()
    ci = Path(".github/workflows/ci.yml").read_text()

    assert "audit:" in makefile
    assert "python scripts/dependency_audit.py" in makefile
    assert "Run dependency audit report" in ci
    assert "python scripts/dependency_audit.py" in ci


def test_readme_and_docs_index_link_dependency_security():
    readme = Path("README.md").read_text()
    docs_index = Path("docs/DOCS_INDEX.md").read_text()

    assert "docs/DEPENDENCY_SECURITY.md" in readme
    assert "DEPENDENCY_SECURITY.md" in docs_index
