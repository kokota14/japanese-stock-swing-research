from __future__ import annotations

from typing import Any

from public_data import format_percent, format_yen


def _candidate_lines(snapshot: dict[str, Any]) -> str:
    candidates = snapshot.get("candidates", [])
    if not candidates:
        return "- 今週は公開対象の候補がありません。"

    return "\n".join(
        (
            f"- {row['security_code']} {row['stock_name']}："
            f"{row['score']}点（{row['market']}）"
        )
        for row in candidates
    )


def build_blog_markdown(snapshot: dict[str, Any]) -> str:
    """公開用の週次ブログ下書きを作る。"""

    market = snapshot["market"]
    portfolio = snapshot["paper_portfolio"]
    learning = snapshot["learning"]

    return f"""# 日本株スイング研究日記

更新日：{snapshot['updated_at']}

## 今週の概要

- 市場判定：{market['judgment']}
- 市場スコア：{market['score']}点
- 現金比率の目安：{market['cash_ratio']}%
- 仮想口座の総資産：{format_yen(portfolio['total_assets'])}
- 仮想口座の損益率：{format_percent(portfolio['return_pct'])}

## 機械的に抽出された候補

{_candidate_lines(snapshot)}

上記は設定した採点条件による抽出結果であり、購入を推奨するものではありません。

## 今週の検証

{learning['current_experiment']}

## 分かったこと

{learning['finding']}

## 次回試すこと

{learning['next_experiment']}

## 開示事項

- すべて仮想売買による検証です。
- 将来の値上がりや利益を保証するものではありません。
- データソースは{snapshot['data_source']}です。
- 株価データには遅延、欠損、訂正が含まれる可能性があります。
- 売買コストの前提：往復{snapshot['assumptions']['round_trip_cost_pct']:.2f}%
- モデルバージョン：{snapshot['model_version']}
"""


def build_video_script(snapshot: dict[str, Any]) -> str:
    """5～8分程度の動画台本を作る。"""

    market = snapshot["market"]
    portfolio = snapshot["paper_portfolio"]
    learning = snapshot["learning"]
    candidates = snapshot.get("candidates", [])
    candidate_text = "、".join(
        f"{row['security_code']} {row['stock_name']} {row['score']}点"
        for row in candidates[:5]
    ) or "該当なし"

    return f"""【0:00 オープニング】
日本株スイング分析ツールが、予想、仮想売買、検証を通して学習していく様子を記録します。
今回は{snapshot['updated_at']}時点の結果です。

【0:25 市場状況】
現在の市場判定は「{market['judgment']}」、市場スコアは{market['score']}点です。
現金比率の目安は{market['cash_ratio']}パーセントとしています。

【1:10 今週の候補】
設定した条件で機械的に抽出された上位候補は、{candidate_text}です。
これは購入推奨ではなく、検証対象の一覧です。

【2:10 仮想口座】
開始資金は{format_yen(portfolio['initial_capital'])}。
現在の総資産は{format_yen(portfolio['total_assets'])}、
開始時からの損益率は{format_percent(portfolio['return_pct'])}です。

【3:00 今週の検証】
{learning['current_experiment']}

【4:15 分かったこと】
{learning['finding']}

【5:20 次回の改善】
{learning['next_experiment']}

【6:10 注意事項】
この動画は仮想売買による学習記録です。
特定銘柄の購入を推奨するものではなく、将来の利益も保証しません。
データには遅延や欠損が含まれる可能性があります。
"""
