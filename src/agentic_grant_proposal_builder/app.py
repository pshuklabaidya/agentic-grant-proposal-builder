from __future__ import annotations

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from agentic_grant_proposal_builder.config import load_runtime_config, runtime_summary
from agentic_grant_proposal_builder.document_loader import load_uploaded_file
from agentic_grant_proposal_builder.evaluation import run_all_scenarios
from agentic_grant_proposal_builder.export import package_to_json, proposal_to_markdown
from agentic_grant_proposal_builder.models import GrantDocument, OrganizationProfile
from agentic_grant_proposal_builder.pipeline import build_proposal

load_dotenv()
load_runtime_config()

st.set_page_config(page_title="Agentic Grant Proposal Builder", page_icon="AG", layout="wide")


@st.cache_data(show_spinner=False)
def cached_demo_evaluation() -> list[dict[str, object]]:
    return [result.model_dump() for result in run_all_scenarios()]


st.title("Agentic Grant Proposal Builder")
st.caption("Agentic RAG workflow for grant requirements, proposal drafting, review, and evaluation.")

with st.sidebar:
    st.header("OpenAI Runtime")
    for label, value in runtime_summary().items():
        st.write(f"{label}: {value}")

    st.divider()
    st.header("Applicant Profile")
    organization_name = st.text_input("Organization name", "Example Community Impact Organization")
    mission = st.text_area(
        "Mission",
        "Expand equitable access to education, workforce readiness, and community support.",
    )
    target_population = st.text_input(
        "Target population",
        "Low-income students, adult learners, and underserved families.",
    )
    geography = st.text_input("Geography", "Regional service area")
    current_programs = st.text_area(
        "Current programs",
        "Tutoring, career coaching, digital literacy, and case management.",
    )
    requested_amount = st.text_input("Requested amount", "$250,000")
    project_duration = st.text_input("Project duration", "12 months")

profile = OrganizationProfile(
    organization_name=organization_name,
    mission=mission,
    target_population=target_population,
    geography=geography,
    current_programs=current_programs,
    requested_amount=requested_amount,
    project_duration=project_duration,
)

uploaded_files = st.file_uploader(
    "Upload funder guidelines, RFPs, prior proposals, program notes, or source documents",
    type=["pdf", "txt", "md"],
    accept_multiple_files=True,
)

documents: list[GrantDocument] = []

if uploaded_files:
    for uploaded_file in uploaded_files:
        documents.append(load_uploaded_file(uploaded_file.name, uploaded_file.getvalue()))
else:
    documents.append(
        GrantDocument(
            name="sample_funder_guidance.txt",
            text=(
                "Eligible applicants include nonprofit organizations serving underserved communities. "
                "Priority will be given to education access, workforce readiness, measurable outcomes, "
                "budget narrative, evaluation plan, sustainability, and allowable costs."
            ),
            source_type="sample",
        )
    )

if st.button("Build Proposal", type="primary"):
    proposal, fit_score, evidence, package = build_proposal(profile, documents)

    st.success("Proposal package created.")

    metric_cols = st.columns(6)
    metric_cols[0].metric("Overall", fit_score.overall)
    metric_cols[1].metric("Mission", fit_score.mission_fit)
    metric_cols[2].metric("Eligibility", fit_score.eligibility_fit)
    metric_cols[3].metric("Evidence", fit_score.evidence_fit)
    metric_cols[4].metric("Budget", fit_score.budget_fit)
    metric_cols[5].metric("Implementation", fit_score.implementation_fit)

    tabs = st.tabs(
        [
            "Proposal Draft",
            "Funder Requirements",
            "Agent Trace",
            "Compliance",
            "Budget",
            "Reviewer Findings",
            "Quality Gate",
            "Evidence",
            "Benchmark",
            "Exports",
        ]
    )

    markdown_output = proposal_to_markdown(proposal, fit_score, package)
    json_output = package_to_json(proposal, fit_score, package)

    with tabs[0]:
        st.markdown(markdown_output)

    with tabs[1]:
        st.dataframe(
            pd.DataFrame([item.model_dump() for item in package.funder_requirements]),
            use_container_width=True,
        )

    with tabs[2]:
        st.dataframe(
            pd.DataFrame([step.model_dump() for step in package.workflow_trace]),
            use_container_width=True,
        )

    with tabs[3]:
        st.dataframe(
            pd.DataFrame([check.model_dump() for check in package.compliance_checks]),
            use_container_width=True,
        )

    with tabs[4]:
        st.dataframe(
            pd.DataFrame([item.model_dump() for item in package.budget_plan.line_items]),
            use_container_width=True,
        )
        st.markdown(package.budget_plan.narrative)

    with tabs[5]:
        st.dataframe(
            pd.DataFrame([finding.model_dump() for finding in package.reviewer_findings]),
            use_container_width=True,
        )

    with tabs[6]:
        if package.quality_report is not None:
            st.metric("Readiness Score", package.quality_report.readiness_score)
            st.write("Overall status: " + package.quality_report.overall_status)
            st.write(package.quality_report.final_recommendation)
            st.dataframe(
                pd.DataFrame([check.model_dump() for check in package.quality_report.checks]),
                use_container_width=True,
            )

    with tabs[7]:
        for chunk in evidence:
            with st.expander(f"{chunk.source} - relevance {chunk.score:.3f}"):
                st.write(chunk.text)

    with tabs[8]:
        st.dataframe(pd.DataFrame(cached_demo_evaluation()), use_container_width=True)

    with tabs[9]:
        st.download_button(
            "Download Proposal Markdown",
            data=markdown_output,
            file_name="grant_proposal_draft.md",
            mime="text/markdown",
        )
        st.download_button(
            "Download Proposal Package JSON",
            data=json_output,
            file_name="grant_proposal_package.json",
            mime="application/json",
        )
