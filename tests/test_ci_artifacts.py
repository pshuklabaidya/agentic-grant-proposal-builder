from pathlib import Path


def test_ci_uploads_generated_reports_and_schemas():
    text = Path(".github/workflows/ci.yml").read_text()

    assert "Upload generated reports and schemas" in text
    assert "actions/upload-artifact@v4" in text
    assert "reports/evaluation_report.md" in text
    assert "reports/repo_health.md" in text
    assert "reports/dependency_audit.md" in text
    assert "reports/publication_readiness.md" in text
    assert "reports/schemas/" in text
    assert "retention-days: 14" in text


def test_ci_artifacts_doc_exists():
    path = Path("docs/CI_ARTIFACTS.md")

    assert path.exists()
    text = path.read_text()
    assert "CI Artifacts" in text
    assert "reports/schemas/" in text
    assert "generated-reports-and-schemas" in text


def test_readme_and_docs_index_link_ci_artifacts():
    readme = Path("README.md").read_text()
    docs_index = Path("docs/DOCS_INDEX.md").read_text()

    assert "docs/CI_ARTIFACTS.md" in readme
    assert "CI_ARTIFACTS.md" in docs_index
