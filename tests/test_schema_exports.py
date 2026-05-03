import json
from pathlib import Path

from scripts import export_schemas


def test_schema_export_script_defines_expected_models():
    model_names = {model.__name__ for model in export_schemas.SCHEMA_MODELS}

    assert "OrganizationProfile" in model_names
    assert "ProposalArtifact" in model_names
    assert "ProposalPackage" in model_names
    assert "EvaluationResult" in model_names


def test_schema_files_are_written(tmp_path):
    paths = export_schemas.write_schema_files(tmp_path)

    assert paths
    assert (tmp_path / "OrganizationProfile.schema.json").exists()
    assert (tmp_path / "ProposalPackage.schema.json").exists()

    payload = json.loads((tmp_path / "OrganizationProfile.schema.json").read_text())
    assert payload["title"] == "OrganizationProfile"
    assert "properties" in payload


def test_schema_doc_is_written(tmp_path):
    schema_dir = tmp_path / "schemas"
    doc_path = tmp_path / "SCHEMAS.md"

    paths = export_schemas.write_schema_files(schema_dir)
    export_schemas.write_schema_doc(paths, doc_path)

    text = doc_path.read_text()
    assert "JSON Schema Contracts" in text
    assert "OrganizationProfile.schema.json" in text
    assert "ProposalPackage.schema.json" in text


def test_schema_export_main_writes_default_outputs():
    assert export_schemas.main() == 0
    assert Path("docs/SCHEMAS.md").exists()
    assert Path("reports/schemas/OrganizationProfile.schema.json").exists()
    assert Path("reports/schemas/ProposalPackage.schema.json").exists()


def test_makefile_and_ci_include_schema_export():
    makefile = Path("Makefile").read_text()
    ci = Path(".github/workflows/ci.yml").read_text()

    assert "schemas:" in makefile
    assert "python scripts/export_schemas.py" in makefile
    assert "Export JSON Schema contracts" in ci
    assert "python scripts/export_schemas.py" in ci


def test_readme_and_docs_index_link_schemas():
    readme = Path("README.md").read_text()
    docs_index = Path("docs/DOCS_INDEX.md").read_text()

    assert "docs/SCHEMAS.md" in readme
    assert "SCHEMAS.md" in docs_index
