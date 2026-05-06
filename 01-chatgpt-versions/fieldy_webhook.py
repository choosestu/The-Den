"""
Fieldy Webhook Receiver for The Den
------------------------------------
Runs on localhost:9090
- Receives transcript pushes from Fieldy every 30s via ngrok
- Serves latest transcript to The Den via GET /transcript
- Accumulates the day's full transcript in memory and on disk

Setup:
  1. python fieldy_webhook.py
  2. ngrok http 9090  (in a second terminal)
  3. Copy the ngrok https:// URL into Fieldy > Settings > Developer > Webhook Endpoint URL
  4. The Den polls http://localhost:9090/transcript automatically
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time
import os
import datetime

# ── State ───────────────────────────────────────────────────────────────────
latest = {
    "text": "",
    "timestamp": 0,
    "date": "",
    "session_count": 0
}
today_full_transcript = []   # All chunks for today, in order
DATA_FILE = os.path.join(os.path.dirname(__file__), "fieldy_today.json")
DEN_DATA_FILE = os.path.join(os.path.dirname(__file__), "den_data.json")

def save_to_disk():
    """Write today's accumulated transcript to disk so The Den can load it on restart."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "date": latest["date"],
                "text": latest["text"],
                "timestamp": latest["timestamp"],
                "session_count": latest["session_count"],
                "chunks": today_full_transcript
            }, f, indent=2)
    except Exception as e:
        print(f"[warn] Could not write to disk: {e}")

def load_from_disk():
    """Restore today's transcript if the server was restarted mid-day."""
    global today_full_transcript
    today = datetime.date.today().isoformat()
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if data.get("date") == today:
                latest.update({
                    "text": data.get("text", ""),
                    "timestamp": data.get("timestamp", 0),
                    "date": today,
                    "session_count": data.get("session_count", 0)
                })
                today_full_transcript = data.get("chunks", [])
                print(f"[info] Restored {len(today_full_transcript)} chunks from disk for {today}")
    except Exception as e:
        print(f"[warn] Could not load from disk: {e}")

# ── Request Handler ──────────────────────────────────────────────────────────
class FieldyHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        # Quieter logging
        if "POST" in str(args) or "200" not in str(args):
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {format % args}")

    def send_cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors()
        self.end_headers()

    def do_POST(self):
        """Handle POST requests."""
        if self.path == "/data":
            # Save Den task data to disk
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length) if content_length else b""
            try:
                json.loads(body)  # validate JSON
                with open(DEN_DATA_FILE, "w", encoding="utf-8") as f:
                    f.write(body.decode("utf-8"))
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_cors()
                self.end_headers()
                self.wfile.write(json.dumps({"ok": True}).encode())
                print(f"[data] Den state saved to disk ({len(body)} bytes)")
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"ok": False, "error": str(e)}).encode())
            return
        """Receive a transcript chunk from Fieldy."""
        global today_full_transcript
        today = datetime.date.today().isoformat()

        # Reset if it's a new day
        if latest["date"] != today:
            today_full_transcript = []
            latest["session_count"] = 0
            latest["date"] = today
            print(f"[info] New day detected, resetting transcript buffer for {today}")

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length else b""

        text = ""
        try:
            data = json.loads(body)
            # Try common field names Fieldy might use
            text = (data.get("text") or data.get("transcript") or
                    data.get("content") or data.get("transcription") or "")
            if not text and isinstance(data, str):
                text = data
        except Exception:
            text = body.decode("utf-8", errors="replace")

        text = text.strip()

        if text:
            latest["text"] = text
            latest["timestamp"] = time.time()
            latest["session_count"] += 1

            # Only add if this chunk has new content (Fieldy sends cumulative text)
            if not today_full_transcript or today_full_transcript[-1] != text:
                today_full_transcript.append(text)
                save_to_disk()
                print(f"[push] Chunk #{latest['session_count']} received ({len(text)} chars)")
        else:
            print(f"[warn] Empty payload received")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_cors()
        self.end_headers()
        self.wfile.write(json.dumps({"ok": True}).encode())

    def do_GET(self):
        """Serve latest transcript data to The Den."""
        if self.path == "/transcript" or self.path == "/":
            response = {
                "text": latest["text"],
                "timestamp": latest["timestamp"],
                "date": latest["date"],
                "session_count": latest["session_count"],
                # Also provide the full day's accumulated text for Veritas processing
                "full_text": "\n\n---\n\n".join(today_full_transcript)
            }
            body = json.dumps(response).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.send_cors()
            self.end_headers()
            self.wfile.write(body)

        elif self.path == "/clear":
            # Clear today's transcript (GET /clear for easy manual reset)
            global today_full_transcript
            today_full_transcript = []
            latest.update({"text": "", "timestamp": 0, "session_count": 0})
            save_to_disk()
            self.send_response(200)
            self.send_cors()
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True, "message": "Cleared"}).encode())

        elif self.path == "/data":
            # Serve saved Den task data
            try:
                if os.path.exists(DEN_DATA_FILE):
                    with open(DEN_DATA_FILE, "r", encoding="utf-8") as f:
                        body = f.read().encode()
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Content-Length", str(len(body)))
                    self.send_cors()
                    self.end_headers()
                    self.wfile.write(body)
                else:
                    self.send_response(404)
                    self.send_cors()
                    self.end_headers()
                    self.wfile.write(json.dumps({"ok": False}).encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()

        elif self.path == "/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_cors()
            self.end_headers()
            self.wfile.write(json.dumps({
                "running": True,
                "date": latest["date"],
                "chunks_today": len(today_full_transcript),
                "last_update": latest["timestamp"]
            }).encode())
        else:
            self.send_response(404)
            self.end_headers()

# ── Main ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    load_from_disk()
    server = HTTPServer(("localhost", 9090), FieldyHandler)
    print("=" * 50)
    print("  Fieldy Webhook Receiver")
    print("  Listening on http://localhost:9090")
    print("  GET  /transcript  — latest + full day text")
    print("  GET  /status      — health check")
    print("  GET  /clear       — reset today's buffer")
    print("  POST /            — Fieldy webhook target")
    print("=" * 50)
    print("\n  Next step: run  ngrok http 9090")
    print("  Then paste the ngrok URL into Fieldy > Settings > Developer\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
