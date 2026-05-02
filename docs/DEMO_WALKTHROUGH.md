# Demo Walkthrough

## Demo Goal

Show how Agentic Grant Proposal Builder turns applicant information and grant guidance into a structured proposal package with evidence retrieval, funder-fit scoring, requirements extraction, reviewer findings, budget planning, quality-gate review, and exportable artifacts.

## Local Startup

Run:

    source .venv/bin/activate
    make check
    make run

Or run directly:

    python -m pip install -e ".[dev]"
    python -m ruff check .
    python -m pytest
    python -m agentic_grant_proposal_builder.evaluation
    streamlit run src/agentic_grant_proposal_builder/app.py

## Opening Narrative

Agentic Grant Proposal Builder is an Agentic RAG application for grant-writing workflows. It combines local retrieval, deterministic scoring, optional OpenAI tool-calling agents, reviewer checks, budget planning, quality gates, and evaluation reports.

The app is designed to work with or without an OpenAI API key. Without the key, deterministic fallback makes the app demoable and testable. With the key, the OpenAI Agents SDK path activates specialist agents for requirements extraction, proposal drafting, review, budget planning, and quality-gate evaluation.

## Dashboard Walkthrough

### 1. OpenAI Runtime Panel

Show the sidebar runtime section.

Explain:

- API key detected
- Key source
- Model
- Agent SDK mode
- Tracing disabled
- Runtime path

The key point is that the runtime mode is transparent. Reviewers can see whether the OpenAI-powered path or deterministic fallback path is active.

### 2. Applicant Profile

Show the applicant profile form.

Explain that profile fields become a structured `OrganizationProfile` object. The proposal generation process does not rely on loose chat text only. It uses typed application state.

### 3. Source Document Upload

Show the file uploader.

Explain that uploaded PDF, text, or Markdown files become `GrantDocument` objects. Source text is chunked and searched by the local retrieval layer.

Demo option:

- Leave the uploader empty to use sample guidance.
- Upload a small synthetic funder guideline file to show document ingestion.

### 4. Build Proposal

Click:

    Build Proposal

Explain that the pipeline runs these stages:

1. Intake
2. Document loading
3. Local retrieval
4. Funder-fit scoring
5. Requirements extraction
6. Proposal drafting
7. Reviewer findings
8. Budget planning
9. Quality gate
10. Export packaging

### 5. Proposal Draft Tab

Show the generated proposal draft.

Call out:

- Executive summary
- Need statement
- Project design
- Outcomes
- Budget narrative
- Evaluation plan
- Sustainability
- Funder alignment

### 6. Funder Requirements Tab

Show the structured requirements table.

Explain that funder guidance is converted into reviewer-friendly requirement rows:

- Eligibility
- Required sections
- Budget rules
- Evaluation expectations
- Sustainability expectations

### 7. Agent Trace Tab

Show the workflow trace.

Explain that this gives reviewers visibility into which logical agents ran and what each produced.

### 8. Compliance Tab

Show compliance checks.

Explain that the app highlights guidance terms found in retrieved evidence and marks missing areas as needing review.

### 9. Budget Tab

Show budget line items.

Explain that the budget plan is a draft allocation and not a final finance-approved budget. It helps reviewers inspect whether line items match the total request.

### 10. Reviewer Findings Tab

Show findings.

Explain that this is the red-team layer. It flags weak need statements, missing evidence, low fit, unresolved risks, and requirements that need explicit proposal coverage.

### 11. Quality Gate Tab

Show readiness score and checks.

Explain that the quality gate does not approve submission. It provides a structured revision signal before human review.

### 12. Evidence Tab

Show retrieved chunks.

Explain that generated content remains reviewable because evidence snippets are visible.

### 13. Benchmark Tab

Show synthetic evaluation results.

Explain that the app includes repeatable scenarios, not only one-off demos.

### 14. Exports Tab

Show download buttons.

Explain that the proposal can be exported as Markdown and the full package can be exported as JSON.

## Strong Demo Path

1. Start with no uploaded files and build the sample proposal.
2. Show runtime panel.
3. Show proposal draft.
4. Show funder requirements.
5. Show quality gate.
6. Show benchmark tab.
7. Download Markdown and JSON.
8. Open `reports/evaluation_report.md` in the repo.

## Risk Boundaries

The app does not guarantee:

- Grant eligibility
- Legal compliance
- Financial compliance
- Award likelihood
- Final funder acceptance

The app supports drafting, review, and evidence-grounded preparation.
