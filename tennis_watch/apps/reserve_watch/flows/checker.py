# apps/reserve_watch/flows/checker.py
import re
from datetime import date
from collections import defaultdict

from shared.config import settings
from shared.notify.line_notify import send_line_message
from shared.utils import hashing
from shared.infra.browser import BrowserSession

from apps.reserve_watch.config.courts_config import COURTS
from apps.reserve_watch.pages.home_page import (
    open_top_with_auto_refresh,
    go_home,
    set_search_conditions,
    click_search,
)
from apps.reserve_watch.pages.month_view_page import (
    expand_month_view,
    collect_vacancies_from_month_view,
)

# 戻り値
#   "SITE_ERROR"  … サイト・ブラウザ障害
#   "NO_VACANCY"  … 空きが1件もない
#   "NO_CHANGE"   … 前回通知内容と同一で送信スキップ
#   "SENT"        … 新しい内容をLINEに送信


def check_courts_months(headless: bool = True) -> str:
    today_str = date.today().strftime("%Y-%m-%d")
    print("検索起点日:", today_str)
    print("土日のみ:", settings.WEEKEND_ONLY)

    target_courts = [c for c in COURTS if c.get("enabled", True)]
    if not target_courts:
        print("有効なコートがありません（enabled=True が0）")
        return "SITE_ERROR"

    all_vacancies: list[dict] = []

    try:
        with BrowserSession(headless=headless) as bs:
            page = bs.page

            # 最初のアクセス：直叩き＋20秒ごと自動リロード待ち
            if not open_top_with_auto_refresh(page):
                print("⚠ トップページに到達できず → 障害扱い")
                return "SITE_ERROR"

            for idx, court in enumerate(target_courts):
                print("\n==================================================")
                print(f"【検索中】{court['name']}")
                print("==================================================")

                if idx > 0:
                    if not go_home(page):
                        return "SITE_ERROR"

                if not set_search_conditions(
                    page,
                    date_str=today_str,
                    purpose_label=court["purpose_label"],
                    select_label=court["select_label"],
                ):
                    return "SITE_ERROR"

                if not click_search(page):
                    return "SITE_ERROR"

                if not expand_month_view(page):
                    return "SITE_ERROR"

                vacancies = collect_vacancies_from_month_view(page, settings.WEEKEND_ONLY)
                for v in vacancies:
                    v["court"] = court["name"]
                all_vacancies.extend(vacancies)

    except Exception as e:
        print("⚠ 予期せぬ例外 → 障害扱い:", e)
        return "SITE_ERROR"

    if not all_vacancies:
        print("全コートで空きなし")
        return "NO_VACANCY"

    # 日付順
    def sort_key(v):
        m = re.search(r"(\d{4})年(\d{1,2})月(\d{1,2})日", v["date"])
        if m:
            return int(m.group(1)), int(m.group(2)), int(m.group(3))
        return (9999, 99, 99)

    all_vacancies.sort(key=sort_key)

    grouped = defaultdict(list)
    for v in all_vacancies:
        grouped[v["court"]].append(v)

    # メッセージ生成
    header = "【テニス空きあり（月表示／複数コート）】\n"
    if settings.WEEKEND_ONLY:
        header += "※土日のみ\n"
    header += "---------------------\n"

    lines: list[str] = []
    for court in target_courts:
        name = court["name"]
        items = grouped.get(name, [])
        if not items:
            continue

        lines.append(f"■{name}")
        lines.append("空きコート数：")
        for v in items:
            lines.append(f"{v['date']}（{v['weekday']}） {v['symbol']} {v['status']}")
        lines.append("")

    message = header + "\n".join(lines).rstrip() + f"\n予約サイト：\n{settings.RESULT_URL}"

    # 重複通知防止（ハッシュ）
    if hashing.is_same_as_last(message, settings.HASH_FILE):
        print("前回と同じ結果 → 通知スキップ")
        return "NO_CHANGE"

    hashing.update_last(message, settings.HASH_FILE)

    print("送信メッセージ:\n", message)
    send_line_message(message)
    return "SENT"