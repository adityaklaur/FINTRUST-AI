import importlib.util

import pytest

from app.core.auth import ANON, get_current_user_id, verify_token


def test_anon_when_no_authorization_header():
    assert get_current_user_id(None) == ANON


def test_anon_when_secret_unset_even_with_token():
    # Default test settings have no SUPABASE_JWT_SECRET, so auth is disabled.
    assert get_current_user_id("Bearer some.jwt.token") == ANON


def test_anon_when_header_not_bearer():
    assert get_current_user_id("Basic abc") == ANON


@pytest.mark.skipif(importlib.util.find_spec("jwt") is None, reason="PyJWT not installed")
def test_verify_token_roundtrip():
    import jwt

    token = jwt.encode({"sub": "user-123"}, "s3cret", algorithm="HS256")
    assert verify_token(token, "s3cret") == "user-123"
    assert verify_token(token, "wrong-secret") is None
    assert verify_token("not-a-jwt", "s3cret") is None
