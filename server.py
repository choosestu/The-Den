from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

os.makedirs("transcripts", exist_ok=True)

@app.route("/", methods=["POST"])
def receive_fieldy():
    data = request.get_json(force=True)

    date = data.get("date", datetime.now().isoformat())
    safe_date = date.replace(":", "-").replace(".", "-")
    filename = f"transcripts/{safe_date}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Saved transcript:", filename)

    return jsonify({"status": "received", "file": filename})

@app.route("/", methods=["GET"])
def home():
    return "Fieldy webhook receiver is running."

if __name__ == "__main__":
    app.run(port=5000)