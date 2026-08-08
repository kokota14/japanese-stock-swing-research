from __future__ import annotations

import json
from pathlib import Path


APP_DIR = Path(__file__).resolve().parent
SNAPSHOT_PATH = APP_DIR / "data" / "public_snapshot.json"

FORBIDDEN_SUFFIXES = {
    ".db",
    ".pkl",
    ".sqlite",
    ".sqlite3",
}
FORBIDDEN_NAMES = {
    ".env",
    "secrets.toml",
}
FORBIDDEN_TEXT = {
    "c:\\users\\",
    "onedrive\\デスクトップ",
    "api_key=",
    "api-key=",
    "secret_key=",
}
EXPECTED_KEYS = {
    "updated_at",
    "data_date",
    "data_source",
    "model_version",
    "market",
    "paper_portfolio",
    "learning",
    "candidates",
    "assumptions",
}


def _tracked_files() -> list[Path]:
    return [
        path
        for path in APP_DIR.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and "__pycache__" not in path.parts
        and path.name not in {
            "start_public_app.bat",
            "start_public_app.ps1",
        }
        and path.suffix != ".log"
    ]


def main() -> None:
    problems: list[str] = []

    for path in _tracked_files():
        relative = path.relative_to(APP_DIR)
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            problems.append(f"公開禁止の形式です: {relative}")
        if path.name.lower() in FORBIDDEN_NAMES:
            problems.append(f"公開禁止のファイルです: {relative}")

        if path.name == Path(__file__).name:
            continue

        if path.suffix.lower() not in {
            ".py",
            ".md",
            ".txt",
            ".json",
            ".toml",
            "",
        }:
            continue

        try:
            text = path.read_text(encoding="utf-8").lower()
        except UnicodeDecodeError:
            continue
        for forbidden in FORBIDDEN_TEXT:
            if forbidden in text:
                problems.append(
                    f"個人情報・秘密情報の可能性があります: "
                    f"{relative} ({forbidden})"
                )

    if not SNAPSHOT_PATH.exists():
        problems.append("data/public_snapshot.json がありません。")
    else:
        try:
            snapshot = json.loads(
                SNAPSHOT_PATH.read_text(encoding="utf-8")
            )
        except json.JSONDecodeError as error:
            problems.append(f"公開JSONが壊れています: {error}")
        else:
            if set(snapshot) != EXPECTED_KEYS:
                problems.append(
                    "公開JSONの項目構成が想定と異なります。"
                )
            if len(snapshot.get("candidates", [])) > 5:
                problems.append(
                    "公開候補が5銘柄を超えています。"
                )

    if problems:
        print("公開前チェックで問題が見つかりました。")
        for problem in problems:
            print(f"- {problem}")
        raise SystemExit(1)

    print("公開前チェック: 問題ありません。")
    print(f"確認ファイル数: {len(_tracked_files())}")


if __name__ == "__main__":
    main()
