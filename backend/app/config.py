from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    openai_api_key: str | None
    llm_model: str = "gpt-5.4-mini"
    embedding_model: str = "text-embedding-3-small"
    allowed_origins: tuple[str, ...] = (
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    )

    @property
    def has_openai_api_key(self) -> bool:
        return bool(self.openai_api_key and self.openai_api_key.strip())


def get_settings() -> Settings:
    load_environment_files()
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        llm_model=os.getenv("LLM_MODEL", "gpt-5.4-mini"),
        embedding_model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"),
        allowed_origins=parse_allowed_origins(os.getenv("ALLOWED_ORIGINS")),
    )


def parse_allowed_origins(value: str | None) -> tuple[str, ...]:
    defaults = ("http://localhost:5173", "http://127.0.0.1:5173")
    if not value:
        return defaults

    origins = tuple(origin.strip().rstrip("/") for origin in value.split(",") if origin.strip())
    return origins or defaults


def default_env_file_paths() -> list[Path]:
    repo_root = Path(__file__).resolve().parents[2]
    return [repo_root / ".env", repo_root / "backend" / ".env"]


def load_environment_files(paths: list[Path] | None = None) -> None:
    for path in paths or default_env_file_paths():
        if path.exists():
            load_dotenv(path, override=False)
