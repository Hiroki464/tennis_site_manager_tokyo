# tennis_watch/shared/tool/lottery_apply_debug.py
from playwright.sync_api import sync_playwright

from shared.config.settings import RESULT_URL
from shared.infra.auth.credentials import load_credentials_list
from shared.infra.auth.login_service import LoginService
from shared.infra.auth.logout_service import LogoutService

from apps.lottery.pages.lottery_apply_list_page import LotteryApplyListPage
from apps.lottery.pages.lottery_apply_page import LotteryApplyPage
from shared.config.lottery_config import LOTTERY_TARGET, CONFIG
from apps.lottery.pages.lottery_confirm_page import LotteryConfirmPage


def _run_lottery_for_account(page, cred, login_svc) -> bool:
    """
    1アカウント分の抽選フローを実行する。成功 True / 途中失敗 False。
    """
    if not login_svc.login(page, cred):
        print(f"❌ ログイン失敗: {cred.user_id}")
        return False

    list_page = LotteryApplyListPage(page)
    if not list_page.goto_apply_list():
        print(f"❌ 抽選申込み一覧へ行けない: {cred.user_id}")
        return False

    if not list_page.click_apply_for(LOTTERY_TARGET.category_label):
        print(f"❌ 対象種別の申込みボタンが押せない: {cred.user_id}")
        return False

    apply_page = LotteryApplyPage(page)
    if not apply_page.select_park_and_facility(
        park_label=LOTTERY_TARGET.park_label,
        facility_label=LOTTERY_TARGET.facility_label,
        timeout_ms=CONFIG.usedate_timeout_ms,
    ):
        print(f"❌ 公園・施設選択失敗: {cred.user_id}")
        return False

    if not apply_page.select_datetime_cell(
        ymd=LOTTERY_TARGET.ymd,
        time_str=LOTTERY_TARGET.time,
        max_next_week=CONFIG.max_next_week,
        timeout_ms=CONFIG.usedate_timeout_ms,
    ):
        print(f"❌ 日時セル選択失敗: {cred.user_id}")
        return False

    if not apply_page.click_apply():
        print(f"❌ 申込みボタン押下失敗: {cred.user_id}")
        return False

    confirm_page = LotteryConfirmPage(page)
    if not confirm_page.select_apply_slot(LOTTERY_TARGET.apply_slot):
        print(f"❌ 申込み番号の選択に失敗: {cred.user_id}")
        return False

    if not confirm_page.submit():
        print(f"❌ 申込み確定に失敗: {cred.user_id}")
        return False

    print(f"✅ 抽選申込み完了: {cred.user_id}")
    return True


def run(headless: bool = False) -> None:
    """
    抽選申込みの動作確認用デバッグ（複数アカウント対応）
    main.py から呼ばれる前提。
    アカウントは load_credentials_list() で取得し、1件ずつログイン→抽選→ログアウトのループで実行する。
    """
    credentials_list = load_credentials_list()
    if not credentials_list:
        print("❌ 抽選用アカウントが0件です")
        return

    print(f"抽選対象アカウント数: {len(credentials_list)}")

    login_svc = LoginService(RESULT_URL)
    logout_svc = LogoutService()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()

        for idx, cred in enumerate(credentials_list):
            print(f"\n--- アカウント {idx + 1}/{len(credentials_list)}: {cred.user_id} ---")
            ok = _run_lottery_for_account(page, cred, login_svc)
            if not ok:
                # 次のアカウントへ（トップに戻すためログアウト試行）
                logout_svc.logout(page)
                continue

            # 次のアカウントがいる場合はログアウトしてから次へ
            if idx + 1 < len(credentials_list):
                if not logout_svc.logout(page):
                    print(f"⚠ ログアウトに失敗しましたが次のアカウントを試行します: {cred.user_id}")

        print("\n✅ 全アカウントの処理が終わりました")
        input("Enter を押すとブラウザを閉じます")
        browser.close()