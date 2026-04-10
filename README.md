# tennis_site_manager_tokyo
東京都のテニスコート予約サイトを対象にした自動化ツールです。

現在は主に次の2機能があります。
- 空き状況の監視（予約監視）
- 抽選申込みの自動実行（複数アカウント対応）


## 機能
- 予約監視
  - テニスコート予約状況の監視（月表示）
  - コートごとの監視 ON / OFF 設定
  - 土日限定チェック対応
  - 同じ内容の重複通知防止
  - サイト障害時の自動リトライ
  - 障害が連続した場合のLINE通知
- 抽選自動
  - 抽選申込みの自動実行（アカウントごとに順次処理）


## 環境構築方法
### 1. 前提
- Python 3.11 以上を推奨
- Homebrew がインストール済みであること
- macOS / Linux の場合、以下のコマンド例をそのまま利用可能

### 2. 仮想環境作成
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. ライブラリインストール
```bash
pip install -r requirements.txt
```

### 4. Playwright インストール
Playwright 本体とブラウザ実行に必要な依存をインストールします。

```bash
python -m playwright install
python -m playwright install-deps chromium
```
※ `install-deps` は Linux 向けです。macOS では不要な場合があるため、エラーが出ても `install` が成功していれば基本的に問題ありません。

### 5. `.env` 作成
プロジェクトルートに `.env` を作成し、最低限以下を設定してください。

```env
# 監視系で使用（LINE通知）
CHANNEL_ACCESS_TOKEN=xxxx
USER_ID=xxxx
※ 予約監視で使用するため、抽選申込み自動化のみを使用する場合は不要です。

# ログインで使用（単一アカウント運用時 / JSON読込失敗時のフォールバック）
TOKYO_TENNIS_USER_ID=xxxx
TOKYO_TENNIS_PASSWORD=xxxx
```

※ 抽選を複数アカウントで実行する場合は、後述の「抽選申込みで必要なデータ/ファイル」を参照してください。  
※ `LOTTERY_ACCOUNTS_JSON` が有効な場合は JSON のアカウント情報が優先され、上記2項目は使われません。


## 実行方法
エントリポイントは `tennis_watch/main.py` です。  
`MODE` を切り替えて実行します。

### MODE 一覧
- `check`: 予約監視の単発テスト
- `watch`: 予約監視の常駐実行
- `lottery_apply_debug`: 抽選申込みフロー実行（デバッグ用途）


## テニスコート自動抽選の使い方
### 1. 抽選対象を設定
`tennis_watch/shared/config/lottery_config.py` の `LOTTERY_TARGETS` を編集します。

1件ごとに以下を指定します。
- `enabled`: その条件を申し込むかどうか（`True` / `False`）
- `category_label`: 種別（例: `テニス（ハード）`）
- `park_label`: 公園名（プルダウン表示名と完全一致）
- `facility_label`: 施設名（プルダウン表示名と完全一致）
- `ymd`: 日付（`YYYYMMDD`）
- `time`: 時刻（例: `13:00`）
- `apply_slot`: 申込み番号（1 または 2）

### 2. アカウント情報を設定
抽選実行時のアカウントは次の優先順位で読み込まれます。

1. `LOTTERY_ACCOUNTS_JSON` で指定した JSON ファイル
2. `.env` の連番変数（`TOKYO_TENNIS_USER_ID_1` / `TOKYO_TENNIS_PASSWORD_1` ...）
3. `.env` の単一アカウント（`TOKYO_TENNIS_USER_ID` / `TOKYO_TENNIS_PASSWORD`）

### 3. 実行
`tennis_watch/main.py` の `MODE = "lottery_apply_debug"` にして、次を実行します。


ブラウザを見ながら確認したい場合は、`run(headless=False)` のまま使用してください。


## 抽選申込みで必要なデータ/ファイル
### 1. 抽選条件ファイル
- `tennis_watch/shared/config/lottery_config.py`
- 申し込みたい公園・施設・日時・申込枠をここで定義

### 2. アカウントJSON（任意）
- 例: `lottery_accounts.json`
- `.env` に `LOTTERY_ACCOUNTS_JSON=./lottery_accounts.json` のように指定して利用

JSON形式の例:
```json
[
  {
    "enabled": true,
    "user_id": "your_id",
    "password": "your_password",
    "name": "表示名"
  }
]
```

### 3. `.env`
- 単一アカウントまたは連番アカウントの認証情報
- JSONを使う場合は `LOTTERY_ACCOUNTS_JSON` の設定も追加


## 関連設定ファイル
- 監視対象コート設定: `tennis_watch/apps/reserve_watch/config/courts_config.py`
- 全体設定: `tennis_watch/shared/config/settings.py`
- 抽選対象設定: `tennis_watch/shared/config/lottery_config.py`
- 認証情報読み込み: `tennis_watch/shared/infra/auth/credentials.py`


## 注意事項
- `.env` / `.venv` / `.last_notify_hash` / 認証情報JSONは Git 管理しないでください
- 本番アカウントで運用する前に、テスト用条件で必ず動作確認してください
- サイト側の表示変更により自動操作が失敗する場合があります
- 実際の運用ルール・規約は利用サイトの最新規約を確認してください
