from pathlib import Path


def test_streamlit_app_entrypoint_exists():
    assert Path("src/agentic_grant_proposal_builder/app.py").exists()


def test_streamlit_config_exists():
    assert Path(".streamlit/config.toml").exists()


def test_streamlit_secrets_example_exists():
    path = Path(".streamlit/secrets.toml.example")

    assert path.exists()
    text = path.read_text()
    assert "OPENAI_API_KEY" in text
    assert "AGPB_USE_OPENAI_AGENTS" in text


def test_streamlit_deployment_checklist_exists():
    path = Path("docs/STREAMLIT_DEPLOYMENT_CHECKLIST.md")

    assert path.exists()
    text = path.read_text()
    assert "src/agentic_grant_proposal_builder/app.py" in text
    assert "Streamlit" in text
