from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    # DB DSNs are read directly via os.getenv in db.py (DATABASE_URL, DWH_DATABASE_URL);
    # mirrored here for visibility/overrides.
    database_url: str = ""
    dwh_database_url: str = ""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
