# Command Line Interface

## Purpose

The command line interface makes Agentic Grant Proposal Builder usable outside the Streamlit dashboard. It supports scripted proposal generation, scenario evaluation, and artifact export.

## Installed Command

After installation:

    pip install -e ".[dev]"

Run:

    agpb --help

## Commands

### List Demo Scenarios

    agpb list-scenarios

### Build Proposal From Scenario

    agpb build-scenario education_access

Generated files:

    reports/cli/education_access_proposal.md
    reports/cli/education_access_proposal_package.json
    reports/cli/education_access_summary.json

### Evaluate One Scenario

    agpb evaluate-scenario education_access

### Build From Local Files

Create a profile JSON file with fields accepted by `OrganizationProfile`.

Example:

    {
      "organization_name": "Example Community Organization",
      "mission": "Expand equitable access to education and workforce readiness.",
      "target_population": "Underserved learners and families.",
      "geography": "Regional service area",
      "current_programs": "Tutoring, coaching, and family navigation.",
      "requested_amount": "$250,000",
      "project_duration": "12 months"
    }

Run:

    agpb build-files --profile profile.json --documents guidance.txt notes.txt --stem custom_project

Generated files:

    reports/cli/custom_project_proposal.md
    reports/cli/custom_project_proposal_package.json
    reports/cli/custom_project_summary.json

## Runtime Modes

The CLI uses the same pipeline as the Streamlit app.

Without `OPENAI_API_KEY`, deterministic fallback runs.

With `OPENAI_API_KEY` and `AGPB_USE_OPENAI_AGENTS=1`, the OpenAI-powered tool-calling agent path can run.
