from dataclasses import dataclass


@dataclass(frozen=True)
class AuthResult:
    user_id: str
    provider: str
    external_id: str | None = None
