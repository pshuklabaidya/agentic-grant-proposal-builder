# Architecture

## System Overview

Agentic Grant Proposal Builder is a Streamlit-first Agentic RAG application. It converts applicant profile data and grant guidance into a structured proposal package with evidence retrieval, funder-fit scoring, extracted funder requirements, proposal drafting, reviewer findings, budget planning, quality-gate review, and benchmark evaluation.

```mermaid
flowchart TD
    A[Applicant Profile] --> C[Pipeline]
    B[Uploaded Grant Guidance] --> D[Document Loader]
    D --> E[Local Retriever]
    E --> C
    C --> F[Fit Scoring]
    C --> G{OpenAI Agents Enabled?}
    G -->|No| H[Deterministic Fallback]
    G -->|Yes| I[OpenAI Tool-Calling Agents]
    H --> J[Proposal Package]
    I --> J[Proposal Package]
    J --> K[Streamlit Dashboard Tabs]
    J --> L[Markdown Export]
    J --> M[JSON Export]
    J --> N[Evaluation Reports]
```

## Agent Workflow

```mermaid
flowchart TD
    A[Intake Agent] --> B[Retrieval Agent]
    B --> C[Fit Agent]
    C --> D[Funder Requirements Extractor Agent]
    D --> E[Grant Proposal Writer Agent]
    E --> F[Grant Reviewer Agent]
    F --> G[Budget Narrative Agent]
    G --> H[Proposal Quality Gate Agent]
    H --> I[Export Agent]
```

## OpenAI Runtime Path

When `OPENAI_API_KEY` exists and `AGPB_USE_OPENAI_AGENTS=1`, the OpenAI-powered path activates. The application still performs local retrieval and funder-fit scoring before agent execution.

```mermaid
flowchart LR
    A[Local App State] --> B[Function Tools]
    B --> C[Funder Requirements Agent]
    B --> D[Proposal Writer Agent]
    B --> E[Reviewer Agent]
    B --> F[Budget Agent]
    B --> G[Quality Gate Agent]
    C --> H[Typed Pydantic Outputs]
    D --> H
    E --> H
    F --> H
    G --> H
    H --> I[Proposal Package]
```

## Deterministic Fallback Path

The app remains useful without an API key.

```mermaid
flowchart LR
    A[Applicant Profile] --> B[Local Retrieval]
    B --> C[Keyword Fit Scoring]
    C --> D[Deterministic Proposal Draft]
    D --> E[Deterministic Requirements]
    E --> F[Deterministic Reviewer Findings]
    F --> G[Deterministic Budget Plan]
    G --> H[Deterministic Quality Gate]
```

## Data Flow

1. Applicant profile fields are normalized into `OrganizationProfile`.
2. Uploaded text, Markdown, or PDF files are normalized into `GrantDocument`.
3. Source text is chunked and searched through local TF-IDF retrieval.
4. Retrieved evidence drives funder-fit scoring.
5. Agentic or deterministic proposal package generation runs.
6. The dashboard displays proposal, requirements, evidence, reviewer findings, quality gate, and exports.
7. The evaluation harness runs synthetic scenarios and writes JSON and Markdown reports.

## Safety And Review Boundaries

The system supports proposal drafting and review. It does not guarantee eligibility, legal compliance, funding likelihood, or funder acceptance. Human review remains required before submission.
