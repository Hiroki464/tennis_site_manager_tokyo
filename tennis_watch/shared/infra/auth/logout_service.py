# tennis_watch/shared/infra/auth/logout_service.py
import re
from playwright.sync_api import Page


class LogoutService:
    """
    東京都の施設予約サイト用 ログアウト処理（共通部品）
    - 「マイメニュー」→「ログアウト」
    """

    def logout(self, page: Page) -> bool:
        try:
            # まずページが落ち着くまで待つ
            page.wait_for_load_state("networkidle")
        except Exception:
            # networkidle が安定しない時があるので無視して進める
            pass

        # 1) マイメニューを開く
        try:
            # アイコン文字が混ざるので "マイメニュー" で拾う
            page.get_by_role("link", name=re.compile("マイメニュー")).click()
        except Exception as e:
            print("⚠ マイメニューが押せない:", e)
            return False

        # 2) ログアウトを押す
        try:
            page.get_by_role("link", name=re.compile("ログアウト")).click()
        except Exception as e:
            print("⚠ ログアウトが押せない:", e)
            return False

        # 3) ログアウト完了確認（ログインボタンが見える/トップに戻る等）
        # ここはサイト仕様で揺れるから「ベストエフォート」にしておく
        try:
            page.wait_for_load_state("networkidle")
        except Exception:
            pass

        return True