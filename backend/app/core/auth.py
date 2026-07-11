"""Optional authentication.

With no ``SUPABASE_JWT_SECRET`` configured (the default), every request resolves
to the ANON user and the app behaves as a public demo. Configure the secret and
send a Supabase JWT (``Authorization: Bearer <token>``) to get real per-user
identity — audit history is then scoped to that user.

Note: this uses Supabase's legacy HS256 shared secret (Project Settings → API →
JWT secret). Newer projects can use asymmetric keys + JWKS; that's a drop-in
upgrade to ``verify_token`` when needed.
"""

from __future__ import annotations

from fastapi import Header

from app.core.config import get_settings
from app.core.logging import get_logger

log = get_logger("auth")

ANON = "anonymous"


def verify_token(token: str, secret: str) -> str | None:
    """Return the Supabase user id (JWT 'sub') if the token verifies, else None."""
    try:
        import jwt

        payload = jwt.decode(token, secret, algorithms=["HS256"], options={"verify_aud": False})
        return payload.get("sub")
    except Exception as exc:  # noqa: BLE001 - any failure => unauthenticated
        log.warning("JWT verification failed: %s", exc)
        return None


def get_current_user_id(authorization: str | None = Header(default=None)) -> str:
    """FastAPI dependency: resolve the caller's user id, or ANON if not authed."""
    cfg = get_settings()
    if not cfg.supabase_jwt_secret or not authorization:
        return ANON
    if not authorization.lower().startswith("bearer "):
        return ANON
    return verify_token(authorization.split(" ", 1)[1].strip(), cfg.supabase_jwt_secret) or ANON
