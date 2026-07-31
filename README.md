# 日本株スイング研究ノート（一般公開・無料版）

私用の分析アプリとは分離し、公開用に整形した
`data/public_snapshot.json` だけを表示するStreamlitアプリです。

## 起動

最も簡単な方法は、`start_public_app.bat`をダブルクリックすることです。

ターミナルから起動する場合：

```powershell
python -m streamlit run streamlit_app.py
```

## 非公開版からの自動更新

非公開版の日次更新が完了すると、`public_snapshot_export.py` が公開用JSONを
作り直します。公開する項目は次の集計値だけです。

- 更新日時
- 市場判定・市場スコア・現金比率の目安
- 仮想口座の開始資金・総資産・損益率
- 評価済み予想件数と学習状況
- ランキング上位5銘柄のコード・名称・市場・点数・判定

保有株数、売買履歴、個人設定、SQLiteデータベースは公開版へコピーしません。
公開先を変更する場合は、環境変数 `SWING_PUBLIC_SNAPSHOT_PATH` に
`public_snapshot.json` の保存先を指定できます。

## 公開前の確認

- 実口座、保有資産、個人情報を含めない
- APIキーやローカルパスを含めない
- 仮想売買であることを明記する
- 成功例だけでなく失敗例も公開する
- 銘柄一覧は「推奨」ではなく「機械的な抽出結果」と表現する

次のコマンドで、公開禁止ファイル・PC内パス・秘密情報・JSON構成を
まとめて確認できます。

```powershell
python verify_public_release.py
```

## GitHubとStreamlit Community Cloudで公開

1. この `public_free_app` フォルダだけをGitHubへ登録します。
2. Streamlit Community Cloudで「Create app」を選びます。
3. GitHubリポジトリと `streamlit_app.py` を指定します。
4. Pythonは3.12以上を選び、Deployを実行します。

公開に必要なファイルは、`streamlit_app.py`、`app_pages/`、
`public_data.py`、`data/public_snapshot.json`、
`requirements.txt`、`.streamlit/config.toml`です。

ローカル専用の起動ファイル、ログ、仮想環境、DB、pickle、秘密設定は
`.gitignore`によりGitHubの対象外になります。

## 現在の画面

- 学習ダッシュボード
- 週次の検証記録
- 検証方法
