import json
from pathlib import Path

from scripts import repo_health


def test_repo_health_script_exists():
    path = Path("scripts/repo_health.py")

    assert path.exists()
    text = path.read_text()
    assert "REQUIRED_FILES" in text
    assert "Repository Health Report" in text


def test_repo_health_builds_checks():
    checks = []
    checks.extend(repo_health.check_required_files())
    checks.extend(repo_health.check_readme_content())
    checks.extend(repo_health.check_gitignore())
    checks.extend(repo_health.check_ci_content())

    assert checks
    assert all(check.name for check in checks)


def test_repo_health_writes_reports(tmp_path, monkeypatch):
    monkeypatch.chdir(Path.cwd())

    status = repo_health.main()

    assert status in {0, 1}
    assert Path("reports/repo_health.json").exists()
    assert Path("reports/repo_health.md").exists()

    payload = json.loads(Path("reports/repo_health.json").read_text())
    assert isinstance(payload, list)
    assert payload
    assert {"name", "status", "details"}.issubset(payload[0].keys())


def test_makefile_includes_health_target():
    text = Path("Makefile").read_text()

    assert "health:" in text
    assert "python scripts/repo_health.py" in text


def test_ci_includes_health_report_step():
    text = Path(".github/workflows/ci.yml").read_text()

    assert "Run repository health report" in text
    assert "python scripts/repo_health.py" in text
