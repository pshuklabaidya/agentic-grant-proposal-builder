# JSON Schema Contracts

## Purpose

These generated schema files document the typed contracts used by Agentic Grant Proposal Builder.

They are useful for inspecting exported proposal packages, CLI outputs, evaluation reports, reviewer artifacts, budget plans, and quality-gate outputs.

## Generated Files

| Model | Schema File |
|---|---|
| AgentStep | `reports/schemas/AgentStep.schema.json` |
| BudgetLineItem | `reports/schemas/BudgetLineItem.schema.json` |
| BudgetPlan | `reports/schemas/BudgetPlan.schema.json` |
| ComplianceCheck | `reports/schemas/ComplianceCheck.schema.json` |
| EvaluationResult | `reports/schemas/EvaluationResult.schema.json` |
| EvaluationScenario | `reports/schemas/EvaluationScenario.schema.json` |
| FitScore | `reports/schemas/FitScore.schema.json` |
| FunderRequirement | `reports/schemas/FunderRequirement.schema.json` |
| GrantDocument | `reports/schemas/GrantDocument.schema.json` |
| OrganizationProfile | `reports/schemas/OrganizationProfile.schema.json` |
| ProposalArtifact | `reports/schemas/ProposalArtifact.schema.json` |
| ProposalPackage | `reports/schemas/ProposalPackage.schema.json` |
| QualityCheck | `reports/schemas/QualityCheck.schema.json` |
| QualityReport | `reports/schemas/QualityReport.schema.json` |
| ReviewerFinding | `reports/schemas/ReviewerFinding.schema.json` |

## Regeneration

Run:

    python scripts/export_schemas.py

Or:

    make schemas

## Notes

Schema files are generated from the Pydantic models used by the application, CLI, evaluation harness, and exported proposal package.
