# tennis_watch/shared/config/lottery_config.py
from dataclasses import dataclass

# 種別は完全一致
TENNIS_HARD = "テニス（ハード）"
TENNIS_TURF = "テニス（人工芝）"


@dataclass(frozen=True)
class LotteryTarget:
    """
    抽選の1件分の条件。enabled=False のものは申し込まない。
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


# 1アカウントあたり最大4回：ハード1件目・2件目、人工芝1件目・2件目。enabled で申し込む/申し込まないを切り替え。
LOTTERY_TARGETS = (
    LotteryTarget(enabled=True, category_label=TENNIS_HARD, park_label="大井ふ頭中央海浜公園Ｂ", facility_label=TENNIS_HARD, ymd="20260326", time="13:00", apply_slot=1),  # 1回目: ハード, 申込1件目
    LotteryTarget(enabled=False, category_label=TENNIS_HARD, park_label="大井ふ頭中央海浜公園Ｂ", facility_label=TENNIS_HARD, ymd="20260326", time="15:00", apply_slot=2),  # 2回目: ハード, 申込2件目
    LotteryTarget(enabled=False, category_label=TENNIS_TURF, park_label="東大和南公園", facility_label=TENNIS_TURF, ymd="20260326", time="13:00", apply_slot=1),  # 3回目: 人工芝, 申込1件目
    LotteryTarget(enabled=False, category_label=TENNIS_TURF, park_label="東大和南公園", facility_label=TENNIS_TURF, ymd="20260326", time="15:00", apply_slot=2),  # 4回目: 人工芝, 申込2件目
)

CONFIG = LotteryConfig()