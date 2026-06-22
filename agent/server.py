# -*- coding: utf-8 -*-
"""Tenky JSON API nad agentem (jen stdlib, zadne zavislosti).

Spusteni:   python3 agent/server.py        (port 8000, lze PORT=xxxx)
Endpointy:
    GET /health              -> {"ok": true}
    GET /cases               -> [{id, nazev, predmet}, ...]
    GET /analyze?id=FIRMA-0002 -> plny rozbor (viz agent/README.md)

CORS *: aby UI v prohlizeci (jiny origin) mohlo volat.
"""
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
from engine import analyze, list_cases


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        if u.path == "/health":
            return self._send(200, {"ok": True})
        if u.path == "/cases":
            return self._send(200, list_cases())
        if u.path == "/analyze":
            fid = (q.get("id") or [None])[0]
            if not fid:
                return self._send(400, {"error": "chybi parametr id"})
            return self._send(200, analyze(fid))
        self._send(404, {"error": "neznamy endpoint"})

    def log_message(self, *a):
        pass  # ticho


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print(f"Spolecnik agent API -> http://localhost:{port}")
    print("  /cases   /analyze?id=FIRMA-0002   /health")
    HTTPServer(("127.0.0.1", port), Handler).serve_forever()
