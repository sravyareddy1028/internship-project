import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def load_env_file(path: Optional[Path] = None) -> None:
    env_path = path or Path(__file__).with_name(".env")
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


class OpenRouterClient:
    def __init__(self):
        load_env_file()
        self.use_openrouter = os.getenv("USE_OPENROUTER", "true").strip().lower()
        self.api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
        self.model = os.getenv("OPENROUTER_MODEL", "openrouter/auto").strip()
        self.site_url = os.getenv("OPENROUTER_SITE_URL", "http://127.0.0.1:8000").strip()
        self.app_name = os.getenv("OPENROUTER_APP_NAME", "Multilingual Internship Chatbot").strip()
        self.timeout = int(os.getenv("OPENROUTER_TIMEOUT", "30"))

    @property
    def enabled(self) -> bool:
        return self.use_openrouter in {"1", "true", "yes", "on"} and self.is_valid_api_key(self.api_key)

    @staticmethod
    def is_valid_api_key(api_key: str) -> bool:
        normalized = api_key.strip().lower()
        if not normalized.startswith("sk-or-"):
            return False
        if len(normalized) < 24:
            return False
        return not any(token in normalized for token in ("your-key", "your-real", "key-here"))

    def configure(self, api_key: str, model: str = "openrouter/auto", persist: bool = True) -> Dict[str, object]:
        self.use_openrouter = "true"
        self.api_key = api_key.strip()
        self.model = (model or "openrouter/auto").strip()

        if persist:
            self._write_env_file()

        return self.status()

    def status(self) -> Dict[str, object]:
        return {
            "enabled": self.enabled,
            "model": self.model,
            "api_key_set": bool(self.api_key),
            "api_key_preview": self._masked_key(),
        }

    def _masked_key(self) -> str:
        if not self.api_key:
            return ""
        if len(self.api_key) <= 12:
            return "********"
        return f"{self.api_key[:7]}...{self.api_key[-4:]}"

    def _write_env_file(self) -> None:
        env_path = Path(__file__).with_name(".env")
        lines = [
            "USE_OPENROUTER=true",
            f"OPENROUTER_API_KEY={self.api_key}",
            f"OPENROUTER_MODEL={self.model}",
            f"OPENROUTER_SITE_URL={self.site_url}",
            f"OPENROUTER_APP_NAME={self.app_name}",
        ]
        env_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def chat(self, messages: List[Dict[str, str]]) -> str:
        if not self.enabled:
            raise RuntimeError("OPENROUTER_API_KEY is not configured")

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.4,
            "max_tokens": 350,
        }
        body = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            OPENROUTER_URL,
            data=body,
            method="POST",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": self.site_url,
                "X-Title": self.app_name,
            },
        )

        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"OpenRouter HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"OpenRouter network error: {exc.reason}") from exc

        try:
            return data["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError(f"Unexpected OpenRouter response: {data}") from exc