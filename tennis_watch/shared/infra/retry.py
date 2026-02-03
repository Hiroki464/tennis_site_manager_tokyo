# shared/infra/retry.py
import time


def wait_seconds(sec: int):
    time.sleep(sec)