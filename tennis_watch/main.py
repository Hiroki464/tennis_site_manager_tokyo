# main.py
from apps.reserve_watch.flows.checker import check_courts_months
from apps.reserve_watch.flows.watcher import loop_watch

if __name__ == "__main__":
    # 単発テスト（デバッグ用）
    check_courts_months(headless=False)

    # 本番監視（必要ならコメント外す）
    # loop_watch(interval_min=10)