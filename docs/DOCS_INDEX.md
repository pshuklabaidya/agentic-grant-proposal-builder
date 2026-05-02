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
