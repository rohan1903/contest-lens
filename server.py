"""
Contest-Lens Flask API server.
Serves static frontend files and exposes analysis data via REST endpoints.
"""

import json
from pathlib import Path

from flask import Flask, jsonify, send_from_directory

app = Flask(__name__, static_folder="static", static_url_path="")

DATA_DIR = Path(__file__).parent / "data"
SAMPLE_PATH = Path(__file__).parent / "sample_output.json"


# ── Static file serving ─────────────────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


# ── API endpoints ────────────────────────────────────────────────────────────

@app.route("/api/analysis")
def get_analysis():
    """Return real analysis data from data/real_analysis.json."""
    path = DATA_DIR / "real_analysis.json"
    if not path.exists():
        return jsonify({"error": "real_analysis.json not found. Run analyze.py first."}), 404
    with open(path) as f:
        data = json.load(f)
    return jsonify(data)


@app.route("/api/sample")
def get_sample():
    """Return sample/demo data from sample_output.json."""
    if not SAMPLE_PATH.exists():
        return jsonify({"error": "sample_output.json not found."}), 404
    with open(SAMPLE_PATH) as f:
        data = json.load(f)
    return jsonify(data)


# ── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n  Contest-Lens server starting...")
    print("  http://localhost:5000\n")
    app.run(debug=False, port=5000)

