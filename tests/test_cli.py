import json
from pathlib import Path

from agentic_grant_proposal_builder import cli


def test_cli_parser_has_expected_commands():
    parser = cli.create_parser()
    help_text = parser.format_help()

    assert "list-scenarios" in help_text
    assert "build-scenario" in help_text
    assert "evaluate-scenario" in help_text
    assert "build-files" in help_text


def test_cli_list_scenarios_returns_known_scenarios():
    scenarios = cli.list_scenarios()
    scenario_ids = {scenario["scenario_id"] for scenario in scenarios}

    assert "education_access" in scenario_ids
    assert "rural_health" in scenario_ids
    assert "small_business_support" in scenario_ids


def test_cli_evaluate_scenario_returns_metrics():
    result = cli.evaluate_scenario("education_access")

    assert result["scenario_id"] == "education_access"
    assert result["overall_fit_score"] >= 0
    assert result["evidence_count"] >= 0


def test_cli_build_scenario_writes_artifacts(tmp_path):
    paths = cli.build_from_scenario("education_access", tmp_path)

    assert Path(paths["markdown"]).exists()
    assert Path(paths["json"]).exists()
    assert Path(paths["summary"]).exists()

    summary = json.loads(Path(paths["summary"]).read_text())
    assert summary["scenario_id"] == "education_access"


def test_cli_main_list_scenarios(capsys):
    status = cli.main(["list-scenarios"])
    captured = capsys.readouterr()

    assert status == 0
    assert "education_access" in captured.out


def test_pyproject_has_console_script():
    text = Path("pyproject.toml").read_text()

    assert "[project.scripts]" in text
    assert 'agpb = "agentic_grant_proposal_builder.cli:main"' in text


def test_readme_and_docs_index_link_cli():
    readme = Path("README.md").read_text()
    docs_index = Path("docs/DOCS_INDEX.md").read_text()

    assert "docs/CLI.md" in readme
    assert "CLI.md" in docs_index
