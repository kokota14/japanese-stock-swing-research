from __future__ import annotations

import streamlit as st

from public_data import (
    format_percent,
    format_yen,
    load_public_snapshot,
)


snapshot = load_public_snapshot()
market = snapshot["market"]
portfolio = snapshot["paper_portfolio"]
learning = snapshot["learning"]

st.title("週次の検証記録")
st.caption(
    "公開用データから、検証の進み具合と次の課題をまとめています。"
)
st.caption(f"更新: {snapshot['updated_at']}")

with st.container(horizontal=True):
    with st.container(border=True):
        st.metric("市場判定", market["judgment"])
    with st.container(border=True):
        st.metric("現金比率の目安", f"{market['cash_ratio']}%")
    with st.container(border=True):
        st.metric(
            "仮想口座の総資産",
            format_yen(portfolio["total_assets"]),
            format_percent(portfolio["return_pct"]),
        )
    with st.container(border=True):
        st.metric(
            "評価済み予想",
            f"{learning['evaluated_predictions']}件",
        )

st.subheader("今週の検証")
with st.container(border=True):
    st.markdown(f"**仮説:** {learning['current_experiment']}")
    st.markdown(f"**途中経過:** {learning['finding']}")
    st.markdown(f"**次に試すこと:** {learning['next_experiment']}")

st.subheader("検証条件")
with st.container(border=True):
    st.markdown(
        f"- 往復売買コスト: "
        f"{snapshot['assumptions']['round_trip_cost_pct']:.2f}%\n"
        f"- 基本保有期間: "
        f"{snapshot['assumptions']['default_holding_days']}営業日\n"
        f"- データ: {snapshot['data_source']}\n"
        f"- モデル: {snapshot['model_version']}"
    )

st.warning(
    "このページは仮想売買の検証記録です。"
    "特定銘柄の売買を勧めるものではありません。"
)
