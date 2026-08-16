import json
from pathlib import Path

import pytest

from my_first_adventure_game.engine.persistence import (
    load_json,
    save_json_atomic,
)


def test_save_json_atomic_creates_parent_directories(tmp_path: Path) -> None:
    path = tmp_path / "profiles" / "player.json"

    save_json_atomic(path, {"score": 700})

    assert json.loads(path.read_text(encoding="utf-8")) == {"score": 700}


def test_save_json_atomic_replaces_existing_file(tmp_path: Path) -> None:
    path = tmp_path / "profile.json"
    path.write_text('{"score": 100}', encoding="utf-8")

    save_json_atomic(path, {"score": 900})

    assert json.loads(path.read_text(encoding="utf-8")) == {"score": 900}


def test_save_json_atomic_preserves_original_when_replacement_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    path = tmp_path / "profile.json"
    path.write_text('{"score": 100}', encoding="utf-8")
    temporary_paths: list[Path] = []

    def fail_replacement(
        temporary_path: Path,
        destination_path: Path,
    ) -> Path:
        temporary_paths.append(temporary_path)
        raise OSError("replacement failed")

    monkeypatch.setattr(Path, "replace", fail_replacement)

    with pytest.raises(OSError, match="replacement failed"):
        save_json_atomic(path, {"score": 900})

    assert json.loads(path.read_text(encoding="utf-8")) == {"score": 100}
    assert len(temporary_paths) == 1
    assert not temporary_paths[0].exists()


def test_load_json_returns_decoded_data(tmp_path: Path) -> None:
    path = tmp_path / "profile.json"
    path.write_text(
        '{"name": "Éloïse", "best_score": 1200}',
        encoding="utf-8",
    )

    data = load_json(path)

    assert data == {
        "name": "Éloïse",
        "best_score": 1200,
    }


def test_load_json_propagates_invalid_json(tmp_path: Path) -> None:
    path = tmp_path / "profile.json"
    path.write_text("{invalid json", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        load_json(path)


def test_load_json_propagates_missing_file(tmp_path: Path) -> None:
    path = tmp_path / "missing.json"

    with pytest.raises(FileNotFoundError):
        load_json(path)
