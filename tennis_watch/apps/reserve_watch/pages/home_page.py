# apps/reserve_watch/pages/home_page.py
import time
from playwright.sync_api import Page

from shared.config import settings
from shared.infra.site_access import open_top_with_auto_refresh


def open_top(page: Page) -> bool:
    """トップを開く（エラー画面なら自動リロードで復帰待ち）"""
    try:
        return open_top_with_auto_refresh(
            page=page,
            url=settings.RESULT_URL,
            max_refresh=settings.TOP_MAX_REFRESH,
            wait_sec=settings.TOP_WAIT_SEC,
        )
    except Exception as e:
        print("⚠ open_top 失敗:", e)
        return False


def go_home(page: Page) -> bool:
    """検索結果などからホームへ戻る"""
    try:
        page.locator("#nav-home").click()
        page.wait_for_load_state("networkidle")
        time.sleep(0.5)
        return True
    except Exception as e:
        print("⚠ nav-home が押せない:", e)
        return False


def set_search_conditions(page: Page, date_str: str, purpose_label: str, select_label: str) -> bool:
    """トップ画面の検索条件をセット"""
    try:
        page.locator("#daystart-home").fill("")
        page.locator("#daystart-home").fill(date_str)

        page.locator("#purpose-home").select_option(label=purpose_label)
        page.locator("#bname-home").select_option(label=select_label)
        return True
    except Exception as e:
        print("⚠ 検索条件セット失敗:", e)
        return False


def click_search(page: Page) -> bool:
    """検索実行"""
    try:
        page.locator("#btn-go").click()
        page.wait_for_load_state("networkidle")
        return True
    except Exception as e:
        print("⚠ 検索ボタン押下失敗:", e)
        return False