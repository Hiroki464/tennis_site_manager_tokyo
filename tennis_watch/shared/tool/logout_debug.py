# tennis_watch/shared/tool/logout_debug.py
from playwright.sync_api import sync_playwright

from shared.config import settings
from shared.infra.site_access import open_top_with_auto_refresh
from shared.infra.auth.credentials import load_credentials
from shared.infra.auth.login_service import LoginService
from shared.infra.auth.logout_service import LogoutService


def main():
    cred = load_credentials()
    login_svc = LoginService(settings.RESULT_URL)
    logout_svc = LogoutService()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 例の「最初エラー画面→リロード復帰」対策込みでトップを開く
        ok = open_top_with_auto_refresh(page, url=settings.RESULT_URL)
        if not ok:
            print("⚠ トップが開けない（障害画面から復帰できない）")
            browser.close()
            return

        # ログイン
        ok = login_svc.login(page, cred)
        if not ok:
            print("⚠ ログイン失敗")
            browser.close()
            return

        print("✅ ログイン成功。次にログアウトする。")

        # ログアウト
        ok = logout_svc.logout(page)
        if not ok:
            print("⚠ ログアウト失敗")
            browser.close()
            return

        print("✅ ログアウト成功。画面確認して Enter で終了。")
        input()
        browser.close()


if __name__ == "__main__":
    main()