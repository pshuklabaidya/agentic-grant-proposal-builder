from agentic_grant_proposal_builder.config import load_runtime_config, runtime_summary


def test_load_runtime_config_without_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("AGPB_MODEL", raising=False)
    monkeypatch.delenv("AGPB_USE_OPENAI_AGENTS", raising=False)
    monkeypatch.delenv("OPENAI_AGENTS_DISABLE_TRACING", raising=False)

    config = load_runtime_config()

    assert config.openai_api_key_detected is False
    assert config.model == "gpt-4.1-mini"
    assert config.use_openai_agents is True
    assert config.tracing_disabled is False


def test_runtime_summary_contains_runtime_path(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    summary = runtime_summary()

    assert "Runtime path" in summary
