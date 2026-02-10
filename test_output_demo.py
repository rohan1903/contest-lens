"""
Test file to demonstrate the expected output structure for the contest-lens project.
This shows what the visualization will display for different rating ranges.
"""

import json
from typing import Dict, List


# ── Technique Taxonomy ──────────────────────────────────────────────────────
# This is the hierarchical taxonomy we'll use to classify problems.
# Codeforces tags will be mapped into this structure.

TECHNIQUE_TAXONOMY = {
    "Implementation": {
        "description": "Basic coding / simulation problems",
        "cf_tags": ["implementation", "brute force"],
    },
    "Greedy": {
        "description": "Greedy algorithms and strategies",
        "cf_tags": ["greedy", "sortings"],
        "subtechniques": [
            "Interval Greedy",
            "Exchange Argument",
            "Activity Selection",
        ],
    },
    "Math": {
        "description": "Mathematical reasoning and number theory",
        "cf_tags": ["math", "number theory", "combinatorics"],
        "subtechniques": [
            "GCD / LCM",
            "Modular Arithmetic",
            "Prime Factorization",
            "Combinatorics",
            "Pigeonhole Principle",
        ],
    },
    "Binary Search": {
        "description": "Binary search on arrays and on answer",
        "cf_tags": ["binary search"],
        "subtechniques": [
            "Binary Search on Array",
            "Binary Search on Answer",
            "Ternary Search",
        ],
    },
    "Dynamic Programming": {
        "description": "DP techniques across dimensions",
        "cf_tags": ["dp"],
        "subtechniques": [
            "1D DP",
            "2D DP",
            "Knapsack",
            "Bitmask DP",
            "Digit DP",
            "Tree DP",
            "Interval DP",
        ],
    },
    "Graph Theory": {
        "description": "Graph algorithms and traversals",
        "cf_tags": ["graphs", "dfs and similar", "shortest paths", "trees"],
        "subtechniques": [
            "BFS / DFS",
            "Connected Components",
            "Shortest Path (Dijkstra / BFS)",
            "Topological Sort",
            "Multi-source BFS",
            "Cycle Detection",
            "Tree Traversal",
            "Tree DP",
            "LCA",
        ],
    },
    "Data Structures": {
        "description": "Fundamental and advanced data structures",
        "cf_tags": ["data structures"],
        "subtechniques": [
            "Arrays / Prefix Sums",
            "Stacks / Monotonic Stack",
            "Queues / Deques",
            "Hash Maps / Sets",
            "Segment Trees",
            "Fenwick Tree (BIT)",
            "Disjoint Set Union (DSU)",
        ],
    },
    "Two Pointers / Sliding Window": {
        "description": "Two pointer and window techniques",
        "cf_tags": ["two pointers"],
        "subtechniques": [
            "Classic Two Pointers",
            "Sliding Window",
            "Meet in the Middle",
        ],
    },
    "Strings": {
        "description": "String processing algorithms",
        "cf_tags": ["strings", "string suffix structures"],
        "subtechniques": [
            "String Hashing",
            "KMP / Z-function",
            "Trie",
            "Suffix Array",
        ],
    },
    "Constructive Algorithms": {
        "description": "Building valid solutions from scratch",
        "cf_tags": ["constructive algorithms"],
    },
    "Bit Manipulation": {
        "description": "Bitwise operations and tricks",
        "cf_tags": ["bitmasks"],
    },
    "Divide & Conquer": {
        "description": "Divide and conquer paradigm",
        "cf_tags": ["divide and conquer"],
    },
    "Geometry": {
        "description": "Computational geometry",
        "cf_tags": ["geometry"],
        "subtechniques": [
            "Convex Hull",
            "Line Intersection",
            "Sweep Line",
        ],
    },
    "Game Theory": {
        "description": "Sprague-Grundy, Nim, game state analysis",
        "cf_tags": ["games"],
    },
    "Flows & Matching": {
        "description": "Network flow and bipartite matching",
        "cf_tags": ["flows", "graph matchings"],
    },
}


# ── Sample Data: Simulated Codeforces Analysis ─────────────────────────────
# This is what the real output will look like after processing API data.

RATING_BANDS = {
    "800-1000": {
        "label": "Newbie → Pupil",
        "total_problems": 980,
        "techniques": {
            "Implementation":       {"frequency": 0.62, "problem_count": 607, "importance": 9.5},
            "Math":                 {"frequency": 0.38, "problem_count": 372, "importance": 8.0},
            "Greedy":               {"frequency": 0.30, "problem_count": 294, "importance": 8.5},
            "Strings":              {"frequency": 0.18, "problem_count": 176, "importance": 6.0},
            "Constructive Algorithms": {"frequency": 0.15, "problem_count": 147, "importance": 5.5},
            "Bit Manipulation":     {"frequency": 0.05, "problem_count":  49, "importance": 3.0},
        },
        "roadmap": [
            "Implementation",
            "Math (GCD, basic arithmetic)",
            "Greedy (simple exchanges)",
            "Strings (parsing, manipulation)",
        ],
        "insights": [
            "62% of problems are pure implementation — focus on clean coding speed",
            "Math basics (GCD, parity, divisibility) cover 38% of problems",
            "Greedy at this level is mostly observation-based, not algorithmic",
        ],
    },
    "1000-1200": {
        "label": "Pupil",
        "total_problems": 1100,
        "techniques": {
            "Implementation":       {"frequency": 0.50, "problem_count": 550, "importance": 9.0},
            "Greedy":               {"frequency": 0.35, "problem_count": 385, "importance": 9.0},
            "Math":                 {"frequency": 0.32, "problem_count": 352, "importance": 8.0},
            "Constructive Algorithms": {"frequency": 0.22, "problem_count": 242, "importance": 7.0},
            "Strings":              {"frequency": 0.18, "problem_count": 198, "importance": 6.0},
            "Data Structures":      {"frequency": 0.12, "problem_count": 132, "importance": 5.5},
            "Binary Search":        {"frequency": 0.08, "problem_count":  88, "importance": 5.0},
        },
        "roadmap": [
            "Greedy (sorting-based, exchange arguments)",
            "Constructive Algorithms",
            "Prefix Sums",
            "Basic Binary Search",
        ],
        "insights": [
            "Greedy jumps to 35% — start recognizing common greedy patterns",
            "Constructive problems appear more — practice building solutions",
            "Data structures begin mattering (maps, sets for counting)",
        ],
    },
    "1200-1400": {
        "label": "Pupil → Specialist",
        "total_problems": 1250,
        "techniques": {
            "Greedy":               {"frequency": 0.38, "problem_count": 475, "importance": 9.5},
            "Math":                 {"frequency": 0.35, "problem_count": 437, "importance": 8.5},
            "Implementation":       {"frequency": 0.33, "problem_count": 412, "importance": 7.5},
            "Binary Search":        {"frequency": 0.25, "problem_count": 312, "importance": 8.8},
            "Data Structures":      {"frequency": 0.22, "problem_count": 275, "importance": 8.0},
            "Constructive Algorithms": {"frequency": 0.20, "problem_count": 250, "importance": 7.0},
            "Two Pointers / Sliding Window": {"frequency": 0.18, "problem_count": 225, "importance": 7.5},
            "Dynamic Programming":  {"frequency": 0.12, "problem_count": 150, "importance": 7.0},
            "Graph Theory":         {"frequency": 0.10, "problem_count": 125, "importance": 6.5},
            "Strings":              {"frequency": 0.10, "problem_count": 125, "importance": 5.5},
        },
        "roadmap": [
            "Binary Search (on array and on answer)",
            "Two Pointers / Sliding Window",
            "Prefix Sums & Difference Arrays",
            "Intro DP (1D, simple 2D)",
            "Basic Graph Theory (BFS, DFS)",
        ],
        "insights": [
            "Binary Search on Answer appears — a critical technique to master",
            "DP problems begin appearing — start with classic patterns",
            "Graph Theory basics become necessary (BFS/DFS, connected components)",
            "Two Pointers is a high-ROI technique at this level",
        ],
    },
    "1400-1600": {
        "label": "Specialist → Expert",
        "total_problems": 1400,
        "techniques": {
            "Dynamic Programming":  {"frequency": 0.30, "problem_count": 420, "importance": 9.5},
            "Greedy":               {"frequency": 0.32, "problem_count": 448, "importance": 9.0},
            "Math":                 {"frequency": 0.30, "problem_count": 420, "importance": 8.5},
            "Graph Theory":         {"frequency": 0.28, "problem_count": 392, "importance": 9.0},
            "Data Structures":      {"frequency": 0.25, "problem_count": 350, "importance": 8.5},
            "Binary Search":        {"frequency": 0.22, "problem_count": 308, "importance": 8.5},
            "Two Pointers / Sliding Window": {"frequency": 0.18, "problem_count": 252, "importance": 7.5},
            "Constructive Algorithms": {"frequency": 0.18, "problem_count": 252, "importance": 7.0},
            "Strings":              {"frequency": 0.12, "problem_count": 168, "importance": 6.5},
            "Bit Manipulation":     {"frequency": 0.10, "problem_count": 140, "importance": 6.0},
            "Divide & Conquer":     {"frequency": 0.05, "problem_count":  70, "importance": 5.0},
        },
        "roadmap": [
            "DP (Knapsack, Bitmask DP, interval DP)",
            "Graph Theory (Shortest paths, Topological Sort, DSU)",
            "Segment Trees / Fenwick Trees",
            "Number Theory (Modular inverse, Sieve)",
            "Combinatorics",
        ],
        "insights": [
            "DP becomes dominant at 30% — the single most important topic to master",
            "Graph problems jump to 28% — Dijkstra, DSU, topo-sort are essential",
            "Advanced data structures (segment trees) start appearing",
            "Number theory deepens — modular arithmetic, Euler's totient",
        ],
    },
    "1600-1900": {
        "label": "Expert",
        "total_problems": 1600,
        "techniques": {
            "Dynamic Programming":  {"frequency": 0.38, "problem_count": 608, "importance": 10.0},
            "Graph Theory":         {"frequency": 0.32, "problem_count": 512, "importance": 9.5},
            "Data Structures":      {"frequency": 0.30, "problem_count": 480, "importance": 9.0},
            "Math":                 {"frequency": 0.28, "problem_count": 448, "importance": 8.5},
            "Greedy":               {"frequency": 0.25, "problem_count": 400, "importance": 8.0},
            "Binary Search":        {"frequency": 0.20, "problem_count": 320, "importance": 8.0},
            "Constructive Algorithms": {"frequency": 0.15, "problem_count": 240, "importance": 7.0},
            "Strings":              {"frequency": 0.15, "problem_count": 240, "importance": 7.0},
            "Two Pointers / Sliding Window": {"frequency": 0.12, "problem_count": 192, "importance": 6.5},
            "Bit Manipulation":     {"frequency": 0.12, "problem_count": 192, "importance": 6.5},
            "Divide & Conquer":     {"frequency": 0.08, "problem_count": 128, "importance": 6.0},
            "Game Theory":          {"frequency": 0.05, "problem_count":  80, "importance": 5.0},
            "Geometry":             {"frequency": 0.05, "problem_count":  80, "importance": 4.5},
            "Flows & Matching":     {"frequency": 0.03, "problem_count":  48, "importance": 4.0},
        },
        "roadmap": [
            "Advanced DP (Tree DP, Digit DP, Optimization)",
            "Advanced Graphs (LCA, Euler Tour, Heavy-Light Decomposition)",
            "Segment Trees with Lazy Propagation",
            "String Algorithms (KMP, Z-function, Hashing)",
            "Advanced Combinatorics (Inclusion-Exclusion, Burnside)",
        ],
        "insights": [
            "DP at 38% — tree DP, digit DP, and DP optimizations are must-knows",
            "Advanced data structures (lazy segment trees, merge sort tree) appear",
            "Graph algorithms deepen — LCA, Euler tour, heavy-light decomposition",
            "String algorithms become non-trivial (KMP, Z-function, suffix arrays)",
            "Game theory and geometry are niche but can be free points if studied",
        ],
    },
}


# ── Display Functions ───────────────────────────────────────────────────────

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
WHITE_BRIGHT = "\033[97m"
RED = "\033[31m"
BLUE = "\033[34m"
WHITE = "\033[97m"

BAR_FULL = "█"
BAR_HALF = "▌"


def color_bar(fraction: float, width: int = 30) -> str:
    """Return a colored bar string."""
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


def print_header(text: str, char: str = "═", width: int = 70):
    print(f"\n{BOLD}{char * width}")
    print(f"  {text}")
    print(f"{char * width}{RESET}")


def display_band(band_key: str, band: Dict):
    """Display a single rating band's analysis."""
    print_header(f"Rating {band_key}  ·  {band['label']}", "═")
    print(f"  {DIM}Total problems analyzed: {band['total_problems']}{RESET}\n")

    # ── Technique frequency table ───────────────────────────────────────
    print(f"  {BOLD}{'Technique':<35} {'Freq':>6}  {'Bar':<32} {'#Prob':>6}  {'Imp':>4}{RESET}")
    print(f"  {'─' * 68}")

    sorted_techs = sorted(
        band["techniques"].items(), key=lambda x: x[1]["frequency"], reverse=True
    )

    for tech, info in sorted_techs:
        freq_pct = f"{info['frequency'] * 100:.0f}%"
        bar = color_bar(info["frequency"])
        imp_color = GREEN if info["importance"] >= 8 else (YELLOW if info["importance"] >= 6 else DIM)
        print(
            f"  {tech:<35} {freq_pct:>6}  {bar}  {info['problem_count']:>5}  "
            f"{imp_color}{info['importance']:>4.1f}{RESET}"
        )

    # ── Roadmap ─────────────────────────────────────────────────────────
    print(f"\n  {BOLD}{WHITE_BRIGHT}📋 Roadmap for {band_key}:{RESET}")
    for i, item in enumerate(band["roadmap"], 1):
        print(f"     {WHITE_BRIGHT}{i}. {item}{RESET}")

    # ── Insights ────────────────────────────────────────────────────────
    print(f"\n  {BOLD}{BLUE}💡 Key Insights:{RESET}")
    for insight in band["insights"]:
        print(f"     {BLUE}• {insight}{RESET}")

    print()


def display_progression_summary():
    """Show how technique importance changes across ratings."""
    print_header("TECHNIQUE PROGRESSION ACROSS RATINGS", "━", 70)

    # Pick key techniques to track
    key_techniques = [
        "Implementation",
        "Greedy",
        "Math",
        "Binary Search",
        "Dynamic Programming",
        "Graph Theory",
        "Data Structures",
    ]

    bands = list(RATING_BANDS.keys())

    print(f"\n  {BOLD}{'Technique':<28}", end="")
    for b in bands:
        print(f" {b:>10}", end="")
    print(RESET)
    print(f"  {'─' * (28 + 11 * len(bands))}")

    for tech in key_techniques:
        print(f"  {tech:<28}", end="")
        for b in bands:
            freq = RATING_BANDS[b]["techniques"].get(tech, {}).get("frequency", 0)
            if freq == 0:
                cell = f"{'—':>10}"
                print(f"{DIM}{cell}{RESET}", end="")
            else:
                pct = f"{freq * 100:.0f}%"
                if freq >= 0.30:
                    print(f"{GREEN}{pct:>10}{RESET}", end="")
                elif freq >= 0.15:
                    print(f"{YELLOW}{pct:>10}{RESET}", end="")
                else:
                    print(f"{CYAN}{pct:>10}{RESET}", end="")
        print()

    print()


def display_full_roadmap():
    """Display the complete roadmap from Newbie to Expert."""
    print_header("COMPLETE ROADMAP: NEWBIE → EXPERT", "━", 70)

    milestones = [
        ("800-1000",  "🟢", "Foundation",
         ["Implementation speed", "Basic math (GCD, parity, modular)", "Simple greedy observations"]),
        ("1000-1200", "🟡", "Core Skills",
         ["Sorting-based greedy", "Constructive thinking", "Prefix sums", "Hash maps for counting"]),
        ("1200-1400", "🟠", "Intermediate",
         ["Binary search on answer", "Two pointers / sliding window", "Intro DP (1D, 2D)", "BFS / DFS basics"]),
        ("1400-1600", "🔴", "Advanced",
         ["DP variants (knapsack, bitmask, interval)", "Shortest paths (Dijkstra)", "DSU", "Segment trees", "Number theory (sieve, mod inverse)"]),
        ("1600-1900", "🔵", "Expert",
         ["Tree DP, digit DP, DP optimization", "LCA, Euler tour, HLD", "Lazy segment trees", "String algorithms (KMP, Z-fn)", "Advanced combinatorics"]),
    ]

    for band, icon, stage, topics in milestones:
        label = RATING_BANDS[band]["label"]
        print(f"\n  {icon} {BOLD}{band} — {stage}{RESET} {DIM}({label}){RESET}")
        for t in topics:
            print(f"     ├─ {t}")
        if band != "1600-1900":
            print(f"     │")
            print(f"     ▼")


def export_json():
    """Export the complete data as JSON for frontend consumption."""
    output = {
        "taxonomy": TECHNIQUE_TAXONOMY,
        "rating_bands": RATING_BANDS,
    }
    path = "sample_output.json"
    with open(path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\n  {GREEN}✅ Exported to {path}{RESET}")


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    print(f"\n{BOLD}{WHITE}")
    print("   ╔══════════════════════════════════════════════════════════╗")
    print("   ║          CONTEST-LENS · Sample Output Demo              ║")
    print("   ║     Technique Hierarchy & Roadmap by Rating Band        ║")
    print("   ╚══════════════════════════════════════════════════════════╝")
    print(RESET)

    # Show each rating band
    for band_key, band_data in RATING_BANDS.items():
        display_band(band_key, band_data)

    # Progression summary
    display_progression_summary()

    # Full roadmap
    display_full_roadmap()

    # Export JSON
    export_json()

    print(f"\n{DIM}{'─' * 70}")
    print("  This is sample/simulated data.")
    print("  Real data will be fetched from the Codeforces API.")
    print(f"{'─' * 70}{RESET}\n")


if __name__ == "__main__":
    main()

