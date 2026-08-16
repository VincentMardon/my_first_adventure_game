import json
from pathlib import Path
from tempfile import NamedTemporaryFile


def load_json(path: Path) -> object:
    """Decode and return JSON data from a UTF-8 file.

    Filesystem, decoding, and JSON errors are propagated to the caller.
    """
    return json.loads(path.read_text(encoding="utf-8"))


def save_json_atomic(path: Path, data: object) -> None:
    """Serialize data as JSON and atomically replace the target file.

    The temporary file is created beside the destination so replacement remains
    on the same filesystem. Serialization and filesystem errors are propagated
    to the caller.
    """
    temporary_path: Path | None = None

    try:
        path.parent.mkdir(parents=True, exist_ok=True)

        with NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            json.dump(
                data,
                temporary_file,
                ensure_ascii=False,
                indent=2,
            )
            temporary_file.write("\n")

        temporary_path.replace(path)

    finally:
        if temporary_path is not None:
            try:
                temporary_path.unlink(missing_ok=True)
            except OSError:
                pass
