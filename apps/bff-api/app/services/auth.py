from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    username: str
    name: str
    password: str
    tenants: list[str]
    default_tenant: str


@dataclass(frozen=True)
class Tenant:
    id: str
    name: str


TENANTS: dict[str, Tenant] = {
    "perusahaan_a": Tenant(id="perusahaan_a", name="Lembaga ZISWAF A"),
    "perusahaan_b": Tenant(id="perusahaan_b", name="Lembaga ZISWAF B"),
}

USERS: dict[str, User] = {
    "admin": User(
        username="admin",
        name="Administrator",
        password="admin123",
        tenants=["perusahaan_a", "perusahaan_b"],
        default_tenant="perusahaan_a",
    ),
    "finance.a": User(
        username="finance.a",
        name="Finance Perusahaan A",
        password="finance123",
        tenants=["perusahaan_a"],
        default_tenant="perusahaan_a",
    ),
    "finance.b": User(
        username="finance.b",
        name="Finance Perusahaan B",
        password="finance123",
        tenants=["perusahaan_b"],
        default_tenant="perusahaan_b",
    ),
}


def authenticate(username: str, password: str) -> User | None:
    user = USERS.get(username)
    if user is None or user.password != password:
        return None
    return user


def get_user(username: str) -> User | None:
    return USERS.get(username)


def tenant_public(t: Tenant) -> dict:
    return {"id": t.id, "name": t.name}


def user_public(user: User) -> dict:
    return {
        "username": user.username,
        "name": user.name,
        "tenants": [tenant_public(TENANTS[t]) for t in user.tenants],
        "default_tenant": user.default_tenant,
    }
