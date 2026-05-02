# Contributing

## Project Scope

Agentic Grant Proposal Builder is a portfolio project demonstrating Agentic RAG, OpenAI tool-calling agents, Streamlit UI, deterministic fallback behavior, quality gates, and evaluation reports.

## Local Setup

Create and activate a virtual environment:

    python -m venv .venv
    source .venv/bin/activate

Install dependencies:

    python -m pip install -e ".[dev]"

Run checks:

    make check

Run the dashboard:

    make run

## Development Workflow

1. Create a branch.
2. Make a focused change.
3. Run local checks.
4. Update docs or tests when behavior changes.
5. Open a pull request with a clear summary.

## Required Checks

Before opening a pull request, run:

    python -m ruff check .
    python -m pytest
    python -m agentic_grant_proposal_builder.evaluation
    python scripts/smoke_streamlit.py

Or run:

    make check

## AI And Safety Boundaries

Do not add behavior that claims final grant eligibility, legal compliance, financial compliance, award likelihood, or funder acceptance.

Generated proposal content must remain reviewable by humans.

## Secrets

Do not commit:

- `.env`
- `.streamlit/secrets.toml`
- API keys
- Access tokens
- Private grant documents
- Private applicant data

Use examples only:

- `.env.example`
- `.streamlit/secrets.toml.example`
