# tennis_site_manager_tokyo
東京都のテニスコート予約サイトを対象にした自動化ツールです。  
予約監視と、抽選申込みの自動実行に対応しています。

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
- Python 3.11 以上
- Homebrew インストール済み

### 2. 仮想環境作成
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. ライブラリインストール
```bash
python -m pip install playwright python-dotenv
```

### 4. Playwright セットアップ
```bash
python -m playwright install
python -m playwright install-deps chromium
```
- `install-deps` は主に Linux 向けです。
- macOS で `install-deps` が失敗しても、`playwright install` が成功していれば通常は問題ありません。

### 5. `.env` 作成
プロジェクトルートに `.env` を作成し、最低限以下を設定してください。
```env
# 予約監視（LINE通知）で使用
CHANNEL_ACCESS_TOKEN=xxxx
USER_ID=xxxx

# 抽選アカウントのフォールバック用（単一アカウント）
# LOTTERY_ACCOUNTS_JSON が未設定 / 読み込み失敗時に使用
TOKYO_TENNIS_USER_ID=xxxx
TOKYO_TENNIS_PASSWORD=xxxx

# 抽選アカウント一覧（こちらが優先）
LOTTERY_ACCOUNTS_JSON=lottery_accounts.json
```
- 抽選を JSON 運用する場合、`TOKYO_TENNIS_USER_ID` / `TOKYO_TENNIS_PASSWORD` は基本的に使われません。

## 実行方法
エントリポイントは `tennis_watch/main.py` です。  
`MODE` を切り替えて実行します。

```bash
python tennis_watch/main.py
```

### MODE 一覧
- `check`: 予約監視の単発テスト
- `watch`: 予約監視の常駐実行
- `lottery_apply_debug`: 抽選申込みフロー実行（デバッグ用途）

## テニスコート自動抽選の使い方
### 1. 抽選対象を設定
`tennis_watch/shared/config/lottery_config.py` の `LOTTERY_TARGETS` を編集します。

各項目:
- `enabled`: その条件を申し込むかどうか（`True` / `False`）
- `category_label`: 種別（例: `テニス（ハード）`）
- `park_label`: 公園名（プルダウン表示名と完全一致）
- `facility_label`: 施設名（プルダウン表示名と完全一致）
- `ymd`: 日付（`YYYYMMDD`）
- `time`: 時刻（例: `13:00`）
- `apply_slot`: 申込み番号（`1` または `2`）

### 2. アカウント情報を設定
抽選実行時の読み込み優先順位:
1. `LOTTERY_ACCOUNTS_JSON` で指定した JSON
2. `.env` の連番変数（`TOKYO_TENNIS_USER_ID_1` / `TOKYO_TENNIS_PASSWORD_1` ...）
3. `.env` の単一アカウント（`TOKYO_TENNIS_USER_ID` / `TOKYO_TENNIS_PASSWORD`）

### 3. 実行
`tennis_watch/main.py` で `MODE = "lottery_apply_debug"` に設定して実行します。

```bash
python tennis_watch/main.py
```

## 抽選申込みで必要なデータ / ファイル
### 1. 抽選条件ファイル
- `tennis_watch/shared/config/lottery_config.py`
- 申し込みたい公園・施設・日時・申込枠を定義

### 2. アカウントJSON（任意）
- 例: `lottery_accounts.json`
- `.env` に `LOTTERY_ACCOUNTS_JSON=lottery_accounts.json` を設定して使用

JSON 形式例:
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

## 関連設定ファイル
- 監視対象コート設定: `tennis_watch/apps/reserve_watch/config/courts_config.py`
- 全体設定: `tennis_watch/shared/config/settings.py`
- 抽選対象設定: `tennis_watch/shared/config/lottery_config.py`
- 認証情報読み込み: `tennis_watch/shared/infra/auth/credentials.py`

## 注意事項
- `.env` / `.venv` / `.last_notify_hash` / 認証情報JSON は Git 管理しない
- 本番アカウント運用前に、テスト用条件で動作確認する
- サイト側の表示変更により自動操作が失敗する場合がある
- 最新の利用規約・運用ルールを確認して利用する
