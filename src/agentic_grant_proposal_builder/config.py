from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class RuntimeConfig:
    openai_api_key_detected: bool
    model: str
    use_openai_agents: bool
    tracing_disabled: bool
    key_source: str


def _load_streamlit_secret(name: str) -> str | None:
    try:
        import streamlit as st
    except Exception:
        return None

    try:
        value = st.secrets.get(name)
    except Exception:
        return None

    if value is None:
        return None

    return str(value)


def _set_env_from_streamlit_secret(name: str) -> bool:
    if os.getenv(name):
        return False

    value = _load_streamlit_secret(name)
    if not value:
        return False

    os.environ[name] = value
    return True


def load_runtime_config() -> RuntimeConfig:
    load_dotenv()

    key_loaded_from_secrets = _set_env_from_streamlit_secret("OPENAI_API_KEY")
    _set_env_from_streamlit_secret("AGPB_MODEL")
    _set_env_from_streamlit_secret("AGPB_USE_OPENAI_AGENTS")
    _set_env_from_streamlit_secret("OPENAI_AGENTS_DISABLE_TRACING")
    _set_env_from_streamlit_secret("AGPB_DRAFT_DETAIL")
    _set_env_from_streamlit_secret("AGPB_EVIDENCE_TOP_K")

    api_key_detected = bool(os.getenv("OPENAI_API_KEY"))
    model = os.getenv("AGPB_MODEL", "gpt-4.1-mini")
    use_openai_agents = os.getenv("AGPB_USE_OPENAI_AGENTS", "1") == "1"
    tracing_disabled = os.getenv("OPENAI_AGENTS_DISABLE_TRACING", "0") == "1"

    if key_loaded_from_secrets:
        key_source = "Streamlit secrets"
    elif api_key_detected:
        key_source = "environment or .env"
    else:
        key_source = "not configured"

    return RuntimeConfig(
        openai_api_key_detected=api_key_detected,
        model=model,
        use_openai_agents=use_openai_agents,
        tracing_disabled=tracing_disabled,
        key_source=key_source,
    )


def runtime_summary() -> dict[str, str]:
    config = load_runtime_config()

    runtime_path = "deterministic fallback"
    if config.openai_api_key_detected and config.use_openai_agents:
        runtime_path = "OpenAI Agents SDK"

    return {
        "API key detected": "Yes" if config.openai_api_key_detected else "No",
        "Key source": config.key_source,
        "Model": config.model,
        "Agent SDK mode": "On" if config.use_openai_agents else "Off",
        "Tracing disabled": "Yes" if config.tracing_disabled else "No",
        "Runtime path": runtime_path,
    }
