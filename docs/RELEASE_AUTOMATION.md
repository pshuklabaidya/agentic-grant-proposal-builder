# Release Automation

## Purpose

The release automation script creates a release plan, release notes, and a release manifest for the current package version.

The default mode is safe dry-run mode.

## Dry Run

Run:

    python scripts/create_release.py

Generated files:

    reports/release/release_notes_v0.1.0.md
    reports/release/release_manifest_v0.1.0.json

## Publish Release

Run only after all checks pass and GitHub CLI has release permission:

    python scripts/create_release.py --execute

The script will:

1. Create an annotated tag.
2. Push the tag to origin.
3. Create a GitHub release.
4. Attach generated reports and schema contract files.

## Included Assets

The release plan includes:

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
    CHANGELOG.md
    README.md

## Required Before Publishing

Run:

    make check

Confirm:

- Working tree is clean
- CI is passing
- Generated reports exist
- Schema files exist
- GitHub CLI has permission to create releases
