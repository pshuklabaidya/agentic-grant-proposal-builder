from pathlib import Path


def test_streamlit_smoke_script_exists():
    path = Path("scripts/smoke_streamlit.py")

    assert path.exists()
    text = path.read_text()
    assert "python" not in path.name
    assert "streamlit" in text
    assert "server.headless=true" in text


def test_makefile_includes_smoke_target():
    text = Path("Makefile").read_text()

    assert "smoke:" in text
    assert "python scripts/smoke_streamlit.py" in text


def test_ci_includes_streamlit_smoke_test():
    text = Path(".github/workflows/ci.yml").read_text()

    assert "Run Streamlit smoke test" in text
    assert "python scripts/smoke_streamlit.py" in text
