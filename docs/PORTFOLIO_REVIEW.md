# Portfolio Review Brief

## Project Summary

Agentic Grant Proposal Builder is an Agentic RAG application for grant proposal workflows. It converts funder guidance, applicant profiles, and source documents into a structured grant proposal package with retrieved evidence, funder-fit scoring, funder requirements, reviewer findings, budget planning, quality-gate review, and evaluation reports.

## Technical Highlights

- Streamlit dashboard
- Local document ingestion
- TF-IDF retrieval over uploaded or demo grant guidance
- Typed Pydantic models for proposal artifacts
- OpenAI Agents SDK path with tool-calling specialist agents
- Deterministic fallback mode without an API key
- Synthetic demo scenarios
- Evaluation harness
- JSON and Markdown report exports
- GitHub Actions CI

## Agent Workflow

| Stage | Role |
|---|---|
| Intake Agent | Structures applicant profile information |
| Retrieval Agent | Finds relevant guidance chunks |
| Fit Agent | Scores funder alignment |
| Funder Requirements Extractor Agent | Extracts eligibility and rubric requirements |
| Grant Proposal Writer Agent | Drafts proposal sections |
| Grant Reviewer Agent | Flags risks and weaknesses |
| Budget Narrative Agent | Creates line items and budget narrative |
| Proposal Quality Gate Agent | Produces readiness score and final review signal |

## OpenAI API Usage

The API key is optional.

When configured, OpenAI-powered agents run through the Agents SDK. When absent, deterministic fallback keeps the app usable, testable, and deployable for review.

## Evaluation Story

The repository includes synthetic grant scenarios under:

    sample_data/scenarios

The evaluation harness measures:

- Overall fit score
- Evidence count
- Extracted requirement count
- Reviewer finding count
- Compliance needs-review count
- Budget total agreement
- Quality status
- Quality readiness score
- Runtime path

Run:

    python -m agentic_grant_proposal_builder.evaluation

## Reviewer Talking Points

This project demonstrates the practical engineering pattern needed for production-facing AI systems: retrieval first, structured outputs, deterministic fallback, test coverage, runtime configuration, visible evidence, human-review gates, and repeatable evaluation.
