# tennis_watch/shared/tool/lottery_apply_debug.py
from playwright.sync_api import sync_playwright

from shared.config.settings import RESULT_URL
from shared.infra.auth.credentials import load_credentials
from shared.infra.auth.login_service import LoginService

from apps.lottery.pages.lottery_apply_list_page import LotteryApplyListPage
from apps.lottery.pages.lottery_apply_page import LotteryApplyPage
from shared.config.lottery_config import LOTTERY_TARGET, CONFIG
from apps.lottery.pages.lottery_confirm_page import LotteryConfirmPage


def run(headless: bool = False) -> None:
    """
    抽選申込みの動作確認用デバッグ
    main.py から呼ばれる前提
    """
    cred = load_credentials()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()

        # ログイン
        login = LoginService(RESULT_URL)
        if not login.login(page, cred):
            print("❌ ログイン失敗")
            browser.close()
            return

        # 抽選申込み一覧
        list_page = LotteryApplyListPage(page)
        if not list_page.goto_apply_list():
            print("❌ 抽選申込み一覧へ行けない")
            browser.close()
            return

        if not list_page.click_apply_for(LOTTERY_TARGET.category_label):
            print("❌ 対象種別の申込みボタンが押せない")
            browser.close()
            return

        # 日時選択画面
        apply_page = LotteryApplyPage(page)

        if not apply_page.select_park_and_facility(
            park_label=LOTTERY_TARGET.park_label,
            facility_label=LOTTERY_TARGET.facility_label,
            timeout_ms=CONFIG.usedate_timeout_ms,
        ):
            print("❌ 公園・施設選択失敗")
            browser.close()
            return

        if not apply_page.select_datetime_cell(
            ymd=LOTTERY_TARGET.ymd,
            time_str=LOTTERY_TARGET.time,
            max_next_week=CONFIG.max_next_week,
            timeout_ms=CONFIG.usedate_timeout_ms,
        ):
            print("❌ 日時セル選択失敗")
            browser.close()
            return

        if not apply_page.click_apply():
            print("❌ 申込みボタン押下失敗")
            browser.close()
            return

        # 確認画面
        confirm_page = LotteryConfirmPage(page)
        if not confirm_page.select_apply_slot(LOTTERY_TARGET.apply_slot):
            print("❌ 申込み番号の選択に失敗")
            browser.close()
            return

        if not confirm_page.submit():
            print("❌ 申込み確定に失敗")
            browser.close()
            return

        print("✅ 抽選申込み画面まで到達（ここで止める）")
        input("Enter を押すとブラウザを閉じます")

        browser.close()