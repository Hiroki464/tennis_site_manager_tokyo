import os
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