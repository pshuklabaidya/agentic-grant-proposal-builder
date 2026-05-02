# Agentic Grant Proposal Builder v0.1.0

## Summary

Initial portfolio-ready release of Agentic Grant Proposal Builder.

## Highlights

- Streamlit dashboard for grant proposal generation and review
- Upload support for funder guidance and source documents
- Local retrieval over grant guidance
- Funder-fit scoring
- Funder requirements extraction
- Proposal drafting
- Reviewer findings
- Budget narrative and line-item generation
- Proposal quality gate with readiness score
- Deterministic fallback mode without an API key
- Optional OpenAI Agents SDK path with tool-calling specialist agents
- Synthetic benchmark scenarios
- Evaluation report generation
- GitHub Actions CI
- Deployment guide and portfolio review brief

## Agents

- Intake Agent
- Retrieval Agent
- Fit Agent
- Funder Requirements Extractor Agent
- Grant Proposal Writer Agent
- Grant Reviewer Agent
- Budget Narrative Agent
- Proposal Quality Gate Agent

## Runtime Modes

The app works without an API key through deterministic fallback mode. When `OPENAI_API_KEY` is configured and `AGPB_USE_OPENAI_AGENTS=1`, the OpenAI-powered tool-calling agent path is used.

## Evaluation Artifacts

Release assets include generated evaluation reports:

- `evaluation_results.json`
- `evaluation_report.md`

## Safety Note

This application supports grant drafting and review. It does not guarantee eligibility, compliance, award likelihood, legal sufficiency, or funder acceptance.
