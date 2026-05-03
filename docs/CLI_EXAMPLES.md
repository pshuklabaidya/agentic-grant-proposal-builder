# CLI Examples

## Purpose

The CLI examples show how to use Agentic Grant Proposal Builder without opening the Streamlit dashboard.

## Sample Files

Sample profile:

    sample_data/cli_example/profile.json

Sample source documents:

    sample_data/cli_example/funder_guidance.txt
    sample_data/cli_example/program_notes.txt

## List Built-In Scenarios

    agpb list-scenarios

## Evaluate A Scenario

    agpb evaluate-scenario education_access

## Build Artifacts From A Scenario

    agpb build-scenario education_access --output-dir reports/cli

Generated files:

    reports/cli/education_access_proposal.md
    reports/cli/education_access_proposal_package.json
    reports/cli/education_access_summary.json

## Build Artifacts From Local Files

    agpb build-files \
      --profile sample_data/cli_example/profile.json \
      --documents sample_data/cli_example/funder_guidance.txt sample_data/cli_example/program_notes.txt \
      --output-dir reports/cli \
      --stem riverbend

Generated files:

    reports/cli/riverbend_proposal.md
    reports/cli/riverbend_proposal_package.json
    reports/cli/riverbend_summary.json

## CLI Smoke Test

Run:

    python scripts/cli_smoke.py

Or through Makefile:

    make cli-smoke

The smoke test verifies CLI help, scenario listing, scenario evaluation, scenario artifact generation, and local file artifact generation.
