# shared/tool/login_debug.py
from playwright.sync_api import sync_playwright
from shared.infra.auth.login_service import LoginService
from shared.infra.auth.credentials import load_credentials
from shared.config.settings import RESULT_URL

def main():
    cred = load_credentials()
    svc = LoginService(RESULT_URL)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        ok = svc.login(page, cred)
        print("login result:", ok)

        input("ログイン結果を確認したら Enter")
        browser.close()

if __name__ == "__main__":
    main()