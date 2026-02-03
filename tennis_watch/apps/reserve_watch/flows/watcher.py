# apps/reserve_watch/flows/watcher.py
import time
from shared.config import settings
from shared.notify.line_notify import send_line_message
from apps.reserve_watch.flows.checker import check_courts_months


def loop_watch(interval_min: int | None = None):
    if interval_min is None:
        interval_min = settings.INTERVAL_MIN

    loop_count = 0
    error_streak = 0

    while True:
        loop_count += 1
        print(f"\n===== 監視開始（{loop_count}回目）=====")

        try:
            result = check_courts_months(headless=True)

            if result == "SITE_ERROR":
                error_streak += 1
                print(f"⚠ サイト障害っぽい（連続 {error_streak} 回）")

            elif result == "NO_VACANCY":
                print("空きなし")
                error_streak = 0

            elif result == "NO_CHANGE":
                print("前回と同じ結果 → 通知スキップ")
                error_streak = 0

            elif result == "SENT":
                print("空きあり → LINE送信済み")
                error_streak = 0

            else:
                print(f"想定外の戻り値: {result}")
                error_streak += 1

        except Exception as e:
            print(f"予期せぬエラー: {e}")
            error_streak += 1

        if error_streak >= settings.ERROR_LIMIT:
            alert = (
                "【テニス予約監視：障害検知】\n"
                f"サイト接続が {settings.ERROR_LIMIT} 回連続で失敗しています。\n"
                "システム障害 or ブロックの可能性があります。"
            )
            send_line_message(alert)
            print("⚠ 障害が規定回数に達した → LINE通知 → カウンターリセット")
            error_streak = 0

        print(f"{interval_min}分待機（次は {loop_count+1}回目）…")
        time.sleep(interval_min * 60)