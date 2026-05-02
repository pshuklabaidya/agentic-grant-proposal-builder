# AI Usage And Limitations

## Purpose

Agentic Grant Proposal Builder supports grant proposal drafting, review, budget planning, and quality checks. It is designed as a portfolio-ready Agentic RAG application, not as a final grant-submission authority.

## OpenAI Usage

The app has two runtime paths.

### Deterministic Fallback Path

When no OpenAI API key is configured, the app still runs. Local Python logic handles:

- Document loading
- Text chunking
- TF-IDF retrieval
- Funder-fit scoring
- Deterministic proposal drafting
- Requirements extraction fallback
- Reviewer findings fallback
- Budget plan fallback
- Quality-gate fallback
- Evaluation harness

### OpenAI Agents Path

When `OPENAI_API_KEY` exists and `AGPB_USE_OPENAI_AGENTS=1`, OpenAI-powered tool-calling agents can run.

The OpenAI-powered agents are:

- Funder Requirements Extractor Agent
- Grant Proposal Writer Agent
- Grant Reviewer Agent
- Budget Narrative Agent
- Proposal Quality Gate Agent

## Local Tools Exposed To Agents

The OpenAI-powered path exposes controlled local tool outputs, not arbitrary filesystem access.

Tool-style data includes:

- Applicant profile JSON
- Retrieved evidence text
- Funder-fit score JSON
- Evidence source summaries
- Deterministic budget baseline

## Review Boundaries

The app does not guarantee:

- Applicant eligibility
- Legal compliance
- Financial compliance
- Grant award likelihood
- Funder acceptance
- Final budget allowability
- Accuracy of uploaded source documents
- Completeness of extracted requirements

Human review remains required before any real-world submission.

## Evidence Boundaries

Retrieved evidence is shown in the dashboard so reviewers can inspect source support.

Generated narrative should be checked against:

- Full funder instructions
- Eligibility criteria
- Scoring rubric
- Budget allowability rules
- Submission format
- Required attachments
- Deadlines
- Organizational approvals

## Recommended Review Workflow

1. Upload the full funder guidance.
2. Build the proposal package.
3. Inspect retrieved evidence.
4. Review extracted funder requirements.
5. Compare proposal sections against high-priority requirements.
6. Resolve reviewer findings.
7. Inspect budget line items.
8. Review quality-gate output.
9. Export Markdown and JSON.
10. Complete human review before submission.

## Portfolio Interpretation

This project demonstrates applied AI engineering patterns:

- Retrieval before generation
- Structured outputs
- Tool-calling agents
- Deterministic fallback
- Human-review gates
- Evaluation scenarios
- Exportable artifacts
- CI validation
- Deployment documentation
