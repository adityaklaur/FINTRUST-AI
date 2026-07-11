from app.generation.llm_client import LLMRouter


class _Client:
    def __init__(self, name: str, out: str):
        self.model_name = name
        self.available = True
        self._out = out

    def complete(self, system: str, user: str) -> str:
        return self._out


def test_router_falls_through_to_next_provider():
    router = LLMRouter(clients=[_Client("primary", ""), _Client("fallback", "answer")])
    assert router.available is True
    assert router.complete("s", "u") == "answer"
    assert router.model_name == "fallback"  # records which one actually answered


def test_router_returns_empty_when_no_clients():
    router = LLMRouter(clients=[])
    assert router.available is False
    assert router.complete("s", "u") == ""
    assert router.model_name == "extractive-none"


def test_router_uses_primary_when_it_answers():
    router = LLMRouter(clients=[_Client("primary", "hi"), _Client("fallback", "nope")])
    assert router.complete("s", "u") == "hi"
    assert router.model_name == "primary"
