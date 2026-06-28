from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
import json
import re
import uuid

from chatbot_engine import MultilingualChatbot


ROOT = Path(__file__).parent
STATIC_DIR = ROOT / "static"
bot = MultilingualChatbot()


class ChatHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/":
            return self._send_file(STATIC_DIR / "index.html", "text/html; charset=utf-8")
        if path == "/style.css":
            return self._send_file(STATIC_DIR / "style.css", "text/css; charset=utf-8")
        if path == "/app.js":
            return self._send_file(STATIC_DIR / "app.js", "application/javascript; charset=utf-8")
        if path == "/health":
            return self._send_json({"status": "ok"})
        if path == "/config":
            return self._send_json({"openrouter": bot.openrouter.status()})

        self._send_json({"error": "Not found"}, status=404)

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/config/openrouter":
            return self._handle_openrouter_config()
        if parsed.path == "/chat":
            return self._handle_chat()

        return self._send_json({"error": "Not found"}, status=404)

    def _handle_chat(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            message = str(payload.get("message", "")).strip()
            session_id = str(payload.get("session_id") or uuid.uuid4())
        except (ValueError, json.JSONDecodeError):
            return self._send_json({"error": "Invalid JSON"}, status=400)

        if not message:
            return self._send_json({"error": "Message is required"}, status=400)

        result = bot.reply(message, session_id=session_id)
        result["session_id"] = session_id
        self._send_json(result)

    def _handle_openrouter_config(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            api_key = str(payload.get("api_key", "")).strip()
            model = str(payload.get("model", "openrouter/auto")).strip()
        except (ValueError, json.JSONDecodeError):
            return self._send_json({"error": "Invalid JSON"}, status=400)

        if not bot.openrouter.is_valid_api_key(api_key):
            return self._send_json(
                {"error": "Please enter a valid OpenRouter key. It should start with sk-or- and must not be the example placeholder."},
                status=400,
            )

        status = bot.openrouter.configure(api_key=api_key, model=model, persist=True)
        self._send_json({"message": "OpenRouter API key saved.", "openrouter": status})

    def log_message(self, fmt, *args):
        clean = re.sub(r"\s+", " ", fmt % args)
        print(f"{self.client_address[0]} - {clean}")

    def _send_file(self, path, content_type):
        if not path.exists():
            return self._send_json({"error": "File not found"}, status=404)
        body = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 8000), ChatHandler)
    print("Multilingual chatbot running at http://127.0.0.1:8000")
    print("Press Ctrl+C to stop.")
    server.serve_forever()


if __name__ == "__main__":
    main()