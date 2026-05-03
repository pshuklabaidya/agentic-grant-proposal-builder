# Publication Readiness

## Purpose

This checklist verifies that Agentic Grant Proposal Builder is ready to share as a public GitHub portfolio project and deploy through Streamlit Community Cloud.

## Required Local Checks

Run:

    make check

Or run key checks directly:

    python -m ruff check .
    python -m pytest
    python -m agentic_grant_proposal_builder.evaluation
    python scripts/export_schemas.py
    python scripts/check_version.py
    python scripts/dependency_audit.py
    python scripts/repo_health.py
    python scripts/publication_readiness.py

## Streamlit Deployment Values

Repository:

    https://github.com/pshuklabaidya/agentic-grant-proposal-builder

Branch:

    main

Main file path:

    src/agentic_grant_proposal_builder/app.py

Secrets belong in Streamlit Community Cloud secrets, not in the repository.

## Required Secrets

    OPENAI_API_KEY = "your_openai_api_key_here"
    AGPB_MODEL = "gpt-4.1-mini"
    AGPB_USE_OPENAI_AGENTS = "1"
    OPENAI_AGENTS_DISABLE_TRACING = "0"

## Suggested GitHub Topics

- agentic-rag
- openai-agents
- streamlit
- rag
- grant-writing
- llm-evaluation
- portfolio-project

## Generated Reports

    reports/publication_readiness.md
    reports/publication_readiness.json
