# Documentation Index

## Core Project Documents

- [README](../README.md)
- [Architecture](ARCHITECTURE.md)
- [Deployment Guide](../DEPLOYMENT.md)
- [Streamlit Deployment Checklist](STREAMLIT_DEPLOYMENT_CHECKLIST.md)
- [Portfolio Review Brief](PORTFOLIO_REVIEW.md)
- [Demo Walkthrough](DEMO_WALKTHROUGH.md)
- [Interview Talk Track](INTERVIEW_TALK_TRACK.md)
- [Scenario Guide](SCENARIOS.md)

## Local Commands

Install dependencies:

    make install

Run linting:

    make lint

Run tests:

    make test

Run evaluation:

    make eval

Run Streamlit smoke test:

    make smoke

Run all checks:

    make check

Run the dashboard:

    make run

## Main App Entrypoint

    src/agentic_grant_proposal_builder/app.py

## Evaluation Reports

Generated reports:

    reports/evaluation_results.json
    reports/evaluation_report.md

## Runtime Modes

Deterministic fallback mode runs without an OpenAI API key.

OpenAI Agents SDK mode runs when these values are configured:

    OPENAI_API_KEY
    AGPB_MODEL
    AGPB_USE_OPENAI_AGENTS=1

- [AI Usage And Limitations](AI_USAGE_AND_LIMITATIONS.md)
- [Human Review Checklist](HUMAN_REVIEW_CHECKLIST.md)
- [Security Policy](../SECURITY.md)

- [Contributing](../CONTRIBUTING.md)
- [Support](../SUPPORT.md)

- [License](../LICENSE)
- [Code Of Conduct](../CODE_OF_CONDUCT.md)

- [Repository Health Report](../reports/repo_health.md)

- [Changelog](../CHANGELOG.md)
- [Release Checklist](RELEASE_CHECKLIST.md)

- Version consistency script: `scripts/check_version.py`

- [Dependency Security](DEPENDENCY_SECURITY.md)
- Dependency audit script: `scripts/dependency_audit.py`

- [Docker](DOCKER.md)
- Docker smoke script: `scripts/docker_smoke.py`

- [Command Line Interface](CLI.md)
- CLI module: `src/agentic_grant_proposal_builder/cli.py`

- [CLI Examples](CLI_EXAMPLES.md)
- CLI smoke script: `scripts/cli_smoke.py`
- CLI sample profile: `sample_data/cli_example/profile.json`

- [JSON Schema Contracts](SCHEMAS.md)
- Schema export script: `scripts/export_schemas.py`
- Generated schemas: `reports/schemas/`

- [CI Artifacts](CI_ARTIFACTS.md)
- CI artifact bundle: generated reports and schemas

- [Publication Readiness](PUBLICATION_READINESS.md)
- Publication readiness script: `scripts/publication_readiness.py`
- Publication readiness report: `reports/publication_readiness.md`
