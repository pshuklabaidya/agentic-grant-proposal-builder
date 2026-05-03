# Dependency Security

## Purpose

Dependency security checks help keep the project reviewable and safer for public portfolio use.

## Dependabot

The repository includes:

    .github/dependabot.yml

Dependabot is configured for:

- Python package updates
- GitHub Actions updates

## pip-audit

The repository includes a local dependency-audit report script:

    scripts/dependency_audit.py

Run:

    python scripts/dependency_audit.py

Generated reports:

    reports/dependency_audit.json
    reports/dependency_audit.md

## Strict Mode

By default, the dependency audit writes reports and returns success so that portfolio CI remains stable even when upstream advisory databases change.

To fail when vulnerabilities are detected:

    AGPB_STRICT_DEPENDENCY_AUDIT=1 python scripts/dependency_audit.py

## Local Commands

Run the audit only:

    make audit

Run all checks:

    make check

## Review Guidance

When the audit reports vulnerabilities:

1. Review package name and installed version.
2. Review advisory ID.
3. Review fix versions.
4. Upgrade dependencies when compatible.
5. Rerun the full check suite.
