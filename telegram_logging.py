import json
import logging
import os
import queue
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Optional


_TELEGRAM_TEXT_LIMIT = 4096
_DEFAULT_CHUNK_SIZE = 3800


def _parse_log_level(value: str, default: int = logging.ERROR) -> int:
    if not value:
        return default
    value = str(value).strip().upper()
    if value.isdigit():
        try:
            return int(value)
        except Exception:
            return default
    return getattr(logging, value, default)


def _chunk_text(text: str, chunk_size: int = _DEFAULT_CHUNK_SIZE):
    if not text:
        return []
    size = int(chunk_size) if int(chunk_size) > 0 else _DEFAULT_CHUNK_SIZE
    size = min(size, _TELEGRAM_TEXT_LIMIT)
    if len(text) <= size:
        return [text]
    return [text[i : i + size] for i in range(0, len(text), size)]


class TelegramLogHandler(logging.Handler):
    """
    Non-blocking logging handler that sends logs to Telegram via bot API.

    Env usage is wired via `setup_telegram_logging()` in server.py.
    """

    def __init__(
        self,
        bot_token: str,
        chat_id: str,
        *,
        timeout_s: float = 5.0,
        max_queue: int = 200,
        min_interval_s: float = 1.0,
        prefix: str = "",
        chunk_size: int = _DEFAULT_CHUNK_SIZE,
    ):
        super().__init__()
        self._bot_token = (bot_token or "").strip()
        self._chat_id = str(chat_id or "").strip()
        self._timeout_s = float(timeout_s)
        self._min_interval_s = float(min_interval_s)
        self._prefix = (prefix or "").strip()
        self._chunk_size = int(chunk_size)

        self._queue: queue.Queue[str] = queue.Queue(maxsize=int(max_queue))
        self._stop_event = threading.Event()
        self._last_send_at = 0.0

        self._worker = threading.Thread(target=self._worker_loop, name="tg-log-worker", daemon=True)
        self._worker.start()

    def emit(self, record: logging.LogRecord) -> None:
        try:
            text = self.format(record)
            if self._prefix:
                text = f"{self._prefix}\n{text}"

            for chunk in _chunk_text(text, self._chunk_size):
                try:
                    self._queue.put_nowait(chunk)
                except queue.Full:
                    break
        except Exception:
            # Never break the server because of Telegram logging.
            return

    def close(self) -> None:
        try:
            self._stop_event.set()
            try:
                self._worker.join(timeout=1.0)
            except Exception:
                pass
        finally:
            super().close()

    def _rate_limit(self) -> None:
        if self._min_interval_s <= 0:
            return
        now = time.monotonic()
        sleep_s = self._min_interval_s - (now - self._last_send_at)
        if sleep_s > 0:
            time.sleep(sleep_s)
        self._last_send_at = time.monotonic()

    def _worker_loop(self) -> None:
        while not self._stop_event.is_set():
            try:
                text = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue
            try:
                self._rate_limit()
                self._send_message(text)
            except Exception:
                # Avoid recursive logging; just drop on errors.
                pass
            finally:
                try:
                    self._queue.task_done()
                except Exception:
                    pass

    def _send_message(self, text: str) -> None:
        if not self._bot_token or not self._chat_id:
            return

        url = f"https://api.telegram.org/bot{self._bot_token}/sendMessage"
        payload = {
            "chat_id": self._chat_id,
            "text": text or "",
            "disable_web_page_preview": "true",
        }
        data = urllib.parse.urlencode(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=self._timeout_s) as resp:
                resp.read()
        except urllib.error.HTTPError as e:
            # Handle rate limiting (HTTP 429) with optional retry_after.
            if e.code == 429:
                retry_after = None
                try:
                    body = e.read()  # bytes
                    parsed = json.loads(body.decode("utf-8", errors="ignore"))
                    retry_after = (parsed.get("parameters") or {}).get("retry_after")
                except Exception:
                    retry_after = None

                if retry_after:
                    try:
                        time.sleep(float(retry_after))
                        with urllib.request.urlopen(req, timeout=self._timeout_s) as resp:
                            resp.read()
                    except Exception:
                        pass
            # Drop on other HTTP errors.
        except urllib.error.URLError:
            # Network/DNS failure. Drop silently.
            return


def setup_telegram_logging(logger: Optional[logging.Logger] = None) -> Optional[TelegramLogHandler]:
    """
    Attach TelegramLogHandler to the root logger if env vars are present.

    Required:
    - TELEGRAM_BOT_TOKEN
    - TELEGRAM_CHAT_ID

    Optional:
    - TELEGRAM_LOG_LEVEL (default: ERROR)
    - TELEGRAM_LOG_TIMEOUT_S (default: 5)
    - TELEGRAM_LOG_MAX_QUEUE (default: 200)
    - TELEGRAM_LOG_MIN_INTERVAL_S (default: 1.0)
    - TELEGRAM_LOG_PREFIX (default: "[V2Server]")
    """

    token = (os.environ.get("TELEGRAM_BOT_TOKEN") or "").strip()
    chat_id = (os.environ.get("TELEGRAM_CHAT_ID") or "").strip()
    if not token or not chat_id:
        return None

    root = logging.getLogger()
    for h in root.handlers:
        if isinstance(h, TelegramLogHandler):
            return h

    level = _parse_log_level(os.environ.get("TELEGRAM_LOG_LEVEL") or "ERROR", default=logging.ERROR)
    timeout_s = float(os.environ.get("TELEGRAM_LOG_TIMEOUT_S") or "5")
    max_queue = int(os.environ.get("TELEGRAM_LOG_MAX_QUEUE") or "200")
    min_interval_s = float(os.environ.get("TELEGRAM_LOG_MIN_INTERVAL_S") or "1.0")
    prefix = (os.environ.get("TELEGRAM_LOG_PREFIX") or "[V2Server]").strip()

    handler = TelegramLogHandler(
        token,
        chat_id,
        timeout_s=timeout_s,
        max_queue=max_queue,
        min_interval_s=min_interval_s,
        prefix=prefix,
    )
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s", datefmt="%H:%M:%S"))
    root.addHandler(handler)

    if logger:
        logger.info("✓ Telegram logging enabled")
    return handler

