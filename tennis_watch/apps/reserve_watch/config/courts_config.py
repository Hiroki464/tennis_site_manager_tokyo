# apps/reserve_watch/config/courts_config.py
"""
テニスコート一覧の設定ファイル。
ハード / 人工芝 / 監視ON/OFF をここで管理する。
"""

HARD_PURPOSE = "テニス（ハード）"
TURF_PURPOSE = "テニス（人工芝）"

HARD_COURTS = [
    {"name": "大井ふ頭海浜公園A", "select_label": "大井ふ頭海浜公園Ａ", "purpose_label": HARD_PURPOSE, "enabled": False},
    {"name": "大井ふ頭海浜公園B", "select_label": "大井ふ頭海浜公園Ｂ", "purpose_label": HARD_PURPOSE, "enabled": True},
    {"name": "有明テニスA屋外ハードコート", "select_label": "有明テニスＡ屋外ハードコート", "purpose_label": HARD_PURPOSE, "enabled": True},
    {"name": "有明テニスBインドアコート", "select_label": "有明テニスＢインドアコート", "purpose_label": HARD_PURPOSE, "enabled": False},
]

TURF_COURTS = [
    {"name": "日比谷公園", "select_label": "日比谷公園", "purpose_label": TURF_PURPOSE, "enabled": False},
    {"name": "芝公園", "select_label": "芝公園", "purpose_label": TURF_PURPOSE, "enabled": False},
    {"name": "猿江恩賜公園", "select_label": "猿江恩賜公園", "purpose_label": TURF_PURPOSE, "enabled": False},
    {"name": "亀戸中央公園", "select_label": "亀戸中央公園", "purpose_label": TURF_PURPOSE, "enabled": False},
    {"name": "木場公園", "select_label": "木場公園", "purpose_label": TURF_PURPOSE, "enabled": False},
    {"name": "祖師谷公園", "select_label": "祖師谷公園", "purpose_label": TURF_PURPOSE, "enabled": False},
    {"name": "東白鬚公園", "select_label": "東白鬚公園", "purpose_label": TURF_PURPOSE, "enabled": False},
    {"name": "浮間公園", "select_label": "浮間公園", "purpose_label": TURF_PURPOSE, "enabled": False},
    {"name": "城北中央公園", "select_label": "城北中央公園", "purpose_label": TURF_PURPOSE, "enabled": False},
    {"name": "赤塚公園", "select_label": "赤塚公園", "purpose_label": TURF_PURPOSE, "enabled": False},
    {"name": "東綾瀬公園", "select_label": "東綾瀬公園", "purpose_label": TURF_PURPOSE, "enabled": False},
    {"name": "舎人公園", "select_label": "舎人公園", "purpose_label": TURF_PURPOSE, "enabled": False},
    {"name": "篠崎公園Ａ", "select_label": "篠崎公園Ａ", "purpose_label": TURF_PURPOSE, "enabled": False},
    {"name": "大島小松川公園", "select_label": "大島小松川公園", "purpose_label": TURF_PURPOSE, "enabled": False},
    {"name": "汐入公園", "select_label": "汐入公園", "purpose_label": TURF_PURPOSE, "enabled": False},
    {"name": "高井戸公園", "select_label": "高井戸公園", "purpose_label": TURF_PURPOSE, "enabled": False},
    {"name": "善福寺川緑地", "select_label": "善福寺川緑地", "purpose_label": TURF_PURPOSE, "enabled": False},
    {"name": "光が丘公園", "select_label": "光が丘公園", "purpose_label": TURF_PURPOSE, "enabled": False},
    {"name": "石神井公園Ｂ", "select_label": "石神井公園Ｂ", "purpose_label": TURF_PURPOSE, "enabled": False},
    {"name": "井の頭恩賜公園", "select_label": "井の頭恩賜公園", "purpose_label": TURF_PURPOSE, "enabled": False},
    {"name": "武蔵野中央公園", "select_label": "武蔵野中央公園", "purpose_label": TURF_PURPOSE, "enabled": False},
    {"name": "小金井公園", "select_label": "小金井公園", "purpose_label": TURF_PURPOSE, "enabled": False},
    {"name": "野川公園", "select_label": "野川公園", "purpose_label": TURF_PURPOSE, "enabled": False},
    {"name": "府中の森公園", "select_label": "府中の森公園", "purpose_label": TURF_PURPOSE, "enabled": False},
    {"name": "東大和南公園", "select_label": "東大和南公園", "purpose_label": TURF_PURPOSE, "enabled": False},
    {"name": "大井ふ頭海浜公園Ｂ（人工芝）", "select_label": "大井ふ頭海浜公園Ｂ", "purpose_label": TURF_PURPOSE, "enabled": False},
    {"name": "有明テニスＣ人工芝コート", "select_label": "有明テニスＣ人工芝コート", "purpose_label": TURF_PURPOSE, "enabled": False},
]

COURTS = HARD_COURTS + TURF_COURTS