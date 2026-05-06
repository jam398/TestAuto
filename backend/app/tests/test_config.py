from pathlib import Path

import os

from app.config import load_environment_files


def test_load_environment_files_reads_backend_env(monkeypatch, tmp_path: Path):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "OPENAI_API_KEY=from-env-file\nLLM_MODEL=env-file-model\nEMBEDDING_MODEL=env-file-embedding\n",
        encoding="utf-8",
    )
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("LLM_MODEL", raising=False)
    monkeypatch.delenv("EMBEDDING_MODEL", raising=False)

    load_environment_files([env_file])

    assert os.getenv("OPENAI_API_KEY") == "from-env-file"
    assert os.getenv("LLM_MODEL") == "env-file-model"
    assert os.getenv("EMBEDDING_MODEL") == "env-file-embedding"
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("LLM_MODEL", raising=False)
    monkeypatch.delenv("EMBEDDING_MODEL", raising=False)


def test_load_environment_files_does_not_override_process_env(monkeypatch, tmp_path: Path):
    env_file = tmp_path / ".env"
    env_file.write_text("OPENAI_API_KEY=from-env-file\n", encoding="utf-8")
    monkeypatch.setenv("OPENAI_API_KEY", "from-process-env")

    load_environment_files([env_file])

    assert os.getenv("OPENAI_API_KEY") == "from-process-env"
