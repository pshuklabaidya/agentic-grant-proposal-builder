from pathlib import Path

from scripts import check_version


def test_version_check_script_exists():
    path = Path("scripts/check_version.py")

    assert path.exists()
    text = path.read_text()
    assert "Version consistency checks" in text
    assert "read_pyproject_version" in text


def test_version_values_match():
    pyproject_version = check_version.read_pyproject_version()
    package_version = check_version.read_package_version()

    assert pyproject_version == package_version
    assert check_version.semver_like(pyproject_version)


def test_changelog_and_release_checklist_contain_version():
    version = check_version.read_pyproject_version()

    assert check_version.changelog_contains_version(version)
    assert check_version.release_checklist_contains_version(version)


def test_version_check_main_passes():
    assert check_version.main() == 0


def test_makefile_and_ci_include_version_check():
    makefile = Path("Makefile").read_text()
    ci = Path(".github/workflows/ci.yml").read_text()

    assert "version:" in makefile
    assert "python scripts/check_version.py" in makefile
    assert "Run version consistency check" in ci
    assert "python scripts/check_version.py" in ci
