# Scenario Guide

The evaluation harness uses synthetic grant scenarios stored under:

    sample_data/scenarios

Each scenario includes:

- Scenario identifier
- Scenario title
- Applicant organization profile
- Synthetic funder guidance documents

## Scenario: Education Access And Workforce Readiness

File:

    sample_data/scenarios/education_access.json

Purpose:

This scenario tests education access, workforce readiness, family support, measurable outcomes, budget narrative, evaluation plan, and sustainability.

Expected strengths:

- Strong mission fit
- Strong eligibility signal
- Clear required proposal sections
- Budget and evaluation terms present

## Scenario: Rural Health Navigation

File:

    sample_data/scenarios/rural_health.json

Purpose:

This scenario tests rural service delivery, preventive care access, care navigation, transportation barriers, referral coordination, evaluation, and sustainability.

Expected strengths:

- Clear target population
- Health navigation focus
- Strong implementation language
- Evaluation and reporting terms present

## Scenario: Small Business Technical Assistance

File:

    sample_data/scenarios/small_business_support.json

Purpose:

This scenario tests entrepreneurship support, technical assistance, capital readiness, business stabilization, underserved entrepreneurs, measurable outcomes, and partnership strategy.

Expected strengths:

- Clear economic development use case
- Strong target-population fit
- Budget justification terms present
- Measurable outcomes expected

## Running Scenarios

Run all scenarios:

    python -m agentic_grant_proposal_builder.evaluation

Run through Makefile:

    make eval

Generated outputs:

    reports/evaluation_results.json
    reports/evaluation_report.md

## Scenario Design Principle

The scenarios are synthetic and safe for public portfolio demonstration. They are designed to test the same pipeline used by the dashboard without requiring private grant documents.
