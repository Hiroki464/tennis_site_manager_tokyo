# shared/config/settings.py
from pathlib import Path

# ---- 動作設定 ----
WEEKEND_ONLY = True          # 土日だけを見るなら True
SEND_LINE = True             # LINE通知するなら True
RESULT_URL = "https://kouen.sports.metro.tokyo.lg.jp/web/index.jsp"

# ---- 障害・重複通知対策 ----
ERROR_LIMIT = 5              # SITE_ERROR が連続何回で障害通知するか
HASH_FILE = Path(".last_notify_hash")  # 前回通知内容のハッシュ保存用（project直下）

# ---- リトライ系 ----
TOP_OPEN_TIMEOUT_MS = 30_000      # gotoのタイムアウト
MAX_REFRESH = 30                  # エラー画面時の最大リロード回数
REFRESH_WAIT_SEC = 20             # 何秒ごとにリロードするか
MONTH_WAIT_TIMEOUT_MS = 60_000    # 月表示の最大待ち時間（最大1分）

# ---- 監視ループ ----
INTERVAL_MIN = 10                 # 監視間隔（分）
