# Interview Talk Track

## Thirty-Second Version

Agentic Grant Proposal Builder is an Agentic RAG Streamlit application for grant-writing workflows. It ingests applicant profile data and funder guidance, retrieves relevant evidence, scores funder fit, extracts requirements, drafts a proposal, generates reviewer findings, builds a draft budget, runs a quality gate, and exports Markdown and JSON artifacts. It works with deterministic fallback and can also run OpenAI-powered tool-calling agents when an API key is configured.

## Two-Minute Version

This project demonstrates practical agentic AI engineering rather than a simple chatbot. The app starts with structured applicant data and source documents. It uses local retrieval to find relevant funder guidance, then applies funder-fit scoring and requirements extraction before drafting. The reviewer and quality-gate layers help prevent unsupported or submission-risky output.

The OpenAI path uses specialist agents for requirements extraction, proposal drafting, reviewer findings, budget planning, and quality review. The deterministic fallback path keeps the project testable and demoable without an API key. The evaluation harness runs synthetic grant scenarios and produces repeatable reports.

The portfolio value is that the project shows end-to-end applied AI: dashboard, retrieval, structured outputs, agent orchestration, fallback behavior, evaluation, CI, deployment docs, and human-review safeguards.

## Technical Talking Points

### Streamlit

The dashboard supports applicant profile entry, document upload, proposal generation, review tabs, benchmark results, and exports.

### Retrieval

Source documents are normalized into `GrantDocument`, chunked, and searched through a local TF-IDF retriever.

### OpenAI Agents

The OpenAI path activates when `OPENAI_API_KEY` exists and `AGPB_USE_OPENAI_AGENTS=1`.

Specialist agents include:

- Funder Requirements Extractor Agent
- Grant Proposal Writer Agent
- Grant Reviewer Agent
- Budget Narrative Agent
- Proposal Quality Gate Agent

### Deterministic Fallback

The app still works without an API key. That design supports reliable demos, CI, and local testing.

### Evaluation

Synthetic scenarios under `sample_data/scenarios` run through the same pipeline as the app. Reports are written to `reports/evaluation_results.json` and `reports/evaluation_report.md`.

### Safety

The app does not claim final eligibility, compliance, or funding success. It produces reviewable artifacts with evidence, risks, and quality checks.

## Recruiter-Friendly Framing

This project shows the ability to build AI applications that are useful, testable, reviewable, and deployable. It combines product thinking with software engineering: users get a dashboard, reviewers get evidence and risk checks, developers get CI and tests, and hiring managers get a clear demonstration of Agentic RAG capability.

## Technical Interview Framing

The key design choice was separating deterministic application logic from optional LLM-powered agents. Retrieval, scoring, quality checks, and evaluation remain testable. OpenAI agents are used where judgment and drafting are valuable. This prevents the system from becoming an opaque prompt-only application.

## Extension Ideas

Future versions could add:

- Real vector database retrieval
- Better PDF table extraction
- Citation-backed proposal paragraphs
- Funder rubric scoring
- Human approval gates
- Multi-user project persistence
- DOCX and PDF exports
- Authenticated deployment
