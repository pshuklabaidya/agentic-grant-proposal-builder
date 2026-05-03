# CI Artifacts

## Purpose

The CI workflow publishes generated reports and JSON Schema contracts as GitHub Actions artifacts. This gives reviewers access to validation outputs from each workflow run without requiring local execution.

## Uploaded Artifacts

The workflow uploads:

    reports/evaluation_results.json
    reports/evaluation_report.md
    reports/repo_health.json
    reports/repo_health.md
    reports/dependency_audit.json
    reports/dependency_audit.md
    reports/publication_readiness.json
    reports/publication_readiness.md
    reports/schemas/
    docs/SCHEMAS.md

## Artifact Name

The workflow names the bundle by Python version:

    generated-reports-and-schemas-python-${{ matrix.python-version }}

## Retention

The artifact retention period is set to 14 days.

## Local Regeneration

Run:

    python -m agentic_grant_proposal_builder.evaluation
    python scripts/export_schemas.py
    python scripts/check_version.py
    python scripts/dependency_audit.py
    python scripts/repo_health.py
    python scripts/publication_readiness.py

Or run:

    make check
