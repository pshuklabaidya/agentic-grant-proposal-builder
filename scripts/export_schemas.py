from __future__ import annotations

import json
from pathlib import Path
from typing import TypeAlias

from pydantic import BaseModel

from agentic_grant_proposal_builder.evaluation import EvaluationResult, EvaluationScenario
from agentic_grant_proposal_builder.models import (
    FitScore,
    GrantDocument,
    OrganizationProfile,
    ProposalArtifact,
)
from agentic_grant_proposal_builder.workflow import (
    AgentStep,
    BudgetLineItem,
    BudgetPlan,
    ComplianceCheck,
    FunderRequirement,
    ProposalPackage,
    QualityCheck,
    QualityReport,
    ReviewerFinding,
)

ModelClass: TypeAlias = type[BaseModel]

SCHEMA_MODELS: list[ModelClass] = [
    GrantDocument,
    OrganizationProfile,
    ProposalArtifact,
    FitScore,
    AgentStep,
    FunderRequirement,
    ReviewerFinding,
    ComplianceCheck,
    BudgetLineItem,
    BudgetPlan,
    QualityCheck,
    QualityReport,
    ProposalPackage,
    EvaluationScenario,
    EvaluationResult,
]

SCHEMA_DIR = Path("reports/schemas")
DOC_PATH = Path("docs/SCHEMAS.md")


def schema_filename(model: ModelClass) -> str:
    return f"{model.__name__}.schema.json"


def write_schema_files(output_dir: Path = SCHEMA_DIR) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []

    for model in SCHEMA_MODELS:
        schema = model.model_json_schema()
        path = output_dir / schema_filename(model)
        path.write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n")
        paths.append(path)

    return paths


def write_schema_doc(schema_paths: list[Path], doc_path: Path = DOC_PATH) -> Path:
    doc_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# JSON Schema Contracts",
        "",
        "## Purpose",
        "",
        "These generated schema files document the typed contracts used by Agentic Grant Proposal Builder.",
        "",
        "They are useful for inspecting exported proposal packages, CLI outputs, evaluation reports, reviewer artifacts, budget plans, and quality-gate outputs.",
        "",
        "## Generated Files",
        "",
        "| Model | Schema File |",
        "|---|---|",
    ]

    for path in sorted(schema_paths):
        model_name = path.name.replace(".schema.json", "")
        lines.append(f"| {model_name} | `{path}` |")

    lines.extend(
        [
            "",
            "## Regeneration",
            "",
            "Run:",
            "",
            "    python scripts/export_schemas.py",
            "",
            "Or:",
            "",
            "    make schemas",
            "",
            "## Notes",
            "",
            "Schema files are generated from the Pydantic models used by the application, CLI, evaluation harness, and exported proposal package.",
            "",
        ]
    )

    doc_path.write_text("\n".join(lines))
    return doc_path


def main() -> int:
    schema_paths = write_schema_files()
    doc_path = write_schema_doc(schema_paths)

    print("JSON Schema contracts exported.")
    print("Schema directory:", SCHEMA_DIR)
    print("Schema doc:", doc_path)
    print("Schema count:", len(schema_paths))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
