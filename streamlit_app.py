from __future__ import annotations

import streamlit as st


st.set_page_config(
    page_title="日本株スイング研究ノート",
    page_icon="📊",
    layout="wide",
)

st.html(
    """
    <script>
    document.documentElement.lang = "ja";
    document.documentElement.setAttribute("translate", "no");
    document.documentElement.classList.add("notranslate");

    if (!document.querySelector('meta[name="google"]')) {
        const meta = document.createElement("meta");
        meta.name = "google";
        meta.content = "notranslate";
        document.head.appendChild(meta);
    }
    </script>
    """,
    unsafe_allow_javascript=True,
)

page = st.navigation(
    [
        st.Page(
            "app_pages/dashboard.py",
            title="学習ダッシュボード",
            icon=":material/monitoring:",
            default=True,
        ),
        st.Page(
            "app_pages/weekly_report.py",
            title="週次の検証記録",
            icon=":material/article:",
        ),
        st.Page(
            "app_pages/methodology.py",
            title="検証方法",
            icon=":material/science:",
        ),
    ],
    position="top",
)

page.run()
