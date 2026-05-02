# Release Checklist

## Purpose

This checklist keeps releases consistent, reviewable, and portfolio-ready.

## Before Release

Run local checks:

    make check

Or run each command:

    python -m ruff check .
    python -m pytest
    python -m agentic_grant_proposal_builder.evaluation
    python scripts/repo_health.py
    python scripts/smoke_streamlit.py

## Version Review

Confirm version consistency in:

    pyproject.toml
    src/agentic_grant_proposal_builder/__init__.py
    CHANGELOG.md

Current baseline version:

    0.1.0

## Documentation Review

Confirm the following files exist and are current:

    README.md
    CHANGELOG.md
    DEPLOYMENT.md
    SECURITY.md
    CONTRIBUTING.md
    SUPPORT.md
    CODE_OF_CONDUCT.md
    LICENSE
    docs/DOCS_INDEX.md
    docs/ARCHITECTURE.md
    docs/DEMO_WALKTHROUGH.md
    docs/INTERVIEW_TALK_TRACK.md
    docs/AI_USAGE_AND_LIMITATIONS.md
    docs/HUMAN_REVIEW_CHECKLIST.md
    docs/SCENARIOS.md
    docs/STREAMLIT_DEPLOYMENT_CHECKLIST.md
    docs/PORTFOLIO_REVIEW.md

## Generated Reports

Regenerate:

    python -m agentic_grant_proposal_builder.evaluation
    python scripts/repo_health.py

Expected report files:

    reports/evaluation_results.json
    reports/evaluation_report.md
    reports/repo_health.json
    reports/repo_health.md

## GitHub Release

Create or update a tag:

    git tag -a v0.1.0 -m "Agentic Grant Proposal Builder v0.1.0"
    git push origin v0.1.0

Create a GitHub release and attach:

    reports/evaluation_results.json
    reports/evaluation_report.md
    reports/repo_health.json
    reports/repo_health.md

## Streamlit Deployment Review

Deployment values:

    Repository: https://github.com/pshuklabaidya/agentic-grant-proposal-builder
    Branch: main
    Main file path: src/agentic_grant_proposal_builder/app.py

Secrets:

    OPENAI_API_KEY = "your_openai_api_key_here"
    AGPB_MODEL = "gpt-4.1-mini"
    AGPB_USE_OPENAI_AGENTS = "1"
    OPENAI_AGENTS_DISABLE_TRACING = "0"

## Final Safety Review

Confirm:

- No `.env` file committed
- No `.streamlit/secrets.toml` file committed
- No API key committed
- No private grant documents committed
- No private applicant data committed
- Human review boundary remains documented
- App does not claim eligibility, compliance, award likelihood, or funder acceptance
