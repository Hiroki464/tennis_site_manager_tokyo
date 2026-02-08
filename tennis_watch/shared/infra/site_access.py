 # tennis_watch/shared/infra/site_access.py
from playwright.sync_api import Page

SYSTEM_ERROR_TITLE = "施設予約システムからのお知らせ"
SYSTEM_ERROR_MSG = "現在、ご指定のページはアクセスできません。"


def is_system_error_page(page: Page) -> bool:
    try:
        body = page.inner_text("body")
    except Exception:
        return False

    return (SYSTEM_ERROR_TITLE in body) and (SYSTEM_ERROR_MSG in body)


def open_top_with_auto_refresh(
    page: Page,
    url: str,
    max_refresh: int = 30,
    wait_sec: int = 20,
) -> bool:
    """
    url を開く。
    エラー画面（施設予約システムからのお知らせ）なら wait_sec 秒おきに reload して復帰待ち。
    """
    try:
        page.goto(url, timeout=30000)
        page.wait_for_load_state("networkidle")
    except Exception:
        return False

    # 正常なら即OK
    if not is_system_error_page(page):
        return True

    # エラーならリロードで粘る
    for _ in range(max_refresh):
        try:
            page.wait_for_timeout(wait_sec * 1000)
            page.reload(wait_until="networkidle", timeout=30000)
        except Exception:
            continue

        if not is_system_error_page(page):
            return True

    return False