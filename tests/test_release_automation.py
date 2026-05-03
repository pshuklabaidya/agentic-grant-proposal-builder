from pathlib import Path

from scripts import create_release


def test_release_script_builds_plan():
    plan = create_release.build_release_plan("0.1.0")

    assert plan.version == "0.1.0"
    assert plan.tag == "v0.1.0"
    assert plan.repo == "pshuklabaidya/agentic-grant-proposal-builder"
    assert plan.commands
    assert any("gh" in command for command in plan.commands)


def test_release_notes_and_manifest_are_written():
    plan = create_release.build_release_plan("0.1.0")
    manifest = create_release.write_manifest(plan)

    assert Path(plan.release_notes).exists()
    assert manifest.exists()
    assert "Agentic Grant Proposal Builder v0.1.0" in Path(plan.release_notes).read_text()


def test_release_asset_list_includes_reports_and_schemas():
    assets = create_release.expected_assets()

    assert "reports/evaluation_report.md" in assets
    assert "reports/repo_health.md" in assets
    assert "docs/SCHEMAS.md" in assets


def test_release_automation_doc_exists():
    path = Path("docs/RELEASE_AUTOMATION.md")

    assert path.exists()
    text = path.read_text()
    assert "Dry Run" in text
    assert "Publish Release" in text
    assert "python scripts/create_release.py --execute" in text


def test_makefile_includes_release_targets():
    text = Path("Makefile").read_text()

    assert "release-plan:" in text
    assert "release-create:" in text
    assert "python scripts/create_release.py" in text


def test_readme_and_docs_index_link_release_automation():
    readme = Path("README.md").read_text()
    docs_index = Path("docs/DOCS_INDEX.md").read_text()

    assert "docs/RELEASE_AUTOMATION.md" in readme
    assert "RELEASE_AUTOMATION.md" in docs_index
