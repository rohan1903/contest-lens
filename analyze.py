"""
Analyze Codeforces problem data from the SQLite database.
Computes real technique frequencies per rating band and generates
the same output structure as the test demo — but with actual data.
"""

import json
import sqlite3
from collections import defaultdict
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "codeforces.db"

# ── Rating bands ────────────────────────────────────────────────────────────
RATING_BANDS = [
    (800,  1000, "Newbie → Pupil"),
    (1000, 1200, "Pupil"),
    (1200, 1400, "Pupil → Specialist"),
    (1400, 1600, "Specialist → Expert"),
    (1600, 1900, "Expert"),
]

# ── Tag → Category mapping ─────────────────────────────────────────────────
# Maps raw Codeforces tags to our higher-level technique categories.
TAG_TO_CATEGORY = {
    "implementation":           "Implementation",
    "brute force":              "Brute Force",
    "greedy":                   "Greedy",
    "sortings":                 "Sorting",
    "math":                     "Math",
    "number theory":            "Number Theory",
    "combinatorics":            "Combinatorics",
    "geometry":                 "Geometry",
    "dp":                       "Dynamic Programming",
    "binary search":            "Binary Search",
    "two pointers":             "Two Pointers",
    "data structures":          "Data Structures",
    "strings":                  "Strings",
    "string suffix structures": "Strings (Advanced)",
    "hashing":                  "Hashing",
    "graphs":                   "Graphs",
    "dfs and similar":          "DFS / BFS",
    "shortest paths":           "Shortest Paths",
    "trees":                    "Trees",
    "constructive algorithms":  "Constructive Algorithms",
    "bitmasks":                 "Bit Manipulation",
    "divide and conquer":       "Divide & Conquer",
    "games":                    "Game Theory",
    "flows":                    "Flows & Matching",
    "graph matchings":          "Flows & Matching",
    "interactive":              "Interactive",
    "probabilities":            "Probability",
    "matrices":                 "Matrices",
    "fft":                      "FFT",
    "ternary search":           "Ternary Search",
    "expression parsing":       "Expression Parsing",
    "meet-in-the-middle":       "Meet in the Middle",
    "2-sat":                    "2-SAT",
    "chinese remainder theorem":"Chinese Remainder Theorem",
    "schedules":                "Scheduling",
    "*special":                 None,   # skip special tag
}

# ── Colors (no purple/violet) ──────────────────────────────────────────────
RESET   = "\033[0m"
BOLD    = "\033[1m"
DIM     = "\033[2m"
GREEN   = "\033[32m"
YELLOW  = "\033[33m"
CYAN    = "\033[36m"
BLUE    = "\033[34m"
RED     = "\033[31m"
WHITE   = "\033[97m"
GRAY    = "\033[90m"
BRIGHT_GREEN  = "\033[92m"
BRIGHT_CYAN   = "\033[96m"
BRIGHT_BLUE   = "\033[94m"
ORANGE  = "\033[38;5;208m"

# Codeforces rank colors (no purple/violet)
RANK_COLORS = {
    "Newbie → Pupil":       GRAY,           # Gray for Newbie
    "Pupil":                GREEN,           # Green for Pupil
    "Pupil → Specialist":   BRIGHT_CYAN,     # Cyan for Specialist
    "Specialist → Expert":  BLUE,            # Blue for Expert transition
    "Expert":               BLUE,            # Dark blue for Expert
}

MIN_FREQUENCY = 0.05  # Show techniques with ≥ 5% frequency

BAR_FULL = "█"
BAR_HALF = "▌"


def color_bar(fraction: float, width: int = 30) -> str:
    filled = int(fraction * width)
    half = 1 if (fraction * width - filled) >= 0.5 else 0
    empty = width - filled - half
    if fraction >= 0.30:
        color = GREEN
    elif fraction >= 0.15:
        color = YELLOW
    else:
        color = CYAN
    return f"{color}{BAR_FULL * filled}{BAR_HALF * half}{RESET}{DIM}{'░' * empty}{RESET}"


# ── Analysis ────────────────────────────────────────────────────────────────

def load_problems(conn: sqlite3.Connection) -> list[dict]:
    """Load all rated problems from the database."""
    rows = conn.execute(
        "SELECT contest_id, problem_index, name, rating, tags, solved_count "
        "FROM problems WHERE rating IS NOT NULL"
    ).fetchall()

    problems = []
    for cid, idx, name, rating, tags_json, solved in rows:
        problems.append({
            "contest_id": cid,
            "index": idx,
            "name": name,
            "rating": rating,
            "tags": json.loads(tags_json),
            "solved_count": solved,
        })
    return problems


def analyze_band(problems: list[dict], lo: int, hi: int) -> dict:
    """Analyze technique frequencies for a rating band."""
    band_problems = [p for p in problems if lo <= p["rating"] < hi]
    total = len(band_problems)

    if total == 0:
        return {"total": 0, "categories": {}}

    # Count occurrences of each category
    category_counts = defaultdict(int)
    raw_tag_counts = defaultdict(int)

    for p in band_problems:
        seen_categories = set()  # avoid double-counting per problem
        for tag in p["tags"]:
            raw_tag_counts[tag] += 1
            category = TAG_TO_CATEGORY.get(tag, tag)  # fallback to raw tag
            if category and category not in seen_categories:
                category_counts[category] += 1
                seen_categories.add(category)

    # Build result sorted by frequency
    categories = {}
    for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        categories[cat] = {
            "count": count,
            "frequency": round(count / total, 4),
        }

    return {
        "total": total,
        "categories": categories,
        "raw_tags": dict(sorted(raw_tag_counts.items(), key=lambda x: x[1], reverse=True)),
    }


# ── Display ─────────────────────────────────────────────────────────────────

def display_band(lo: int, hi: int, label: str, analysis: dict):
    """Pretty-print analysis for one rating band."""
    total = analysis["total"]
    rank_color = RANK_COLORS.get(label, WHITE)

    print(f"\n{rank_color}{BOLD}{'═' * 70}")
    print(f"  Rating {lo}-{hi}  ·  {label}")
    print(f"{'═' * 70}{RESET}")
    print(f"  {DIM}Total rated problems: {total}{RESET}\n")

    print(f"  {BOLD}{'Technique':<35} {'Freq':>6}  {'Bar':<32} {'#Prob':>6}{RESET}")
    print(f"  {'─' * 62}")

    for cat, info in analysis["categories"].items():
        if info["frequency"] < MIN_FREQUENCY:
            break
        freq_pct = f"{info['frequency'] * 100:.1f}%"
        bar = color_bar(info["frequency"])
        print(f"  {cat:<35} {freq_pct:>6}  {bar}  {info['count']:>5}")


def display_progression(all_analyses: list):
    """Show technique frequency progression across bands."""
    print(f"\n{BOLD}{'━' * 70}")
    print(f"  TECHNIQUE PROGRESSION ACROSS RATINGS (Real Data)")
    print(f"{'━' * 70}{RESET}")

    # Collect all categories that appear
    key_categories = [
        "Implementation", "Greedy", "Math", "Binary Search",
        "Dynamic Programming", "Graphs", "DFS / BFS", "Trees",
        "Data Structures", "Constructive Algorithms", "Sorting",
        "Two Pointers", "Number Theory", "Combinatorics",
        "Strings", "Brute Force", "Bit Manipulation",
    ]

    bands = [(lo, hi) for lo, hi, _ in RATING_BANDS]

    print(f"\n  {BOLD}{'Technique':<28}", end="")
    for (lo, hi), (_, _, label) in zip(bands, RATING_BANDS):
        rank_color = RANK_COLORS.get(label, WHITE)
        print(f"{rank_color}{f' {lo}-{hi:>4}'.rjust(11)}{RESET}", end="")
    print()
    print(f"  {'─' * (28 + 11 * len(bands))}")

    for cat in key_categories:
        print(f"  {cat:<28}", end="")
        for i, (lo, hi) in enumerate(bands):
            analysis = all_analyses[i]
            info = analysis["categories"].get(cat)
            if info is None or info["frequency"] < 0.01:
                print(f"{DIM}{'—':>11}{RESET}", end="")
            else:
                pct = f"{info['frequency'] * 100:.1f}%"
                freq = info["frequency"]
                if freq >= 0.30:
                    print(f"{GREEN}{pct:>11}{RESET}", end="")
                elif freq >= 0.15:
                    print(f"{YELLOW}{pct:>11}{RESET}", end="")
                else:
                    print(f"{CYAN}{pct:>11}{RESET}", end="")
        print()

    print()


def display_roadmap_from_data(all_analyses: list):
    """Generate and display a data-driven roadmap."""
    print(f"\n{BOLD}{'━' * 70}")
    print(f"  DATA-DRIVEN ROADMAP: NEWBIE → EXPERT")
    print(f"{'━' * 70}{RESET}")

    icons = ["🟢", "🟡", "🟠", "🔴", "🔵"]
    stages = ["Foundation", "Core Skills", "Intermediate", "Advanced", "Expert"]

    for i, (lo, hi, label) in enumerate(RATING_BANDS):
        analysis = all_analyses[i]
        icon = icons[i]
        stage = stages[i]

        # Get top techniques for this band (frequency >= 10%)
        top_techs = [
            (cat, info)
            for cat, info in analysis["categories"].items()
            if info["frequency"] >= 0.10
        ]

        # Find techniques that are NEW or GROWING at this level
        # (appear significantly more than in the previous band)
        new_or_growing = []
        if i > 0:
            prev = all_analyses[i - 1]
            for cat, info in top_techs:
                prev_freq = prev["categories"].get(cat, {}).get("frequency", 0)
                growth = info["frequency"] - prev_freq
                if growth >= 0.03 or (prev_freq < 0.05 and info["frequency"] >= 0.08):
                    new_or_growing.append((cat, info["frequency"], growth))

        rank_color = RANK_COLORS.get(label, WHITE)
        print(f"\n  {icon} {rank_color}{BOLD}{lo}-{hi} — {stage}{RESET} {DIM}({label}){RESET}")

        if i == 0:
            # First band: just show top techniques
            for cat, info in top_techs[:6]:
                pct = f"{info['frequency'] * 100:.0f}%"
                print(f"     ├─ {cat} ({pct} of problems)")
        else:
            # Show what's new/growing
            if new_or_growing:
                new_or_growing.sort(key=lambda x: x[2], reverse=True)
                print(f"     {WHITE}New / Growing at this level:{RESET}")
                for cat, freq, growth in new_or_growing[:6]:
                    arrow = f"↑{growth * 100:.0f}%"
                    pct = f"{freq * 100:.0f}%"
                    print(f"     ├─ {cat} ({pct}) {GREEN}{arrow}{RESET}")

            # Show dominant techniques
            dominant = [(c, i) for c, i in top_techs if i["frequency"] >= 0.20]
            if dominant:
                print(f"     {WHITE}Dominant:{RESET}")
                for cat, info in dominant[:5]:
                    pct = f"{info['frequency'] * 100:.0f}%"
                    print(f"     ├─ {cat} ({pct})")

        if i < len(RATING_BANDS) - 1:
            print(f"     │")
            print(f"     ▼")


def export_real_data(all_analyses: list):
    """Export real analysis data as JSON."""
    output = {}
    for i, (lo, hi, label) in enumerate(RATING_BANDS):
        key = f"{lo}-{hi}"
        analysis = all_analyses[i]
        output[key] = {
            "label": label,
            "total_problems": analysis["total"],
            "techniques": {
                cat: {
                    "frequency": info["frequency"],
                    "problem_count": info["count"],
                }
                for cat, info in analysis["categories"].items()
            },
        }

    out_path = Path(__file__).parent / "data" / "real_analysis.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\n  {GREEN}✅ Real analysis data exported to: {out_path}{RESET}")


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    print(f"\n{BOLD}{WHITE}")
    print("   ╔══════════════════════════════════════════════════════════╗")
    print("   ║    CONTEST-LENS · Real Codeforces Data Analysis         ║")
    print("   ╚══════════════════════════════════════════════════════════╝")
    print(RESET)

    conn = sqlite3.connect(str(DB_PATH))

    # Load all rated problems
    problems = load_problems(conn)
    print(f"  Loaded {len(problems)} rated problems\n")

    # Analyze each band
    all_analyses = []
    for lo, hi, label in RATING_BANDS:
        analysis = analyze_band(problems, lo, hi)
        all_analyses.append(analysis)
        display_band(lo, hi, label, analysis)

    # Progression table
    display_progression(all_analyses)

    # Data-driven roadmap
    display_roadmap_from_data(all_analyses)

    # Export
    export_real_data(all_analyses)

    conn.close()

    print(f"\n{DIM}{'─' * 70}")
    print("  Analysis complete — based on real Codeforces API data.")
    print(f"{'─' * 70}{RESET}\n")


if __name__ == "__main__":
    main()

