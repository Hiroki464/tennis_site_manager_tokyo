# tennis_watch/shared/infra/auth/login_service.py
from playwright.sync_api import Page

from shared.config import settings
from shared.infra.auth.credentials import Credentials
from shared.infra.site_access import open_top_with_auto_refresh


class LoginService:
    def __init__(self, result_url: str):
        self.result_url = result_url

    def login(self, page: Page, cred: Credentials) -> bool:
        """成功 True / 失敗 False"""

        # 1) トップへ（エラー画面ならリロード粘り）
        ok = open_top_with_auto_refresh(
            page=page,
            url=self.result_url,
            max_refresh=getattr(settings, "TOP_MAX_REFRESH", 30),
            wait_sec=getattr(settings, "TOP_WAIT_SEC", 20),
        )
        if not ok:
            print("⚠ トップ到達失敗（エラー画面復帰できず）")
            return False

        try:
            # 2) 右上「ログイン」ボタン（トップ画面のやつ）をIDで押す
            page.wait_for_selector("#btn-login", timeout=30000)
            page.locator("#btn-login").click()

            # 3) ログイン画面の入力欄待ち
            page.wait_for_selector('input[name="userId"], input[aria-label="利用者番号"]', timeout=30000)

            # 利用者番号・パスワード（roleは安定してるのでそのまま）
            page.get_by_role("textbox", name="利用者番号").fill(cred.user_id)
            page.get_by_role("textbox", name="パスワード").fill(cred.password)

            # 4) ログイン実行ボタン
            # ※このサイトはログイン画面側のボタンが #btn-go になってることがある
            page.wait_for_selector("#btn-go", timeout=30000)
            page.locator("#btn-go").click()

            page.wait_for_load_state("networkidle")
            return True

        except Exception as e:
            print("⚠ ログイン処理で例外:", e)
            return False