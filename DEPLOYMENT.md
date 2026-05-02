# Deployment Guide

## Streamlit Community Cloud

This project is designed to run as a Streamlit app.

Main app file:

    src/agentic_grant_proposal_builder/app.py

Recommended deployment command:

    streamlit run src/agentic_grant_proposal_builder/app.py

## Required Repository Files

The repository should include:

    pyproject.toml
    README.md
    src/agentic_grant_proposal_builder/app.py
    sample_data/scenarios/
    .streamlit/config.toml

## Secrets

Do not commit real secrets.

For local development, copy:

    cp .streamlit/secrets.toml.example .streamlit/secrets.toml

Then add:

    OPENAI_API_KEY = "your_openai_api_key_here"
    AGPB_MODEL = "gpt-4.1-mini"
    AGPB_USE_OPENAI_AGENTS = "1"
    OPENAI_AGENTS_DISABLE_TRACING = "0"

For Streamlit Community Cloud, add the same values in the app secrets management interface.

## Runtime Modes

### Deterministic Fallback

When no API key is configured, the app still runs with local deterministic proposal, review, budget, quality-gate, and evaluation behavior.

### OpenAI Agents Mode

When `OPENAI_API_KEY` exists and `AGPB_USE_OPENAI_AGENTS=1`, the app uses OpenAI-powered tool-calling agents for requirements extraction, proposal drafting, review, budget planning, and quality-gate output.

## Local Validation

Run:

    make install
    make check

Or run directly:

    python -m pip install -e ".[dev]"
    python -m ruff check .
    python -m pytest
    python -m agentic_grant_proposal_builder.evaluation

## Generated Reports

The evaluation harness writes:

    reports/evaluation_results.json
    reports/evaluation_report.md

These reports are useful for portfolio review and CI artifacts.
