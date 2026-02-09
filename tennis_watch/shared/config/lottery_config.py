# tennis_watch/apps/lottery/config/lottery_config.py
from dataclasses import dataclass

# 種別は完全一致
TENNIS_HARD = "テニス（ハード）"
TENNIS_TURF = "テニス（人工芝）"


@dataclass(frozen=True)
class LotteryTarget:
    """
    抽選の対象条件（まずは1件だけ）
    """
    enabled: bool
    category_label: str   # 「テニス（ハード）」or「テニス（人工芝）」完全一致
    park_label: str       # 公園プルダウンで表示される名前（label）
    facility_label: str   # 施設プルダウンで表示される名前（label）
    ymd: str              # "YYYYMMDD" 例: "20260307"
    time: str             # "7:00" や "13:00"（半角コロンOK）
    apply_slot: int       # 申込み番号：1=申込み1件目, 2=申込み2件目


@dataclass(frozen=True)
class LotteryConfig:
    max_next_week: int = 5         # 翌週ボタンの最大押下回数
    usedate_timeout_ms: int = 60000


# まずは1件だけでいい（複数候補はいらない）
LOTTERY_TARGET = LotteryTarget(
    enabled=True,
    category_label=TENNIS_HARD,           # テニス（ハード） or テニス（人工芝）
    park_label="大井ふ頭中央海浜公園Ｂ",      # 公園ラベル
    facility_label=TENNIS_HARD,           # 施設ラベル（同じ表示名でも公園でvalueは変わるのでlabel指定）
    ymd="20260326",                       # 日付
    time="15:00",                         # 時間（7:00,9:00,11:00,13:00,15:00,17:00）
    apply_slot=2,                         # 1=申込み1件目 / 2=申込み2件目
)

CONFIG = LotteryConfig()