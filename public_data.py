from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import streamlit as st


APP_DIR = Path(__file__).resolve().parent
SNAPSHOT_PATH = APP_DIR / "data" / "public_snapshot.json"


@st.cache_data(ttl="5m", max_entries=2)
def load_public_snapshot() -> dict[str, Any]:
    """公開用に整形済みのスナップショットだけを読み込む。"""

    with SNAPSHOT_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def format_percent(value: float | None) -> str:
    if value is None:
        return "集計中"
    return f"{value:+.2f}%"


def format_yen(value: int | float | None) -> str:
    if value is None:
        return "集計中"
    return f"{value:,.0f}円"
