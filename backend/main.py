import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.config import HOST, PORT
from backend.database import fetch_all
from backend.services.mission_controller import controller

FRONTEND = ROOT / "frontend"

class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, content_type="application/json"):
        data = body if isinstance(body, bytes) else body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/":
            return self._file(FRONTEND / "index.html", "text/html")
        if path == "/style.css":
            return self._file(FRONTEND / "style.css", "text/css")
        if path == "/app.js":
            return self._file(FRONTEND / "app.js", "application/javascript")
        if path == "/api/status":
            return self._json({"ok": True, "system": "SUIMS", "mode": "SIMULATION", "version": "1.0.0"})
        if path == "/api/telemetry":
            return self._json(controller.snapshot()["telemetry"])
        if path == "/api/mission":
            return self._json(controller.snapshot()["mission"])
        if path == "/api/assets":
            return self._json([
                {"id":"T01","type":"Tower","status":"NORMAL","risk":22,"distance_m":410},
                {"id":"T02","type":"Tower","status":"MONITOR","risk":48,"distance_m":276},
                {"id":"T04","type":"Insulator Bank","status":"HIGH RISK","risk":controller.snapshot()["risk"]["score"],"distance_m":142},
                {"id":"T05","type":"Tower","status":"PENDING","risk":31,"distance_m":620}
            ])
        if path == "/api/decisions":
            return self._json(fetch_all("SELECT * FROM decisions ORDER BY id DESC LIMIT 20"))
        if path == "/api/events":
            return self._json(fetch_all("SELECT * FROM events ORDER BY id DESC LIMIT 30"))
        if path == "/api/detections":
            return self._json(fetch_all("SELECT * FROM detections ORDER BY id DESC LIMIT 20"))
        if path == "/api/history":
            return self._json(fetch_all("SELECT * FROM missions ORDER BY id DESC LIMIT 20"))
        if path == "/api/snapshot":
            return self._json(controller.tick())
        self._send(404, "Not found", "text/plain")

    def do_POST(self):
        path = urlparse(self.path).path
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b"{}"
        try:
            body = json.loads(raw.decode("utf-8"))
        except Exception:
            body = {}
        if path == "/api/mission/start":
            return self._json(controller.start())
        if path == "/api/mission/stop":
            return self._json(controller.stop())
        if path == "/api/simulate":
            return self._json(controller.tick())
        if path == "/api/failures":
            return self._json(controller.set_failures(**body))
        if path == "/api/reset":
            controller.failures = {k: False for k in controller.failures}
            controller.mission.reset()
            return self._json(controller.snapshot())
        self._send(404, "Not found", "text/plain")

    def _json(self, obj):
        return self._send(200, json.dumps(obj, default=str), "application/json")

    def _file(self, path, content_type):
        if not path.exists():
            return self._send(404, "Missing file", "text/plain")
        return self._send(200, path.read_bytes(), content_type)

if __name__ == "__main__":
    print(f"SUIMS Mission Control running at http://localhost:{PORT}")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
