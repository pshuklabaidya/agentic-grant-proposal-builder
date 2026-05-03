from pathlib import Path

from scripts import cli_smoke


def test_cli_example_files_exist():
    assert Path("sample_data/cli_example/profile.json").exists()
    assert Path("sample_data/cli_example/funder_guidance.txt").exists()
    assert Path("sample_data/cli_example/program_notes.txt").exists()


def test_cli_examples_doc_exists():
    path = Path("docs/CLI_EXAMPLES.md")

    assert path.exists()
    text = path.read_text()
    assert "agpb build-files" in text
    assert "python scripts/cli_smoke.py" in text
    assert "sample_data/cli_example/profile.json" in text


def test_cli_smoke_script_exists():
    path = Path("scripts/cli_smoke.py")

    assert path.exists()
    text = path.read_text()
    assert "build-scenario" in text
    assert "build-files" in text


def test_cli_smoke_main_runs_after_install():
    assert cli_smoke.main() == 0


def test_makefile_and_ci_include_cli_smoke():
    makefile = Path("Makefile").read_text()
    ci = Path(".github/workflows/ci.yml").read_text()

    assert "cli-smoke:" in makefile
    assert "python scripts/cli_smoke.py" in makefile
    assert "Run CLI smoke test" in ci
    assert "python scripts/cli_smoke.py" in ci


def test_readme_and_docs_index_link_cli_examples():
    readme = Path("README.md").read_text()
    docs_index = Path("docs/DOCS_INDEX.md").read_text()

    assert "docs/CLI_EXAMPLES.md" in readme
    assert "CLI_EXAMPLES.md" in docs_index
