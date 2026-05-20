from __future__ import annotations

import bcrypt

from app.services.auth_db import AuthDB
from app.services.auth_providers.base import AuthResult


class PasswordProvider:
    name = "password"

    def __init__(self, db: AuthDB):
        self.db = db

    @property
    def is_available(self) -> bool:
        return True

    async def authenticate(self, username: str, password: str) -> AuthResult | None:
        user = await self.db.get_user_by_username(username)
        if not user:
            return None
        password_hash = await self.db.get_password_hash(user["id"])
        if not password_hash:
            return None
        try:
            if not bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8")):
                return None
        except ValueError:
            return None
        return AuthResult(user_id=user["id"], provider=self.name)
