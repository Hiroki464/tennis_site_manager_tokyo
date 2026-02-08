# tennis_watch/main.py

# ===== 実行モード切替 =====
# "check"               : 予約監視 単発テスト
# "watch"               : 予約監視 常駐
# "login_debug"         : ログイン動作確認
# "lottery_apply_debug" : 抽選申込みデバッグ
MODE = "lottery_apply_debug"

# watch 時の設定
WATCH_INTERVAL_MIN = 10
# =========================

from apps.reserve_watch.flows.checker import check_courts_months
from apps.reserve_watch.flows.watcher import loop_watch

#from shared.tool.login_debug import run as login_debug_run
from shared.tool.lottery_apply_debug import run as lottery_apply_debug_run


def main() -> None:
    print(f"=== MODE: {MODE} ===")

    if MODE == "check":
        check_courts_months(headless=False)
        return

    if MODE == "watch":
        loop_watch(interval_min=WATCH_INTERVAL_MIN)
        return

    # if MODE == "login_debug":
    #     login_debug_run(headless=False)
    #     return

    if MODE == "lottery_apply_debug":
        lottery_apply_debug_run(headless=False)
        return

    raise RuntimeError(f"未知の MODE が指定されている: {MODE}")


if __name__ == "__main__":
    main()