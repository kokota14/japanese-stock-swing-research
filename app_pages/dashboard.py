from __future__ import annotations

import pandas as pd
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

st.title("日本株スイング研究ノート")
st.caption(
    "予想・仮想売買・検証・改善の過程を、成功例も失敗例も含めて公開します。"
)

with st.container(border=True):
    st.markdown("#### 最新の学習状況")
    st.caption(
        f"更新：{snapshot['updated_at']}　｜　"
        f"モデル：{snapshot['model_version']}　｜　"
        f"データ：{snapshot['data_source']}"
    )

    with st.container(horizontal=True):
        st.metric(
            "市場判定",
            market["judgment"],
            f"市場スコア {market['score']}点",
            delta_color="off",
            border=True,
        )
        st.metric(
            "現金比率の目安",
            f"{market['cash_ratio']}%",
            border=True,
        )
        st.metric(
            "仮想口座の総資産",
            format_yen(portfolio["total_assets"]),
            format_percent(portfolio["return_pct"]),
            border=True,
        )
        st.metric(
            "評価済み予想",
            f"{learning['evaluated_predictions']}件",
            border=True,
        )

st.subheader("今回の検証")
with st.container(border=True):
    st.markdown(f"**仮説**：{learning['current_experiment']}")
    st.markdown(f"**途中経過**：{learning['finding']}")
    st.markdown(f"**次に試すこと**：{learning['next_experiment']}")

st.subheader("機械的に抽出された候補")
st.caption(
    "設定した採点条件による検証対象です。購入を推奨する一覧ではありません。"
)

candidates = pd.DataFrame(snapshot.get("candidates", []))
if candidates.empty:
    st.info("現在、公開対象の候補はありません。")
else:
    candidates = candidates.rename(
        columns={
            "security_code": "証券コード",
            "stock_name": "銘柄名",
            "market": "市場",
            "score": "点数",
            "judgment": "判定",
        }
    )
    st.dataframe(
        candidates,
        hide_index=True,
        width="stretch",
        column_config={
            "証券コード": st.column_config.TextColumn(width="small"),
            "銘柄名": st.column_config.TextColumn(width="large"),
            "市場": st.column_config.TextColumn(width="small"),
            "点数": st.column_config.ProgressColumn(
                min_value=0,
                max_value=100,
                format="%d点",
                width="medium",
            ),
            "判定": st.column_config.TextColumn(width="medium"),
        },
    )

st.warning(
    "このページは仮想売買と研究の記録です。"
    "特定銘柄の売買を勧めるものではなく、将来の利益を保証しません。"
)
