# Publication Readiness Report

Repository: https://github.com/pshuklabaidya/agentic-grant-proposal-builder
Total checks: 27
Passed: 25
Warnings: 2
Failed: 0

## Streamlit Deployment Values

- Repository: https://github.com/pshuklabaidya/agentic-grant-proposal-builder
- Branch: main
- Main file path: src/agentic_grant_proposal_builder/app.py
- OpenAI secrets location: Streamlit Community Cloud secrets
- Local app command: streamlit run src/agentic_grant_proposal_builder/app.py

## Suggested Repository Topics

agentic-rag, openai-agents, streamlit, rag, grant-writing, llm-evaluation, portfolio-project

## Optional GitHub Metadata Command

Run only after GitHub CLI authentication has repository administration permission:

    gh repo edit pshuklabaidya/agentic-grant-proposal-builder --description "Agentic RAG grant proposal builder with OpenAI tool-calling agents, Streamlit dashboard, quality gates, and evaluation reports." --add-topic "agentic-rag" --add-topic "openai-agents" --add-topic "streamlit" --add-topic "rag" --add-topic "grant-writing" --add-topic "llm-evaluation" --add-topic "portfolio-project"

## Checks

| Check | Status | Details |
|---|---:|---|
| file:README.md | pass | found |
| file:CHANGELOG.md | pass | found |
| file:LICENSE | pass | found |
| file:CODE_OF_CONDUCT.md | pass | found |
| file:CONTRIBUTING.md | pass | found |
| file:SUPPORT.md | pass | found |
| file:SECURITY.md | pass | found |
| file:DEPLOYMENT.md | pass | found |
| file:Dockerfile | pass | found |
| file:.github/workflows/ci.yml | pass | found |
| file:.github/dependabot.yml | pass | found |
| file:.streamlit/config.toml | pass | found |
| file:.streamlit/secrets.toml.example | pass | found |
| file:src/agentic_grant_proposal_builder/app.py | pass | found |
| file:docs/DOCS_INDEX.md | pass | found |
| file:docs/ARCHITECTURE.md | pass | found |
| file:docs/STREAMLIT_DEPLOYMENT_CHECKLIST.md | pass | found |
| file:docs/CI_ARTIFACTS.md | pass | found |
| file:docs/SCHEMAS.md | pass | found |
| file:reports/evaluation_report.md | pass | found |
| file:reports/repo_health.md | pass | found |
| file:reports/schemas/OrganizationProfile.schema.json | pass | found |
| file:reports/schemas/ProposalPackage.schema.json | pass | found |
| git_remote | pass | origin	https://github.com/pshuklabaidya/agentic-grant-proposal-builder.git (fetch)<br>origin	https://github.com/pshuklabaidya/agentic-grant-proposal-builder.git (push) |
| current_branch | pass | main |
| working_tree | warn | M .github/workflows/ci.yml;  M Makefile;  M README.md;  M docs/DOCS_INDEX.md;  M reports/evaluation_report.md;  M reports/evaluation_results.json;  M reports/repo_health.json;  M reports/repo_health.md;  M scripts/repo_health.py; ?? docs/CI_ARTIFACTS.md; ?? docs/PUBLICATION_READINESS.md; ?? docs/SCHEMAS.md; ?? reports/schemas/; ?? scripts/export_schemas.py; ?? scripts/publication_readiness.py; ?? tests/test_ci_artifacts.py; ?? tests/test_publication_readiness.py; ?? tests/test_schema_exports.py |
| gh_repo_view | warn | To get started with GitHub CLI, please run:  gh auth login<br>Alternatively, populate the GH_TOKEN environment variable with a GitHub API authentication token. |

## Interpretation

Failed file checks should be fixed before portfolio sharing. GitHub CLI warnings may be acceptable when local credentials do not have repository administration permission.
