from __future__ import annotations

import streamlit as st

from public_data import load_public_snapshot


snapshot = load_public_snapshot()
assumptions = snapshot["assumptions"]

st.title("検証方法")
st.caption("結果を後から都合よく変えないための基本ルールです。")

st.subheader("学習の流れ")
st.markdown(
    """
1. 予想時点のデータと採点ルールを保存する
2. 仮想口座で売買を記録する
3. 決めた保有期間が終わったら実績を評価する
4. TOPIXなどの市場平均と比較する
5. 成績が悪かった理由を分類する
6. 改善案を別期間のデータでも再検証する
7. 再現した変更だけを採用候補にする
"""
)

st.subheader("現在の前提")
assumption_rows = {
    "売買": "仮想売買のみ",
    "往復売買コスト": (
        f"{assumptions['round_trip_cost_pct']:.2f}%"
    ),
    "標準保有期間": (
        f"{assumptions['default_holding_days']}営業日"
    ),
    "データソース": snapshot["data_source"],
    "モデルバージョン": snapshot["model_version"],
}

for label, value in assumption_rows.items():
    with st.container(horizontal=True):
        st.markdown(f"**{label}**")
        st.write(value)

st.subheader("公開方針")
st.markdown(
    """
- 良い結果だけでなく、失敗や未評価の結果も残します。
- 予想後にルールや目標価格を書き換えません。
- 取引件数が少ない結果は、参考値として明記します。
- 手数料などの計算前提を記載します。
- 個人の実口座、保有資産、認証情報は公開しません。
"""
)

st.info(
    "このサイトは一般的な情報提供と学習記録を目的としています。"
    "個別の投資判断は、ご自身の責任で行ってください。"
)
