# Agentic Grant Proposal Builder

Agentic Grant Proposal Builder is a Streamlit application for grant proposal workflows. It combines document upload, local retrieval, funder-fit scoring, funder requirements extraction, proposal drafting, reviewer findings, budget planning, quality-gate checks, and evaluation reports.

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

## Evaluation Harness

Synthetic scenarios live in `sample_data/scenarios`.

Run:

    python -m agentic_grant_proposal_builder.evaluation

Generated artifacts:

    reports/evaluation_results.json
    reports/evaluation_report.md

## Safety

The app supports drafting and review only. It does not guarantee eligibility, compliance, award likelihood, legal sufficiency, or final funder acceptance.
