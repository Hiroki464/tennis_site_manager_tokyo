# tennis_site_manager_tokyo
東京都のテニスコート予約サイトを対象にした監視ツール。
指定したコート・種別（ハード / 人工芝）について、
月表示カレンダーから空き状況を取得し、LINE通知する。

将来的に「抽選申込み機能」も追加予定。

## 機能

- テニスコート予約状況の監視（月表示）
- ハード / 人工芝コートの切り替え対応
- コートごとの監視 ON / OFF 設定
- 土日限定チェック対応
- 同じ内容の重複通知防止
- サイト障害時の自動リトライ
- 障害が連続した場合のLINE通知


## フォルダ構成

project_root/
├─ main.py                  # 実行入口
├─ tennis_watch/
│  ├─ apps/
│  │  ├─ reserve_watch/     # 予約監視アプリ
│  │  │  ├─ flows/          # 処理の流れ
│  │  │  ├─ pages/          # Playwright操作
│  │  │  └─ config/         # コート設定
│  │  └─ lottery/           # 将来追加予定
│  └─ shared/               # 共通処理
├─ .env                     # 環境変数（Git管理外）
├─ .gitignore

## セットアップ

### 1. 仮想環境作成
python -m venv .venv
source .venv/bin/activate

### 2. ライブラリインストール
pip install -r requirements.txt

### 3. 環境変数設定
.env を作成し、以下を設定する。

CHANNEL_ACCESS_TOKEN=xxxx
USER_ID=xxxx


## 実行方法

### 単発実行（デバッグ）
python main.py

### 定期監視
main.py 内で loop_watch を有効にする。


## 設定について

- コート設定：apps/reserve_watch/config/courts_config.py
  - enabled = True / False で監視切り替え
  - purpose_label で ハード / 人工芝 を指定

- 全体設定：shared/config/settings.py
  - SEND_LINE
  - ERROR_LIMIT
  - 監視間隔
 
## 注意事項

- .env / .venv / .last_notify_hash は Git 管理しない
- サイト側の制限により、初回アクセス時にエラー画面が出る場合がある
- 自動リロード処理により復帰を待つ仕様


## TODO

- 抽選申込み機能の実装
- ログイン処理の共通化
- 曜日ごとのON/OFF設定
