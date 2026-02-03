# apps/reserve_watch/pages/month_view_page.py
import re
from datetime import date
from shared.config import settings


def get_year_month_from_page(page) -> tuple[int | None, int | None]:
    txt = page.inner_text("body")
    m = re.search(r"(\d{4})年\s*(\d{1,2})月", txt)
    if not m:
        return None, None
    return int(m.group(1)), int(m.group(2))


def expand_month_view(page) -> bool:
    """月表示の折りたたみを展開"""
    try:
        page.locator('div.collapse-btn-right[data-target="#monthly"]').click()
        return True
    except Exception as e:
        print("⚠ 月表示が展開できない:", e)
        return False


def collect_vacancies_from_month_view(page, weekend_only: bool) -> list[dict]:
    """
    月表示カレンダーから、○ / △ の日を抽出する。
    """
    try:
        page.wait_for_selector("#month-info td img", timeout=settings.MONTH_WAIT_TIMEOUT_MS)
    except Exception as e:
        print("⚠ 月表示読み込みタイムアウト:", e)
        return []

    month_table = page.locator("#month-info")
    rows = month_table.locator("tbody tr")
    year, month = get_year_month_from_page(page)

    if not year or not month:
        # 年月が取れないと日付計算が崩れるので、ここは空扱いで戻す
        print("⚠ 年月が取得できない（ページ表示が不正の可能性）")
        return []

    results: list[dict] = []

    for r in range(rows.count()):
        row = rows.nth(r)
        cells = row.locator("td")

        for c in range(cells.count()):
            cell = cells.nth(c)

            txt = cell.inner_text().strip()
            md = re.search(r"(\d+)", txt)
            if not md:
                continue

            day = int(md.group(1))

            # 曜日
            try:
                d = date(year, month, day)
                week_chars = ["月", "火", "水", "木", "金", "土", "日"]
                w = d.weekday()
                weekday_char = week_chars[w]
                is_weekend = (w in (5, 6))
            except Exception as e:
                print("日付計算エラー:", e)
                continue

            if weekend_only and not is_weekend:
                continue

            imgs = cell.locator("img")
            if imgs.count() == 0:
                continue

            symbol = None
            status = None

            for i in range(imgs.count()):
                src = imgs.nth(i).get_attribute("src") or ""
                if "calendar_available_outline" in src:
                    symbol, status = "○", "空き"
                    break
                elif "calendar_few-available_outline" in src:
                    symbol, status = "△", "一部空き"
                    break
                elif "calendar_full_outline" in src:
                    symbol = "×"

            if symbol and symbol != "×":
                results.append({
                    "date": f"{year}年{month}月{day}日",
                    "weekday": weekday_char,
                    "symbol": symbol,
                    "status": status,
                })

    print("この月で見つけた空き日数:", len(results))
    return results