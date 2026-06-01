from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"

    # Downstream
    api_python_base_url: str = "http://localhost:8000"
    # Reporting service (dashboard + report read/aggregation) — service terpisah
    report_api_base_url: str = "http://localhost:8010"

    # Identity (live lookup ke api-python)
    identity_timeout: float = 3.0

    # Session & CORS
    session_secret: str = "dev-secret-change-me"
    cors_origin: str = "http://localhost:5173"

    # Auth
    auth_providers: str = "password,google"
    isf_auth_database_url: str = ""

    # Google OAuth (empty = provider disabled)
    google_oauth_client_id: str = ""
    google_oauth_client_secret: str = ""
    google_oauth_redirect_url: str = "http://localhost:7000/api/auth/google/callback"
    google_allowed_domains: str = "ihsansolusi.co.id"
    google_allowed_emails: str = ""

    # Frontend
    frontend_base_url: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def enabled_providers(self) -> set[str]:
        return {p.strip() for p in self.auth_providers.split(",") if p.strip()}

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.cors_origin.split(",") if o.strip()]


settings = Settings()
