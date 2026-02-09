import re
from playwright.sync_api import Page, Locator


class LotteryConfirmPage:
    """
    抽選申込み確認画面
    - 申込み番号(#apply) を選択
    - 申込み(#btn-go) 押下 → confirmダイアログOK
    """

    APPLY_SELECT = "#apply"
    APPLY_BUTTON = "#btn-go"

    def __init__(self, page: Page):
        self.page = page

    def _apply_select(self) -> Locator:
        return self.page.locator(self.APPLY_SELECT)

    def _apply_button(self) -> Locator:
        return self.page.locator(self.APPLY_BUTTON)

    @staticmethod
    def _slot_to_value(slot: int) -> str:
        # bodyにあった option に合わせて確定
        if slot == 1:
            return "1-1"
        if slot == 2:
            return "2-1"
        raise ValueError("apply_slot は 1 か 2 だけ")

    def select_apply_slot(self, slot: int, timeout_ms: int = 30000) -> bool:
        try:
            self.page.wait_for_selector(self.APPLY_SELECT, timeout=timeout_ms)

            value = self._slot_to_value(slot)
            self._apply_select().select_option(value=value)

            # 反映待ち（念のため）
            self.page.wait_for_timeout(200)
            return True
        except Exception as e:
            print("⚠ 申込み番号の選択に失敗:", e)
            return False

    def submit(self, timeout_ms: int = 30000) -> bool:
        try:
            self.page.wait_for_selector(self.APPLY_BUTTON, timeout=timeout_ms)

            # confirmは必ず出る前提でOK
            self.page.once("dialog", lambda d: d.accept())

            self._apply_button().click()

            self.page.wait_for_timeout(3000)  # TODO セッション切れを起こして登録できない事があるため、暫定対応でwaitを使用
            self.page.wait_for_load_state("networkidle")
            return True
        except Exception as e:
            print("⚠ 申込み確定に失敗:", e)
            return False