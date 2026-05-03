from pathlib import Path


def test_dockerfile_exists_and_runs_streamlit():
    path = Path("Dockerfile")

    assert path.exists()
    text = path.read_text()
    assert "FROM python:3.12-slim" in text
    assert "EXPOSE 8501" in text
    assert "streamlit" in text
    assert "_stcore/health" in text


def test_dockerignore_excludes_secrets_and_local_artifacts():
    path = Path(".dockerignore")

    assert path.exists()
    text = path.read_text()
    assert ".env" in text
    assert ".streamlit/secrets.toml" in text
    assert ".venv" in text
    assert "reports" in text


def test_docker_doc_exists():
    path = Path("docs/DOCKER.md")

    assert path.exists()
    text = path.read_text()
    assert "docker build" in text
    assert "docker run" in text
    assert "OPENAI_API_KEY" in text


def test_docker_smoke_script_exists():
    path = Path("scripts/docker_smoke.py")

    assert path.exists()
    text = path.read_text()
    assert "docker" in text
    assert "agentic-grant-proposal-builder:local" in text


def test_makefile_includes_docker_targets():
    text = Path("Makefile").read_text()

    assert "docker-build:" in text
    assert "docker-run:" in text
    assert "docker-smoke:" in text


def test_readme_and_docs_index_link_docker_doc():
    readme = Path("README.md").read_text()
    docs_index = Path("docs/DOCS_INDEX.md").read_text()

    assert "docs/DOCKER.md" in readme
    assert "DOCKER.md" in docs_index
