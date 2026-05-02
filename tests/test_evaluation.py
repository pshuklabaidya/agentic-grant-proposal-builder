from pathlib import Path

from agentic_grant_proposal_builder.evaluation import (
    load_scenarios,
    results_to_markdown,
    run_all_scenarios,
    write_evaluation_reports,
)


def test_load_scenarios_returns_demo_scenarios():
    scenarios = load_scenarios()

    assert len(scenarios) >= 3
    assert all(scenario.organization_profile.organization_name for scenario in scenarios)
    assert all(scenario.documents for scenario in scenarios)


def test_run_all_scenarios_returns_results_without_openai_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    results = run_all_scenarios()

    assert results
    assert all(result.overall_fit_score >= 0 for result in results)
    assert all(result.evidence_count >= 0 for result in results)


def test_results_to_markdown_contains_summary(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    results = run_all_scenarios()
    markdown = results_to_markdown(results)

    assert "Evaluation Report" in markdown
    assert "Summary Metrics" in markdown


def test_write_evaluation_reports_creates_files(tmp_path, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    results = run_all_scenarios()
    paths = write_evaluation_reports(results, output_dir=tmp_path)

    assert Path(paths["json"]).exists()
    assert Path(paths["markdown"]).exists()
