"""Provider-agnostic LLM layer with automatic failover.

- ``LLMClient`` wraps ONE provider (groq / gemini / openai / anthropic). It is
  "available" only if the provider is set, a key is present, and the SDK imports.
- ``LLMRouter`` composes a primary + optional fallback client and tries them in
  order; if all fail/return empty, it returns "" and the caller (AnswerGenerator)
  degrades to the offline extractive answer. The app therefore NEVER hard-fails
  on the LLM layer.

Default model IDs are sensible starting points; providers rename/deprecate models
often — override with LLM_MODEL / LLM_FALLBACK_MODEL and check the provider docs.
"""

from __future__ import annotations

from functools import lru_cache

from app.core.config import Settings, get_settings
from app.core.logging import get_logger

log = get_logger("llm")

_DEFAULT_MODELS = {
    "gemini": "gemini-2.5-flash",
    "groq": "llama-3.3-70b-versatile",
    "openai": "gpt-4o-mini",
    "anthropic": "claude-haiku-4-5-20251001",
}


class LLMClient:
    """A single-provider client. Construct from config, or override explicitly."""

    def __init__(
        self,
        config: Settings | None = None,
        provider: str | None = None,
        api_key: str | None = None,
        model: str | None = None,
    ):
        self.config = config or get_settings()
        self.provider = (provider if provider is not None else (self.config.llm_provider or "none")).lower()
        self.api_key = api_key if api_key is not None else self.config.llm_api_key
        self.model_name = model or _DEFAULT_MODELS.get(self.provider, "")
        self._available = False

        if self.provider == "none":
            return
        if not self.api_key:
            log.warning("LLM provider=%s but API key is empty; skipping this provider.", self.provider)
            return
        try:
            self._verify_import()
            self._available = True
            log.info("LLM ready: provider=%s model=%s", self.provider, self.model_name)
        except Exception as exc:  # noqa: BLE001
            log.warning("LLM provider '%s' unavailable (%s).", self.provider, exc)

    @property
    def available(self) -> bool:
        return self._available

    def _verify_import(self) -> None:
        if self.provider == "groq":
            import groq  # noqa: F401
        elif self.provider == "openai":
            import openai  # noqa: F401
        elif self.provider == "gemini":
            import google.generativeai  # noqa: F401
        elif self.provider == "anthropic":
            import anthropic  # noqa: F401
        else:
            raise ValueError(f"unknown LLM provider: {self.provider}")

    def complete(self, system: str, user: str) -> str:
        if not self._available:
            return ""
        try:
            if self.provider == "groq":
                return self._groq(system, user)
            if self.provider == "openai":
                return self._openai(system, user)
            if self.provider == "gemini":
                return self._gemini(system, user)
            if self.provider == "anthropic":
                return self._anthropic(system, user)
        except Exception as exc:  # noqa: BLE001
            log.warning("LLM call failed (provider=%s): %s", self.provider, exc)
        return ""

    # --- provider implementations (SDKs imported lazily) ---
    def _openai_style(self, sdk_client, system: str, user: str) -> str:
        resp = sdk_client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=self.config.llm_temperature,
            max_tokens=self.config.llm_max_tokens,
        )
        return resp.choices[0].message.content or ""

    def _groq(self, system: str, user: str) -> str:
        from groq import Groq

        return self._openai_style(Groq(api_key=self.api_key), system, user)

    def _openai(self, system: str, user: str) -> str:
        from openai import OpenAI

        return self._openai_style(OpenAI(api_key=self.api_key), system, user)

    def _gemini(self, system: str, user: str) -> str:
        import google.generativeai as genai

        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel(self.model_name, system_instruction=system)
        resp = model.generate_content(
            user,
            generation_config={
                "temperature": self.config.llm_temperature,
                "max_output_tokens": self.config.llm_max_tokens,
            },
        )
        return resp.text or ""

    def _anthropic(self, system: str, user: str) -> str:
        import anthropic

        client = anthropic.Anthropic(api_key=self.api_key)
        msg = client.messages.create(
            model=self.model_name,
            system=system,
            max_tokens=self.config.llm_max_tokens,
            temperature=self.config.llm_temperature,
            messages=[{"role": "user", "content": user}],
        )
        return "".join(b.text for b in msg.content if getattr(b, "type", None) == "text")


class LLMRouter:
    """Primary → fallback → (caller does extractive). Exposes the LLMClient interface."""

    def __init__(self, config: Settings | None = None, clients: list | None = None):
        self.config = config or get_settings()
        self._clients = clients if clients is not None else self._build_clients()
        self._last_model = ""

    def _build_clients(self) -> list:
        specs = [
            (self.config.llm_provider, self.config.llm_api_key, self.config.llm_model),
            (self.config.llm_fallback_provider, self.config.llm_fallback_api_key, self.config.llm_fallback_model),
        ]
        clients: list[LLMClient] = []
        for provider, key, model in specs:
            if not provider or provider.lower() == "none":
                continue
            client = LLMClient(config=self.config, provider=provider, api_key=key, model=(model or None))
            if client.available:
                clients.append(client)
        return clients

    @property
    def available(self) -> bool:
        return len(self._clients) > 0

    @property
    def model_name(self) -> str:
        if self._last_model:
            return self._last_model
        return self._clients[0].model_name if self._clients else "extractive-none"

    def complete(self, system: str, user: str) -> str:
        for client in self._clients:
            text = client.complete(system, user)
            if text and text.strip():
                self._last_model = client.model_name
                return text
        return ""


@lru_cache
def get_llm() -> LLMRouter:
    return LLMRouter()
