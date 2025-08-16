import json
import re
from typing import Dict, Any, Union

def extract_telegram_fields(body: Union[bytes, tuple]) -> Dict[str, Any]:
    """
    Extract the 5 desired fields from a Telegram webhook payload.

    body can be:
      - Django   -> request.body (bytes)
      - Else     -> (b'...',)    (tuple with one bytes element)
    """
    # 1. Normalize to bytes
    if isinstance(body, tuple):
        if not body:
            raise ValueError("Empty tuple body")
        payload_bytes = body[0]
    else:
        payload_bytes = body

    if not isinstance(payload_bytes, bytes):
        raise ValueError("Body is not bytes")

    # 2. Decode + parse
    try:
        update = json.loads(payload_bytes.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError("Invalid JSON or encoding") from exc

    # 3. Basic guardrails
    if "message" not in update or "reply_to_message" not in update["message"]:
        raise ValueError("Payload is not a reply to a bot message")

    # 4. Extract
    reply_text        = update["message"]["text"]
    telegram_user_id  = update["message"]["from"]["id"]
    bot_msg_text      = update["message"]["reply_to_message"]["text"]

    def _re(pattern: str, txt: str, label: str) -> str:
        m = re.search(pattern, txt, re.IGNORECASE)
        if not m:
            raise ValueError(f"Cannot find {label} in bot message")
        return m.group(1).strip()

    session_id = _re(r"Session ID:\s*([a-f0-9\-]{36})", bot_msg_text, "session_id")
    user       = _re(r"User:\s*([^\s(]+)",                   bot_msg_text, "user")
    email      = _re(r"\b([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})\b",
                     bot_msg_text, "email")

    return {
        "session_id":       session_id,
        "content":          reply_text,
        "telegram_user_id": telegram_user_id,
        "user":             user,
        "email":            email,
    }