from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRANSCRIPTS_DIR = os.path.join(BASE_DIR, "transcripts")
os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)

@app.route("/", methods=["POST"])
def receive_fieldy():
    data = request.get_json(force=True)

    if not data:
        return jsonify({"status": "error", "message": "empty payload"}), 400

    date = data.get("date", datetime.now().isoformat())
    safe_date = date.replace(":", "-").replace(".", "-")
    filename = os.path.join(TRANSCRIPTS_DIR, f"{safe_date}.json")

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Saved transcript:", filename)

    return jsonify({"status": "received", "file": filename})

@app.route("/", methods=["GET"])
def home():
    return "Fieldy webhook receiver is running."

if __name__ == "__main__":
    app.run(port=5000)
