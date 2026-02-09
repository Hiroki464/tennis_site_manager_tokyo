import json
import os
from pathlib import Path
from dataclasses import dataclass
from dotenv import load_dotenv

@dataclass(frozen=True)
class Credentials:
    user_id: str
    password: str

def load_credentials() -> Credentials:
    # 呼ばれた時に読む（import時読み込みは事故りやすい）
    load_dotenv()

    user_id = os.getenv("TOKYO_TENNIS_USER_ID", "").strip()
    password = os.getenv("TOKYO_TENNIS_PASSWORD", "").strip()

    if not user_id or not password:
        raise RuntimeError(
            "環境変数 TOKYO_TENNIS_USER_ID / TOKYO_TENNIS_PASSWORD が未設定。"
            " .env を確認しろ。"
        )

    return Credentials(user_id=user_id, password=password)


def load_credentials_list() -> list[Credentials]:
    """
    抽選用に複数アカウントを読み込む。優先順位は次のとおり。

    1. LOTTERY_ACCOUNTS_JSON が設定されていれば、そのパスの JSON から読み込む。
       JSON 形式: [ {"user_id": "...", "password": "..."}, ... ]
    2. TOKYO_TENNIS_USER_ID_1 / TOKYO_TENNIS_PASSWORD_1, _2, _3, ... があれば
       .env の番号付きで複数アカウントとして読み込む。
    3. 上記がなければ従来どおり TOKYO_TENNIS_USER_ID / PASSWORD の1件のみを返す。
    """
    load_dotenv()

    path_str = os.getenv("LOTTERY_ACCOUNTS_JSON", "").strip()
    if path_str:
        path = Path(path_str)
        if path.is_file():
            with open(path, "r", encoding="utf-8") as f:
                raw = json.load(f)
            if isinstance(raw, list) and len(raw) > 0:
                result: list[Credentials] = []
                for i, item in enumerate(raw):
                    if not isinstance(item, dict):
                        raise RuntimeError(
                            f"LOTTERY_ACCOUNTS_JSON の {i} 件目はオブジェクトである必要があります。"
                        )
                    uid = (item.get("user_id") or item.get("userId") or "").strip()
                    pw = (item.get("password") or "").strip()
                    if not uid or not pw:
                        raise RuntimeError(
                            f"LOTTERY_ACCOUNTS_JSON の {i} 件目に user_id と password が必要です。"
                        )
                    result.append(Credentials(user_id=uid, password=pw))
                return result
        # ファイルが無いなどでここに来た場合は .env にフォールバック

    # .env の番号付きで複数アカウント（USER_ID_1, PASSWORD_1, _2, _3, ...）
    env_accounts: list[Credentials] = []
    n = 1
    while True:
        uid = os.getenv(f"TOKYO_TENNIS_USER_ID_{n}", "").strip()
        pw = os.getenv(f"TOKYO_TENNIS_PASSWORD_{n}", "").strip()
        if not uid or not pw:
            break
        env_accounts.append(Credentials(user_id=uid, password=pw))
        n += 1
    if env_accounts:
        return env_accounts

    return [load_credentials()]