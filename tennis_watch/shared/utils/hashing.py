import hashlib
from pathlib import Path


def calc_hash(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def read_hash(path: Path) -> str | None:
    if not path.exists():
        return None
    try:
        return path.read_text(encoding="utf-8").strip()
    except Exception:
        return None


def write_hash(path: Path, value: str) -> None:
    try:
        path.write_text(value, encoding="utf-8")
    except Exception as e:
        print("ハッシュファイル書き込みエラー:", e)


def is_same_as_last(message: str, hash_file: Path) -> bool:
    new_hash = calc_hash(message)
    old_hash = read_hash(hash_file)
    return (old_hash == new_hash)


def update_last(message: str, hash_file: Path) -> None:
    new_hash = calc_hash(message)
    write_hash(hash_file, new_hash)