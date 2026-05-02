from pathlib import Path


def test_docs_index_exists_and_links_core_docs():
    path = Path("docs/DOCS_INDEX.md")

    assert path.exists()
    text = path.read_text()
    assert "ARCHITECTURE.md" in text
    assert "DEMO_WALKTHROUGH.md" in text
    assert "INTERVIEW_TALK_TRACK.md" in text
    assert "SCENARIOS.md" in text


def test_scenario_guide_exists_and_names_scenarios():
    path = Path("docs/SCENARIOS.md")

    assert path.exists()
    text = path.read_text()
    assert "education_access.json" in text
    assert "rural_health.json" in text
    assert "small_business_support.json" in text


def test_readme_links_docs_index_and_scenarios():
    text = Path("README.md").read_text()

    assert "docs/DOCS_INDEX.md" in text
    assert "docs/SCENARIOS.md" in text


def test_streamlit_benchmark_cache_has_ttl():
    text = Path("src/agentic_grant_proposal_builder/app.py").read_text()

    assert "@st.cache_data(show_spinner=False, ttl=300)" in text
