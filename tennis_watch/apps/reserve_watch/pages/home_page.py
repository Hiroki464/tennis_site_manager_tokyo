# apps/reserve_watch/pages/home_page.py
import re
from shared.config import settings


SYSTEM_ERR_KEY_1 = "施設予約システムからのお知らせ"
SYSTEM_ERR_KEY_2 = "現在、ご指定のページはアクセスできません。"


def is_system_error_page(page) -> bool:
    try:
        body_txt = page.inner_text("body")
        return (SYSTEM_ERR_KEY_1 in body_txt) and (SYSTEM_ERR_KEY_2 in body_txt)
    except Exception:
        return False


def open_top_with_auto_refresh(page) -> bool:
    """
    トップページを開く。
    エラー画面なら 20秒ごとに reload して復帰待ち（最大 settings.MAX_REFRESH 回）
    """
    try:
        print("トップページへアクセス中...")
        page.goto(settings.RESULT_URL, timeout=settings.TOP_OPEN_TIMEOUT_MS)
        page.wait_for_load_state("networkidle")
    except Exception as e:
        print("トップページへの初回アクセス失敗:", e)
        return False

    if not is_system_error_page(page):
        print("トップページ正常表示。")
        return True

    print("『施設予約システムからのお知らせ』エラー画面を検出。")
    print(f"{settings.REFRESH_WAIT_SEC}秒ごとに再読み込み（最大 {settings.MAX_REFRESH} 回）で復帰待ち。")

    for i in range(1, settings.MAX_REFRESH + 1):
        print(f"[リロード {i}回目] {settings.REFRESH_WAIT_SEC}秒待機中…")
        page.wait_for_timeout(settings.REFRESH_WAIT_SEC * 1000)

        try:
            page.reload(wait_until="networkidle")
        except Exception as e:
            print("reload 中にエラー:", e)
            continue

        if not is_system_error_page(page):
            print("エラー画面から正常画面へ復帰した。")
            return True

        print("まだエラー画面のまま。")

    print("最大リロード回数に達しても復帰せず → 障害扱い。")
    return False


def go_home(page) -> bool:
    """結果画面からホームへ戻る（#nav-home）。失敗したら False"""
    try:
        page.locator("#nav-home").click()
        page.wait_for_load_state("networkidle")
        return True
    except Exception as e:
        print("⚠ nav-home が押せない:", e)
        return False


def set_search_conditions(page, date_str: str, purpose_label: str, select_label: str) -> bool:
    """トップ画面の検索条件入力。失敗したら False"""
    try:
        date_input = page.locator("#daystart-home")
        date_input.fill("")
        date_input.fill(date_str)

        page.locator("#purpose-home").select_option(label=purpose_label)
        page.locator("#bname-home").select_option(label=select_label)
        return True
    except Exception as e:
        print("⚠ 検索条件セット失敗:", e)
        return False


def click_search(page) -> bool:
    """検索ボタン押下。失敗したら False"""
    try:
        page.locator("#btn-go").click()
        page.wait_for_load_state("networkidle")
        return True
    except Exception as e:
        print("⚠ 検索クリック失敗:", e)
        return False