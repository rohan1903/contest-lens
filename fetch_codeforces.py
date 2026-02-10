"""
Fetch all problems from the Codeforces API and store them in SQLite.

Codeforces API docs: https://codeforces.com/apiHelp
Endpoint used: problemset.problems (no auth required)
"""

import json
import sqlite3
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("Installing requests...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests


# ── Config ──────────────────────────────────────────────────────────────────
API_URL = "https://codeforces.com/api/problemset.problems"
DB_PATH = Path(__file__).parent / "data" / "codeforces.db"


# ── Fetch ───────────────────────────────────────────────────────────────────

def fetch_problems() -> dict:
    """Fetch all problems from the Codeforces API."""
    print("Fetching problems from Codeforces API...")
    resp = requests.get(API_URL, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    if data.get("status") != "OK":
        raise RuntimeError(f"API returned status: {data.get('status')} — {data.get('comment', '')}")

    problems = data["result"]["problems"]
    problem_stats = data["result"]["problemStatistics"]

    print(f"  Fetched {len(problems)} problems")
    print(f"  Fetched {len(problem_stats)} problem statistics")

    return problems, problem_stats


# ── Database ────────────────────────────────────────────────────────────────

def init_db(db_path: Path) -> sqlite3.Connection:
    """Create SQLite database and tables."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=WAL")

    conn.executescript("""
        CREATE TABLE IF NOT EXISTS problems (
            contest_id    INTEGER,
            problem_index TEXT,
            name          TEXT,
            rating        INTEGER,
            tags          TEXT,        -- JSON array of tag strings
            solved_count  INTEGER DEFAULT 0,
            PRIMARY KEY (contest_id, problem_index)
        );

        CREATE INDEX IF NOT EXISTS idx_problems_rating ON problems(rating);
        CREATE INDEX IF NOT EXISTS idx_problems_tags   ON problems(tags);
    """)
    conn.commit()
    return conn


def store_problems(conn: sqlite3.Connection, problems: list, stats: list):
    """Insert problems into the database."""
    # Build a lookup for solved counts
    solved_map = {}
    for s in stats:
        key = (s["contestId"], s["index"])
        solved_map[key] = s.get("solvedCount", 0)

    rows = []
    skipped = 0
    for p in problems:
        contest_id = p.get("contestId")
        index = p.get("index")
        if contest_id is None or index is None:
            skipped += 1
            continue

        rating = p.get("rating")  # Can be None if not rated yet
        tags = json.dumps(p.get("tags", []))
        name = p.get("name", "")
        solved = solved_map.get((contest_id, index), 0)

        rows.append((contest_id, index, name, rating, tags, solved))

    conn.executemany("""
        INSERT OR REPLACE INTO problems
            (contest_id, problem_index, name, rating, tags, solved_count)
        VALUES (?, ?, ?, ?, ?, ?)
    """, rows)
    conn.commit()

    print(f"  Stored {len(rows)} problems in database")
    if skipped:
        print(f"  Skipped {skipped} problems (missing contest/index)")


# ── Summary ─────────────────────────────────────────────────────────────────

def print_summary(conn: sqlite3.Connection):
    """Print a quick summary of the database contents."""
    total = conn.execute("SELECT COUNT(*) FROM problems").fetchone()[0]
    rated = conn.execute("SELECT COUNT(*) FROM problems WHERE rating IS NOT NULL").fetchone()[0]
    unrated = total - rated

    print(f"\n{'═' * 60}")
    print(f"  DATABASE SUMMARY")
    print(f"{'═' * 60}")
    print(f"  Total problems:   {total}")
    print(f"  Rated problems:   {rated}")
    print(f"  Unrated problems: {unrated}")

    # Rating distribution
    print(f"\n  Rating Distribution:")
    print(f"  {'Rating Band':<15} {'Count':>8} {'Bar'}")
    print(f"  {'─' * 50}")

    bands = [
        (800, 1000), (1000, 1200), (1200, 1400),
        (1400, 1600), (1600, 1900), (1900, 2100),
        (2100, 2400), (2400, 2800), (2800, 3600),
    ]

    max_count = 0
    band_counts = []
    for lo, hi in bands:
        count = conn.execute(
            "SELECT COUNT(*) FROM problems WHERE rating >= ? AND rating < ?",
            (lo, hi)
        ).fetchone()[0]
        band_counts.append((lo, hi, count))
        max_count = max(max_count, count)

    for lo, hi, count in band_counts:
        bar_len = int(count / max(max_count, 1) * 30)
        bar = "█" * bar_len
        print(f"  {lo:>4}-{hi:<4}       {count:>8}  {bar}")

    # Top tags
    print(f"\n  Top 15 Tags:")
    print(f"  {'Tag':<30} {'Count':>8}")
    print(f"  {'─' * 42}")

    all_tags = conn.execute("SELECT tags FROM problems WHERE rating IS NOT NULL").fetchall()
    tag_counts = {}
    for (tags_json,) in all_tags:
        for tag in json.loads(tags_json):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

    sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
    for tag, count in sorted_tags[:15]:
        print(f"  {tag:<30} {count:>8}")

    print()


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║     CONTEST-LENS · Codeforces Data Fetcher              ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()

    # Fetch from API
    problems, stats = fetch_problems()

    # Store in SQLite
    print(f"\nInitializing database at: {DB_PATH}")
    conn = init_db(DB_PATH)
    store_problems(conn, problems, stats)

    # Print summary
    print_summary(conn)

    conn.close()
    print(f"✅ Done! Database saved to: {DB_PATH}\n")


if __name__ == "__main__":
    main()

