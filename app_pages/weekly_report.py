from __future__ import annotations

import streamlit as st

from content_generator import (
    build_blog_markdown,
    build_video_script,
)
from public_data import load_public_snapshot


snapshot = load_public_snapshot()
blog_markdown = build_blog_markdown(snapshot)
video_script = build_video_script(snapshot)

st.title("週次レポート")
st.caption(
    "同じ検証結果から、ブログの下書きと動画台本を作成します。"
)

blog_tab, video_tab = st.tabs(
    ["ブログ用", "動画用"],
    on_change="rerun",
)

if blog_tab.open:
    with blog_tab:
        st.markdown(blog_markdown)
        st.download_button(
            "ブログ下書きをダウンロード",
            data=blog_markdown.encode("utf-8-sig"),
            file_name="weekly_blog.md",
            mime="text/markdown",
            icon=":material/download:",
            width="stretch",
        )

if video_tab.open:
    with video_tab:
        st.text(video_script)
        st.download_button(
            "動画台本をダウンロード",
            data=video_script.encode("utf-8-sig"),
            file_name="weekly_video_script.txt",
            mime="text/plain",
            icon=":material/download:",
            width="stretch",
        )
