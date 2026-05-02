from agentic_grant_proposal_builder.openai_workflow import openai_agents_enabled


def test_openai_agents_disabled_without_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("AGPB_USE_OPENAI_AGENTS", "1")

    assert openai_agents_enabled() is False


def test_openai_agents_disabled_by_flag(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("AGPB_USE_OPENAI_AGENTS", "0")

    assert openai_agents_enabled() is False


def test_openai_agents_enabled_with_key_and_flag(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("AGPB_USE_OPENAI_AGENTS", "1")

    assert openai_agents_enabled() is True
