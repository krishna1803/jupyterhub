from pydantic import BaseSettings, AnyHttpUrl, Field
from typing import Optional


class Settings(BaseSettings):
    jupyterhub_url: AnyHttpUrl = Field(..., description="Base URL of JupyterHub, e.g. https://hub.example.com")
    api_token: str = Field(..., description="Admin API token for JupyterHub")
    verify_ssl: bool = True
    request_timeout: int = 30

    # FastAPI server config
    api_host: str = "0.0.0.0"
    api_port: int = 8080

    # Streamlit
    streamlit_port: int = 8501

    class Config:
        env_prefix = "JUPYTERHUB_MANAGER_"
        case_sensitive = False


settings = Settings()  # type: ignore[arg-type]
