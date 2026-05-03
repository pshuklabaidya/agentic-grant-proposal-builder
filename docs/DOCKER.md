# Docker

## Purpose

Docker packaging provides a portable way to run Agentic Grant Proposal Builder outside the local virtual environment.

## Build

    docker build -t agentic-grant-proposal-builder:local .

## Run

    docker run --rm -p 8501:8501 agentic-grant-proposal-builder:local

Open:

    http://localhost:8501

## Smoke Test

Run:

    python scripts/docker_smoke.py

The smoke test builds the image, starts the container, checks that Streamlit responds, and removes the container.

If Docker is unavailable, the smoke script skips cleanly.

## Secrets

Do not bake secrets into the image.

Pass secrets through runtime environment variables:

    docker run --rm -p 8501:8501 \
      -e OPENAI_API_KEY="your_openai_api_key_here" \
      -e AGPB_MODEL="gpt-4.1-mini" \
      -e AGPB_USE_OPENAI_AGENTS="1" \
      -e OPENAI_AGENTS_DISABLE_TRACING="0" \
      agentic-grant-proposal-builder:local

## Files Excluded From Build Context

The `.dockerignore` file excludes local development artifacts, virtual environments, generated reports, cache directories, backups, and secret files.

Key exclusions:

    .env
    .streamlit/secrets.toml
    .venv
    reports
    __pycache__
    .pytest_cache
    .ruff_cache
