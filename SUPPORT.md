# Support

## Portfolio Project Status

This repository is a portfolio project. Support is limited to issues, documentation, and reproducible bug reports.

## Before Opening An Issue

Run:

    make check

Or run:

    python -m ruff check .
    python -m pytest
    python -m agentic_grant_proposal_builder.evaluation
    python scripts/smoke_streamlit.py

## Useful Issue Details

Include:

- Operating system
- Python version
- Command run
- Full traceback
- Whether `OPENAI_API_KEY` was configured
- Whether deterministic fallback or OpenAI Agents mode was active

Do not include secrets, private grant documents, or private applicant data.
