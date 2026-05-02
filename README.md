# Agentic Grant Proposal Builder

[![CI](https://github.com/pshuklabaidya/agentic-grant-proposal-builder/actions/workflows/ci.yml/badge.svg)](https://github.com/pshuklabaidya/agentic-grant-proposal-builder/actions/workflows/ci.yml)

Agentic Grant Proposal Builder is a Streamlit application for grant proposal workflows. It combines document upload, local retrieval, funder-fit scoring, funder requirements extraction, proposal drafting, reviewer findings, budget planning, quality-gate checks, and evaluation reports.


## Repository

**Repository:** https://github.com/pshuklabaidya/agentic-grant-proposal-builder




## Documentation Index

Documentation index:

    docs/DOCS_INDEX.md

Scenario guide:

    docs/SCENARIOS.md

## Demo And Interview Materials

Demo walkthrough:

    docs/DEMO_WALKTHROUGH.md

Interview talk track:

    docs/INTERVIEW_TALK_TRACK.md

Architecture documentation:

    docs/ARCHITECTURE.md

## Architecture

Architecture documentation:

    docs/ARCHITECTURE.md

The architecture document includes Mermaid diagrams for the system overview, agent workflow, OpenAI runtime path, and deterministic fallback path.

## Core Agents

| Agent | Responsibility |
|---|---|
| Intake Agent | Normalizes applicant profile and project constraints |
| Retrieval Agent | Finds relevant grant guidance from uploaded source documents |
| Fit Agent | Scores mission, eligibility, evidence, budget, and implementation fit |
| Funder Requirements Extractor Agent | Extracts eligibility, rubric, budget, and evidence requirements |
| Grant Proposal Writer Agent | Produces proposal sections |
| Grant Reviewer Agent | Flags weaknesses and submission risks |
| Budget Narrative Agent | Creates budget line items and narrative |
| Proposal Quality Gate Agent | Evaluates readiness and unresolved risks |

## OpenAI API Use

When `OPENAI_API_KEY` exists and `AGPB_USE_OPENAI_AGENTS=1`, OpenAI-powered tool-calling agents run through the OpenAI Agents SDK path. Without a key, deterministic fallback remains active.

## Quickstart

    python -m venv .venv
    source .venv/bin/activate
    pip install -e ".[dev]"
    python -m pytest
    python -m agentic_grant_proposal_builder.evaluation
    streamlit run src/agentic_grant_proposal_builder/app.py

## Runtime Configuration

Copy `.env.example` or `.streamlit/secrets.toml.example`, then add the real key locally. Never commit secrets.

    OPENAI_API_KEY=your_key_here
    AGPB_MODEL=gpt-4.1-mini
    AGPB_USE_OPENAI_AGENTS=1
    OPENAI_AGENTS_DISABLE_TRACING=0


## Repository Health Report

Generate repository health reports:

    python scripts/repo_health.py

Generated outputs:

    reports/repo_health.json
    reports/repo_health.md

The health report checks expected portfolio, documentation, community, security, CI, deployment, and evaluation assets.

## Evaluation Harness

Synthetic scenarios live in `sample_data/scenarios`.

Run:

    python -m agentic_grant_proposal_builder.evaluation

Generated artifacts:

    reports/evaluation_results.json
    reports/evaluation_report.md


## Local Commands

    make install
    make lint
    make test
    make eval
    make smoke
    make check
    make run

## Continuous Integration

GitHub Actions runs package installation, Ruff, pytest, and the evaluation harness on push and pull request.

Workflow file:

    .github/workflows/ci.yml

The workflow uploads generated evaluation reports as CI artifacts.

## Deployment

Deployment instructions are in:

    DEPLOYMENT.md

Portfolio review notes are in:

    docs/PORTFOLIO_REVIEW.md



## Streamlit Smoke Test

The repository includes a local smoke test that starts the Streamlit app in headless mode and verifies that it responds.

    python scripts/smoke_streamlit.py

This is also included in:

    make check

## Streamlit Deployment

Deployment checklist:

    docs/STREAMLIT_DEPLOYMENT_CHECKLIST.md

Main app path:

    src/agentic_grant_proposal_builder/app.py

Required secrets belong in Streamlit Community Cloud secrets, not in the repository.


## AI Usage, Security, And Human Review

AI usage and limitations:

    docs/AI_USAGE_AND_LIMITATIONS.md

Human review checklist:

    docs/HUMAN_REVIEW_CHECKLIST.md

Security policy:

    SECURITY.md



## License And Conduct

License:

    LICENSE

Code of conduct:

    CODE_OF_CONDUCT.md

## Contributing And Support

Contributing guide:

    CONTRIBUTING.md

Support guide:

    SUPPORT.md

Issue forms and pull request template live under:

    .github/

## Safety

The app supports drafting and review only. It does not guarantee eligibility, compliance, award likelihood, legal sufficiency, or final funder acceptance.
