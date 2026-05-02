# Streamlit Deployment Checklist

## Repository

Repository:

    https://github.com/pshuklabaidya/agentic-grant-proposal-builder

Branch:

    main

Main file path:

    src/agentic_grant_proposal_builder/app.py

## Required Secrets

Add these in Streamlit Community Cloud secrets:

    OPENAI_API_KEY = "your_openai_api_key_here"
    AGPB_MODEL = "gpt-4.1-mini"
    AGPB_USE_OPENAI_AGENTS = "1"
    OPENAI_AGENTS_DISABLE_TRACING = "0"

## Local Validation

Run before deployment:

    python -m pip install -e ".[dev]"
    python -m ruff check .
    python -m pytest
    python -m agentic_grant_proposal_builder.evaluation
    streamlit run src/agentic_grant_proposal_builder/app.py

## Expected App Behavior

The dashboard should show:

- OpenAI Runtime panel
- Applicant Profile form
- File uploader
- Build Proposal button
- Proposal Draft tab
- Funder Requirements tab
- Agent Trace tab
- Compliance tab
- Budget tab
- Reviewer Findings tab
- Quality Gate tab
- Evidence tab
- Benchmark tab
- Exports tab

## Runtime Modes

Without `OPENAI_API_KEY`, deterministic fallback mode runs.

With `OPENAI_API_KEY` and `AGPB_USE_OPENAI_AGENTS=1`, OpenAI-powered tool-calling agents run.

## Deployment Notes

Do not commit `.streamlit/secrets.toml`.

Use `.streamlit/secrets.toml.example` only as a template.
