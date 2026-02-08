# tennis_watch/apps/lottery/pages/lottery_apply_list_page.py

import re
from typing import Optional

from playwright.sync_api import Page, Locator


class LotteryApplyListPage:
    """
    抽選申込み：対象期間一覧画面

    役割：
    - トップ/任意画面から「抽選申込み」一覧へ遷移
    - 対象（テニス（ハード） or テニス（人工芝））の行を見つけて
      その行の「申込み」ボタンを押して次の画面へ進む
    """

    LIST_AREA_ID = "#lottery-info-list-area"

    def __init__(self, page: Page):
        self.page = page

    # -------------------------
    # 画面内エリア
    # -------------------------
    def _list_area(self) -> Locator:
        return self.page.locator(self.LIST_AREA_ID)

    # -------------------------
    # 遷移
    # -------------------------
    def goto_apply_list(self) -> bool:
        """
        「抽選 ⏷」→「抽選申込み」へ進む。
        すでに一覧にいる場合はそのままでも良い。
        """
        try:
            # 一覧エリアが既に見えるならOK
            if self.page.locator(self.LIST_AREA_ID).count() > 0:
                return True

            # メニューの「抽選 ⏷」を開く（リンク扱いが多い）
            # exactにすると死ぬことがあるので、正規表現で拾う
            self.page.get_by_role("link", name=re.compile(r"抽選")).click()

            # 抽選申込み（完全一致）
            self.page.get_by_role(
                "link",
                name="抽選申込み",
                exact=True
            ).click()

            # 一覧の描画待ち
            self.page.wait_for_selector(self.LIST_AREA_ID, timeout=30000)
            return True
        except Exception as e:
            print("⚠ 抽選申込み一覧へ遷移できない:", e)
            return False

    # -------------------------
    # 対象行の取得
    # -------------------------
    def _find_target_row(self, purpose_label: str) -> Optional[Locator]:
        """
        一覧の中から、指定の種目（テニス（ハード）/テニス（人工芝））が
        “含まれる”行を返す。
        完全一致がいいと言ってたが、行の中には期間文字列も混ざるので
        「行テキストに purpose_label が含まれる」を採用する。
        """
        area = self._list_area()
        rows = area.get_by_role("row")

        for i in range(rows.count()):
            row = rows.nth(i)
            try:
                txt = row.inner_text().strip()
            except Exception:
                continue

            if purpose_label in txt:
                return row

        # role=row で拾えない構造の場合の保険
        try:
            btn = area.locator("button", has_text="申込み").first
            if btn.count() > 0:
                container = btn.locator("xpath=ancestor::*[self::tr or self::div][1]")
                if container.count() > 0:
                    txt = container.first.inner_text()
                    if purpose_label in txt:
                        return container.first
        except Exception:
            pass

        return None

    # -------------------------
    # 申込みボタン押下
    # -------------------------
    def click_apply_for(self, purpose_label: str) -> bool:
        """
        一覧から対象行を探して「申込み」ボタンを押す。
        成功したら True。
        """
        try:
            self.page.wait_for_selector(self.LIST_AREA_ID, timeout=30000)
            row = self._find_target_row(purpose_label)
            if row is None:
                print(f"⚠ 一覧に目的の行が見つからない: {purpose_label}")
                return False

            btn = row.locator("button", has_text="申込み")
            if btn.count() == 0:
                btn = row.locator("button[onclick*='doLotEntry']")
            if btn.count() == 0:
                print("⚠ 対象行に申込みボタンが見つからない")
                return False

            btn.first.click()
            self.page.wait_for_load_state("networkidle")
            return True
        except Exception as e:
            print("⚠ 申込みボタン押下に失敗:", e)
            return False