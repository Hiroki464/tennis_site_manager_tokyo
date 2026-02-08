# tennis_watch/apps/lottery/pages/lottery_apply_page.py

import re
from typing import Optional

from playwright.sync_api import Page, Locator


class LotteryApplyPage:
    """
    抽選の「日時選択」画面。
    - 公園(#bname) と 施設(#iname) を選ぶと、日時テーブル(#usedate-table)が Ajax で出る
    - 翌週(#next-week)を押すと週が進む（最終週で disabled）
    """

    def __init__(self, page: Page):
        self.page = page

    # -------------------------
    # 基本セレクタ
    # -------------------------
    def _park_select(self) -> Locator:
        return self.page.locator("#bname")

    def _facility_select(self) -> Locator:
        return self.page.locator("#iname")

    def _usedate_table(self) -> Locator:
        return self.page.locator("#usedate-table")

    def _next_week_button(self) -> Locator:
        return self.page.locator("#next-week")

    def _apply_button(self) -> Locator:
        return self.page.get_by_role("button", name=re.compile(r".*申込み.*"))

    # -------------------------
    # 便利関数
    # -------------------------
    @staticmethod
    def _normalize_time_text(s: str) -> str:
        """
        画面の「７：００」みたいな全角を「7:00」に寄せる。
        """
        if s is None:
            return ""

        trans = str.maketrans("０１２３４５６７８９：", "0123456789:")
        s = s.translate(trans)
        s = re.sub(r"\s+", "", s)
        return s

    def _wait_iname_has_label(self, facility_label: str, timeout_ms: int) -> None:
        """
        公園選択後、#iname が Ajax で更新される。
        facility_label が option に出現するまで待つ（最大timeout_ms）
        """
        self.page.wait_for_selector("#iname", timeout=30000)
        self.page.wait_for_function(
            """(label) => {
                const el = document.querySelector("#iname");
                if (!el) return false;
                if (el.disabled) return false;
                const opts = Array.from(el.options || []);
                if (opts.length <= 1) return false; // 「選択してください。」だけの状態を除外
                return opts.some(o => (o.textContent || "").trim() === label);
            }""",
            arg=facility_label,
            timeout=timeout_ms,
        )

    def _wait_usedate_table_loaded(self, timeout_ms: int) -> None:
        self.page.wait_for_selector("#usedate-loaded", timeout=timeout_ms)
        self.page.wait_for_selector("#usedate-table", timeout=timeout_ms)

    # -------------------------
    # 公園/施設選択
    # -------------------------
    def select_park_and_facility(self, park_label: str, facility_label: str, timeout_ms: int) -> bool:
        """
        公園：labelで選択（valueは変わるので使わない）
        施設：labelで選択
        """
        try:
            self.page.wait_for_selector("#bname", timeout=30000)
            self._park_select().select_option(label=park_label)

            # 施設の選択肢が更新され、目的のlabelが出るまで待つ
            self._wait_iname_has_label(facility_label, timeout_ms=timeout_ms)
            # TODO: waitを置かないと施設選択がクリアされてしまう現象がある
            self.page.wait_for_timeout(1000)  # 1秒

            # 施設選択
            self._facility_select().select_option(label=facility_label)

            # 日時テーブルが出るまで待つ
            self._wait_usedate_table_loaded(timeout_ms=timeout_ms)
            return True
        except Exception as e:
            print("⚠ 公園/施設の選択に失敗:", e)
            return False

    # -------------------------
    # 日付列・時間行の特定
    # -------------------------
    def _get_date_col_index(self, ymd: str) -> Optional[int]:
        """
        thead の th 内の
        <input name="selectUseYMD" value="YYYYMMDD">
        で列番号を特定する。
        戻り値は0始まりで、0は「時間帯」列(th)。
        """
        table = self._usedate_table()
        headers = table.locator("thead tr").first.locator("th")

        for i in range(headers.count()):
            th = headers.nth(i)
            inp = th.locator('input[name="selectUseYMD"]')
            if inp.count() == 0:
                continue
            v = (inp.first.get_attribute("value") or "").strip()
            if v == ymd:
                return i
        return None

    def _get_time_row(self, time_str: str) -> Optional[Locator]:
        """
        tbody の各行は
        <tr ...>
          <th>７：００</th> ...
        なので、左端thの表示で行を特定。
        """
        target = self._normalize_time_text(time_str)
        table = self._usedate_table()
        rows = table.locator("tbody tr")

        for i in range(rows.count()):
            row = rows.nth(i)
            th = row.locator("th").first
            txt = self._normalize_time_text(th.inner_text().strip())
            if txt == target:
                return row
        return None

    def _is_next_week_enabled(self) -> bool:
        btn = self._next_week_button()
        if btn.count() == 0:
            return False
        return btn.get_attribute("disabled") is None

    # -------------------------
    # セル選択＆申込み
    # -------------------------
    def select_datetime_cell(self, ymd: str, time_str: str, max_next_week: int, timeout_ms: int) -> bool:
        """
        (ymd, time) が今の週に無ければ「翌週」を押して探す。
        見つかったらセルをクリック。
        """
        for attempt in range(max_next_week + 1):
            try:
                self._wait_usedate_table_loaded(timeout_ms=timeout_ms)
            except Exception:
                pass

            col_idx = self._get_date_col_index(ymd)
            row = self._get_time_row(time_str)

            if col_idx is not None and row is not None:
                # row.locator("td") は「時間帯thを除いたtd」なので col_idx-1
                td_idx = col_idx - 1
                if td_idx < 0:
                    print("⚠ 列番号が不正（ヘッダ列のズレ）:", col_idx)
                    return False

                tds = row.locator("td")
                if td_idx >= tds.count():
                    print("⚠ td数が足りない。想定外のテーブル構造。")
                    return False

                cell = tds.nth(td_idx)

                cls = (cell.get_attribute("class") or "")
                if "col-maintenance" in cls:
                    print("⚠ メンテナンス枠っぽいので選択不可:", ymd, time_str)
                    return False

                cell.click()
                return True

            # 見つからない → 翌週
            if attempt >= max_next_week:
                break

            if not self._is_next_week_enabled():
                print("⚠ 翌週ボタンが非活性。これ以上進めない。")
                break

            # 翌週ボタン押下
            self._next_week_button().click()
            # TODO: waitを置かないと翌週ボタンが2回以上押されてしまう現象がある
            self.page.wait_for_timeout(1000)  # 1秒
            self.page.wait_for_load_state("networkidle")

        print("⚠ 指定の日時が見つからなかった:", ymd, time_str)
        return False

    def click_apply(self) -> bool:
        try:
            self._apply_button().first.click()
            self.page.wait_for_load_state("networkidle")
            return True
        except Exception as e:
            print("⚠ 申込みボタン押下に失敗:", e)
            return False
